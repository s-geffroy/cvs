"""Generate population-weighted sample points per state from Natural Earth populated_places.

For each ISO3 in the canonical UN list, we:
1. Collect all populated places ``ne_10m_populated_places.geojson`` whose
   ``ADM0_A3`` (or equivalent) matches the ISO3.
2. Take the ``POP_MAX`` field as the per-city population.
3. Choose ``k = min(5, 1 + ⌊log₁₀(total_population_in_millions)⌋)``
   cluster centers via weighted k-means (each city contributes a sample
   with weight = population).
4. Emit a JSON list of ``(iso3, longitude_deg, latitude_deg, weight)``
   sample points — each ISO3 contributes ``k`` rows.

Edge cases:
- Micro-states with a single city → 1 sample point at that city.
- States missing from populated_places → fall back on the ADM0 polygon
  centroid (uniformly weighted, no clustering).

The weight assigned to each sample point is the cluster's population share
of the country total. This propagates to the GP as the observation's
inverse-variance prior (small populations contribute less to the field).
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass

import numpy as np

from apps.basis_builder.paths import DATA_SOURCES_DIR
from apps.basis_builder.un_members import un_member_iso3_codes

POPULATED_PLACES_PATH = (
    DATA_SOURCES_DIR / "natural_earth" / "ne_10m_populated_places.geojson"
)
NATURAL_EARTH_ADM0_PATH = (
    DATA_SOURCES_DIR / "natural_earth" / "ne_110m_admin_0_countries.geojson"
)
SAMPLE_POINTS_PATH = DATA_SOURCES_DIR / "natural_earth" / "state_sample_points.json"


@dataclass(frozen=True)
class SamplePoint:
    iso3: str
    longitude_deg: float
    latitude_deg: float
    weight: float
    cluster_index: int  # 0-based; the most populous cluster has index 0


def _polygon_centroid(geometry: dict) -> tuple[float, float]:
    """Approximate the centroid of an ADM0 geometry (polygon or multipolygon).

    For prototype use only — not aware of dateline crossing or spherical
    geometry. Acceptable as a fallback for states with no populated_places
    coverage.
    """
    coordinates_to_average: list[tuple[float, float]] = []
    if geometry["type"] == "Polygon":
        coordinates_to_average.extend(geometry["coordinates"][0])
    elif geometry["type"] == "MultiPolygon":
        for polygon in geometry["coordinates"]:
            coordinates_to_average.extend(polygon[0])
    longitudes = [point[0] for point in coordinates_to_average]
    latitudes = [point[1] for point in coordinates_to_average]
    return float(np.mean(longitudes)), float(np.mean(latitudes))


def _adm0_centroids_by_iso3() -> dict[str, tuple[float, float]]:
    if not NATURAL_EARTH_ADM0_PATH.exists():
        return {}
    payload = json.loads(NATURAL_EARTH_ADM0_PATH.read_text())
    centroids: dict[str, tuple[float, float]] = {}
    for feature in payload.get("features", []):
        iso3 = feature.get("properties", {}).get("iso3") or feature.get(
            "properties", {}
        ).get("ADM0_A3")
        if not iso3:
            continue
        centroids[iso3] = _polygon_centroid(feature["geometry"])
    return centroids


def _cities_by_iso3() -> dict[str, list[tuple[float, float, float]]]:
    """Return ``{iso3: [(longitude_deg, latitude_deg, population), ...]}``."""
    payload = json.loads(POPULATED_PLACES_PATH.read_text())
    cities_per_iso3: dict[str, list[tuple[float, float, float]]] = {}
    for feature in payload["features"]:
        properties = feature["properties"]
        iso3 = properties.get("ADM0_A3") or properties.get("ISO_A3")
        if not iso3 or iso3 == "-99":
            continue
        try:
            longitude_deg, latitude_deg = feature["geometry"]["coordinates"]
        except (TypeError, ValueError, KeyError):
            continue
        population_max = properties.get("POP_MAX") or properties.get("POP_MIN") or 0
        if population_max is None or population_max <= 0:
            continue
        cities_per_iso3.setdefault(iso3, []).append(
            (float(longitude_deg), float(latitude_deg), float(population_max))
        )
    return cities_per_iso3


def _weighted_kmeans(
    coordinates: np.ndarray,
    weights: np.ndarray,
    n_clusters: int,
    n_iterations: int = 20,
    random_seed: int = 7,
) -> np.ndarray:
    """Minimal weighted k-means in 2D — no sphere correction (prototype-grade).

    Returns the cluster centers as a (n_clusters, 2) array of (lon, lat).
    """
    rng = np.random.default_rng(random_seed)
    n_points = coordinates.shape[0]
    if n_clusters >= n_points:
        return coordinates.copy()

    # k-means++ initialisation, weighted
    probability = weights / weights.sum()
    initial_index = rng.choice(n_points, p=probability)
    centers = [coordinates[initial_index]]
    for _ in range(n_clusters - 1):
        distances_squared = np.min(
            np.array(
                [
                    np.sum((coordinates - center) ** 2, axis=1)
                    for center in centers
                ]
            ),
            axis=0,
        )
        weighted_distribution = distances_squared * weights
        if weighted_distribution.sum() == 0:
            break
        probability = weighted_distribution / weighted_distribution.sum()
        chosen_index = rng.choice(n_points, p=probability)
        centers.append(coordinates[chosen_index])
    centers_array = np.array(centers)

    for _ in range(n_iterations):
        distances_to_centers = np.array(
            [
                np.sum((coordinates - center) ** 2, axis=1)
                for center in centers_array
            ]
        )
        cluster_assignments = np.argmin(distances_to_centers, axis=0)
        new_centers = []
        for cluster_index in range(len(centers_array)):
            mask = cluster_assignments == cluster_index
            if not np.any(mask):
                new_centers.append(centers_array[cluster_index])
                continue
            cluster_weights = weights[mask]
            cluster_coordinates = coordinates[mask]
            new_centers.append(
                np.average(cluster_coordinates, axis=0, weights=cluster_weights)
            )
        new_centers_array = np.array(new_centers)
        if np.allclose(new_centers_array, centers_array, atol=1e-6):
            break
        centers_array = new_centers_array
    return centers_array


def _cluster_weights(
    coordinates: np.ndarray, weights: np.ndarray, centers: np.ndarray
) -> np.ndarray:
    """Return the total weight assigned to each cluster center."""
    distances_to_centers = np.array(
        [np.sum((coordinates - center) ** 2, axis=1) for center in centers]
    )
    cluster_assignments = np.argmin(distances_to_centers, axis=0)
    cluster_total_weights = np.zeros(len(centers), dtype=float)
    for cluster_index in range(len(centers)):
        mask = cluster_assignments == cluster_index
        cluster_total_weights[cluster_index] = weights[mask].sum()
    return cluster_total_weights


def _n_clusters_for_population(total_population: float) -> int:
    """k = min(5, 1 + ⌊log₁₀(population_in_millions)⌋), with a floor of 1."""
    population_in_millions = total_population / 1.0e6
    if population_in_millions < 1.0:
        return 1
    return int(min(5, 1 + math.floor(math.log10(population_in_millions))))


def generate_sample_points_per_state() -> list[SamplePoint]:
    """Compute the per-state sample points and persist them to JSON."""
    cities_per_iso3 = _cities_by_iso3()
    adm0_centroids = _adm0_centroids_by_iso3()
    canonical_un_iso3s = un_member_iso3_codes()

    sample_points: list[SamplePoint] = []
    states_without_cities: list[str] = []
    states_without_centroid: list[str] = []

    for iso3 in sorted(canonical_un_iso3s):
        cities = cities_per_iso3.get(iso3, [])
        if not cities:
            fallback_centroid = adm0_centroids.get(iso3)
            if fallback_centroid is None:
                states_without_centroid.append(iso3)
                continue
            states_without_cities.append(iso3)
            sample_points.append(
                SamplePoint(
                    iso3=iso3,
                    longitude_deg=fallback_centroid[0],
                    latitude_deg=fallback_centroid[1],
                    weight=1.0,
                    cluster_index=0,
                )
            )
            continue

        coordinates = np.array([(longitude, latitude) for longitude, latitude, _ in cities])
        weights = np.array([population for _, _, population in cities], dtype=float)
        total_population = float(weights.sum())

        n_clusters = _n_clusters_for_population(total_population)
        cluster_centers = _weighted_kmeans(coordinates, weights, n_clusters)
        cluster_weights = _cluster_weights(coordinates, weights, cluster_centers)

        order = np.argsort(cluster_weights)[::-1]
        cluster_centers = cluster_centers[order]
        cluster_weights = cluster_weights[order]

        normalised_weights = cluster_weights / max(cluster_weights.sum(), 1e-12)
        for cluster_index, ((longitude_deg, latitude_deg), normalised_weight) in enumerate(
            zip(cluster_centers, normalised_weights)
        ):
            sample_points.append(
                SamplePoint(
                    iso3=iso3,
                    longitude_deg=float(longitude_deg),
                    latitude_deg=float(latitude_deg),
                    weight=float(normalised_weight),
                    cluster_index=cluster_index,
                )
            )

    payload = {
        "_meta": {
            "source": "Natural Earth 10m populated places (cities) — for prototype only; production should switch to GPW v4 or GHS-POP raster.",
            "n_sample_points": len(sample_points),
            "n_states_with_cities": len(canonical_un_iso3s)
            - len(states_without_cities)
            - len(states_without_centroid),
            "states_without_cities_fallback_centroid": states_without_cities,
            "states_without_centroid": states_without_centroid,
            "n_clusters_rule": "k = min(5, 1 + floor(log10(population_in_millions))), floor 1",
        },
        "sample_points": [
            {
                "iso3": sample_point.iso3,
                "longitude_deg": sample_point.longitude_deg,
                "latitude_deg": sample_point.latitude_deg,
                "weight": sample_point.weight,
                "cluster_index": sample_point.cluster_index,
            }
            for sample_point in sample_points
        ],
    }
    SAMPLE_POINTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAMPLE_POINTS_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return sample_points

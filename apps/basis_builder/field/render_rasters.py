"""Generate PNG rasters of the continuous field for MapLibre image overlays.

For each (component, metric) couple we render one PNG covering the world
in equirectangular projection (the MapLibre raster source then warps it
to Mercator). The PNG dimensions match the grid (360 × 181 for the V2
1°-spaced grid).

Metrics rendered per raw component:
- ``mean`` — predicted value ``μ`` (signed colormap RdBu_r)
- ``grad_magnitude`` — fault lines ``‖∇μ‖`` (perceptual colormap Plasma)

Three additional aggregate indicators are rendered:
- ``civ_identity_sharpness`` — entropy-inverse of the affinity vector (2.1, paired)
- ``civ_texture_intensity``  — trace of the deformation tensor tr(G) (3.1, paired)
- ``civ_classification_margin`` — Davies-Bouldin-local margin (2.2, standalone)

The ``index.json`` entries carry ``read_mode`` ∈ {"raw", "paired", "standalone"}
and an optional ``pair_with`` so the UI can render the appropriate guidance
banner (cf. ``site_src/docs/assets/js/map.js``).

Output: ``site_src/docs/assets/data/continuous_field/<component>_<metric>.png``
+ a small ``site_src/docs/assets/data/continuous_field/index.json`` listing
the available rasters with their min/max for legend rendering.

The PNG vertical axis is flipped so latitude 90° (north) is at the top —
standard image convention required by MapLibre.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from matplotlib import colormaps as matplotlib_colormaps
from matplotlib.colors import Normalize
from PIL import Image

from apps.basis_builder.field.train_v2 import (
    CONTINUOUS_FIELD_V2_ARRAYS_PATH,
    CONTINUOUS_FIELD_V2_META_PATH,
)
from apps.basis_builder.paths import CIVILIZATION_CENTROIDS_PATH, REPO_ROOT
from packages.civvec_core.algebra.distances import (
    intra_civilizational_covariance_inverse,
)
from packages.civvec_core.continuous_field.aggregate_indicators import (
    X_SCORE_COMPONENT_NAMES,
    affinity_entropy_inverse_field,
    classification_margin_field,
    deformation_trace_field,
)

CIVILIZATION_IDS_ORDER: tuple[str, ...] = (
    "western",
    "orthodox",
    "islamic",
    "sinic",
    "hindic",
    "japanese",
    "buddhist",
    "latin_american",
    "african",
    "indigenous",
    "oceanian",
)

RASTERS_OUTPUT_DIR = (
    REPO_ROOT / "site_src" / "docs" / "assets" / "data" / "continuous_field"
)

COMPONENTS_TO_RENDER: tuple[str, ...] = (
    "x_viz_ts",
    "x_viz_se",
    "x_score_pdi",
    "x_score_idv",
    "x_score_mas",
    "x_score_uai",
    "x_score_lto",
    "x_score_ivr",
)


@dataclass
class RasterRecord:
    component_name: str
    metric_name: str
    filename: str
    colormap_name: str
    value_min: float
    value_max: float
    physical_units: str
    description_fr: str
    read_mode: str = "raw"
    pair_with: str | None = None


@dataclass(frozen=True)
class AggregateIndicatorSpec:
    component_name: str
    colormap_name: str
    quantile_range: tuple[float, float]
    description_fr: str
    read_mode: str
    pair_with: str | None = None


AGGREGATE_INDICATORS_TO_RENDER: tuple[AggregateIndicatorSpec, ...] = (
    AggregateIndicatorSpec(
        component_name="civ_identity_sharpness",
        colormap_name="viridis",
        quantile_range=(0.02, 0.98),
        description_fr=(
            "Force d’identité civilisationnelle — 1 = cœur identitaire net, "
            "0 = zone interstitielle (entropie inverse normalisée du vecteur "
            "d’affinité GP)."
        ),
        read_mode="paired",
        pair_with="civ_texture_intensity",
    ),
    AggregateIndicatorSpec(
        component_name="civ_texture_intensity",
        colormap_name="plasma",
        quantile_range=(0.0, 0.98),
        description_fr=(
            "Tension culturelle locale — somme des magnitudes de gradient sur "
            "les 19 composantes (trace du tenseur de déformation G(p) en "
            "métrique sphérique)."
        ),
        read_mode="paired",
        pair_with="civ_identity_sharpness",
    ),
    AggregateIndicatorSpec(
        component_name="civ_classification_margin",
        colormap_name="cividis",
        quantile_range=(0.0, 0.95),
        description_fr=(
            "Profondeur du cœur civilisationnel — marge (d₂ − d₁) / d₁ entre "
            "les deux centroïdes les plus proches en B_score (Mahalanobis "
            "intra-civilisationnelle). Élevé = cœur stable, proche de 0 = "
            "fault line."
        ),
        read_mode="standalone",
    ),
)


def _flip_for_image(grid_array: np.ndarray) -> np.ndarray:
    """MapLibre expects raster origin top-left → flip latitude axis."""
    return np.flipud(grid_array)


def _array_to_png_with_colormap(
    grid_array: np.ndarray,
    output_path: Path,
    colormap_name: str,
    value_range: tuple[float, float],
) -> None:
    normalisation = Normalize(vmin=value_range[0], vmax=value_range[1], clip=True)
    colormap = matplotlib_colormaps[colormap_name]
    normalised_array = normalisation(_flip_for_image(grid_array))
    rgba_float = colormap(normalised_array.filled(0.5) if hasattr(normalised_array, "filled") else normalised_array)

    nan_mask = ~np.isfinite(_flip_for_image(grid_array))
    rgba_byte = (rgba_float * 255.0).astype(np.uint8)
    rgba_byte[..., 3] = np.where(nan_mask, 0, rgba_byte[..., 3])

    Image.fromarray(rgba_byte, mode="RGBA").save(output_path, format="PNG")


def _value_range_robust(
    grid_array: np.ndarray, lower_quantile: float, upper_quantile: float
) -> tuple[float, float]:
    finite_values = grid_array[np.isfinite(grid_array)]
    if finite_values.size == 0:
        return 0.0, 1.0
    return (
        float(np.quantile(finite_values, lower_quantile)),
        float(np.quantile(finite_values, upper_quantile)),
    )


def _compute_aggregate_indicator_fields(arrays, metadata: dict) -> dict[str, np.ndarray]:
    """Compute 2.1, 3.1 and 2.2 from arrays already present in the NPZ.

    No GP refit; reads only ``__predicted_mean`` and ``__gradient_magnitude``
    arrays produced by :mod:`apps.basis_builder.field.train_v2`.
    """
    affinity_predicted_mean_by_civilization: dict[str, np.ndarray] = {}
    for civilization_id in CIVILIZATION_IDS_ORDER:
        array_key = f"affinity_{civilization_id}__predicted_mean"
        if array_key in arrays.files:
            affinity_predicted_mean_by_civilization[civilization_id] = np.array(
                arrays[array_key]
            )

    gradient_magnitude_by_component: dict[str, np.ndarray] = {}
    for array_key in arrays.files:
        if array_key.endswith("__gradient_magnitude"):
            component_name = array_key.removesuffix("__gradient_magnitude")
            gradient_magnitude_by_component[component_name] = np.array(arrays[array_key])

    x_score_field_by_component: dict[str, np.ndarray] = {}
    for component_name in X_SCORE_COMPONENT_NAMES:
        array_key = f"{component_name}__predicted_mean"
        if array_key in arrays.files:
            x_score_field_by_component[component_name] = np.array(arrays[array_key])

    centroid_document = json.loads(CIVILIZATION_CENTROIDS_PATH.read_text())
    centroids_by_id = {
        entry["civilization_id"]: entry for entry in centroid_document["centroids"]
    }
    centroid_mu_scores = np.array(
        [centroids_by_id[civ]["mu_score"] for civ in CIVILIZATION_IDS_ORDER],
        dtype=np.float64,
    )
    centroid_sigma_scores = np.array(
        [centroids_by_id[civ]["sigma_score"] for civ in CIVILIZATION_IDS_ORDER],
        dtype=np.float64,
    )
    covariance_inverse = intra_civilizational_covariance_inverse(centroid_sigma_scores)

    z_score_std_by_component = metadata.get("_meta", {}).get("z_score_stds", {})

    return {
        "civ_identity_sharpness": affinity_entropy_inverse_field(
            affinity_predicted_mean_by_civilization
        ),
        "civ_texture_intensity": deformation_trace_field(
            gradient_magnitude_by_component,
            z_score_std_by_component=z_score_std_by_component,
        ),
        "civ_classification_margin": classification_margin_field(
            x_score_field_by_component,
            centroid_mu_scores,
            covariance_inverse,
        ),
    }


def render_rasters_for_field() -> list[RasterRecord]:
    if not CONTINUOUS_FIELD_V2_ARRAYS_PATH.exists():
        raise FileNotFoundError(
            "Run `python -m apps.basis_builder.field.train_v2` first to produce "
            f"{CONTINUOUS_FIELD_V2_ARRAYS_PATH}."
        )
    metadata = json.loads(CONTINUOUS_FIELD_V2_META_PATH.read_text())
    arrays = np.load(CONTINUOUS_FIELD_V2_ARRAYS_PATH)
    RASTERS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    records: list[RasterRecord] = []

    metric_specifications = (
        (
            "mean",
            "predicted_mean",
            "RdBu_r",
            (0.02, 0.98),
            "Valeur prédite μ par le GP, échelle signée centrée sur la moyenne globale.",
        ),
        (
            "grad_magnitude",
            "gradient_magnitude",
            "plasma",
            (0.0, 0.98),
            "Magnitude du gradient ‖∇μ‖ — fault lines civilisationnelles.",
        ),
    )

    for component_name in COMPONENTS_TO_RENDER:
        for (
            metric_short,
            array_suffix,
            colormap_name,
            quantile_range,
            description_fr,
        ) in metric_specifications:
            array_key = f"{component_name}__{array_suffix}"
            if array_key not in arrays.files:
                continue
            grid_array = np.array(arrays[array_key])
            value_range = _value_range_robust(grid_array, *quantile_range)
            output_filename = f"{component_name}_{metric_short}.png"
            output_path = RASTERS_OUTPUT_DIR / output_filename
            _array_to_png_with_colormap(
                grid_array, output_path, colormap_name, value_range
            )
            records.append(
                RasterRecord(
                    component_name=component_name,
                    metric_name=metric_short,
                    filename=output_filename,
                    colormap_name=colormap_name,
                    value_min=value_range[0],
                    value_max=value_range[1],
                    physical_units=metadata["_meta"]
                    .get("z_score_stds", {})
                    .get(component_name, ""),
                    description_fr=description_fr,
                    read_mode="raw",
                )
            )

    aggregate_fields = _compute_aggregate_indicator_fields(arrays, metadata)
    for indicator_spec in AGGREGATE_INDICATORS_TO_RENDER:
        grid_array = aggregate_fields[indicator_spec.component_name]
        value_range = _value_range_robust(grid_array, *indicator_spec.quantile_range)
        output_filename = f"{indicator_spec.component_name}_mean.png"
        output_path = RASTERS_OUTPUT_DIR / output_filename
        _array_to_png_with_colormap(
            grid_array, output_path, indicator_spec.colormap_name, value_range
        )
        records.append(
            RasterRecord(
                component_name=indicator_spec.component_name,
                metric_name="mean",
                filename=output_filename,
                colormap_name=indicator_spec.colormap_name,
                value_min=value_range[0],
                value_max=value_range[1],
                physical_units="",
                description_fr=indicator_spec.description_fr,
                read_mode=indicator_spec.read_mode,
                pair_with=indicator_spec.pair_with,
            )
        )

    grid_longitudes_deg = metadata["grid"]["longitudes_deg"]
    grid_latitudes_deg = metadata["grid"]["latitudes_deg"]

    def _raster_entry(record: RasterRecord) -> dict:
        entry: dict = {
            "component": record.component_name,
            "metric": record.metric_name,
            "filename": record.filename,
            "colormap": record.colormap_name,
            "value_min": record.value_min,
            "value_max": record.value_max,
            "description_fr": record.description_fr,
            "read_mode": record.read_mode,
        }
        if record.pair_with is not None:
            entry["pair_with"] = record.pair_with
        return entry

    index_payload = {
        "_meta": {
            "schema": "continuous_field_rasters_index.schema.json",
            "n_rasters": len(records),
            "grid_step_deg": metadata["_meta"]["grid_step_deg"],
            "documentation": "docs/17_continuous_field.md",
        },
        "bbox": {
            "longitude_min_deg": float(min(grid_longitudes_deg)),
            "longitude_max_deg": float(max(grid_longitudes_deg)),
            "latitude_min_deg": float(min(grid_latitudes_deg)),
            "latitude_max_deg": float(max(grid_latitudes_deg)),
        },
        "rasters": [_raster_entry(record) for record in records],
    }
    (RASTERS_OUTPUT_DIR / "index.json").write_text(
        json.dumps(index_payload, indent=2, ensure_ascii=False)
    )
    return records


if __name__ == "__main__":
    rendered_records = render_rasters_for_field()
    print(f"Rendered {len(rendered_records)} rasters to {RASTERS_OUTPUT_DIR}")
    for record in rendered_records:
        print(
            f"  {record.filename}: [{record.value_min:.3f}, {record.value_max:.3f}] "
            f"colormap={record.colormap_name}"
        )

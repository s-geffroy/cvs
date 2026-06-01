"""Natural Earth ADM0 (sovereign states) geometries — fetch, filter, tag.

We pin Natural Earth Vector at a known commit so the build is reproducible.
Output: ``data_sources/natural_earth/admin0_sovereign_110m.geojson`` carrying
``properties.geometry_source = "Natural Earth"`` on every feature and a
top-level ``properties.geometry_provenance`` block compatible with
``schemas/geometry_provenance.schema.json`` (no GADM).

Natural Earth Vector is **public domain** (https://www.naturalearthdata.com/about/terms-of-use/).
The pinned upstream commit gives a stable, auditable input.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from apps.basis_builder.paths import DATA_SOURCES_DIR, STATE_COORDINATES_PATH

NATURAL_EARTH_DIR = DATA_SOURCES_DIR / "natural_earth"
NATURAL_EARTH_ADM0_PATH = NATURAL_EARTH_DIR / "admin0_countries_110m.geojson"

NATURAL_EARTH_PINNED_COMMIT = "ca96624a56bd078437bca8184e78163e5039ad19"
NATURAL_EARTH_DATASET = "ne_110m_admin_0_countries"
NATURAL_EARTH_URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    f"{NATURAL_EARTH_PINNED_COMMIT}/geojson/{NATURAL_EARTH_DATASET}.geojson"
)


def _load_target_iso3_codes() -> set[str]:
    state_coordinates_payload = json.loads(STATE_COORDINATES_PATH.read_text())
    return {entry["iso3"] for entry in state_coordinates_payload["states"]}


def _download_admin0_sovereign_110m() -> dict:
    request = urllib.request.Request(
        NATURAL_EARTH_URL,
        headers={"User-Agent": "civvec-site-builder/2.0 (+https://github.com/s-geffroy/cvs)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def _tag_feature_with_provenance(feature: dict) -> dict:
    properties = feature.setdefault("properties", {})
    properties["geometry_source"] = "Natural Earth"
    properties["geometry_license"] = "Public Domain"
    properties["geometry_pinned_commit"] = NATURAL_EARTH_PINNED_COMMIT
    return feature


def _extract_iso3(feature: dict) -> str | None:
    properties = feature.get("properties", {})
    for candidate_key in ("ISO_A3_EH", "ADM0_ISO", "ADM0_A3", "ADM0_A3_US"):
        candidate = properties.get(candidate_key)
        if isinstance(candidate, str) and len(candidate) == 3 and candidate.isalpha():
            return candidate.upper()
    return None


def fetch_and_filter_natural_earth_admin0(
    target_iso3_codes: set[str] | None = None,
    force_refresh: bool = False,
) -> Path:
    """Download Natural Earth ADM0 110m, filter to target ISO3, tag provenance, write GeoJSON."""
    NATURAL_EARTH_DIR.mkdir(parents=True, exist_ok=True)
    if NATURAL_EARTH_ADM0_PATH.exists() and not force_refresh:
        return NATURAL_EARTH_ADM0_PATH

    target_iso3_codes = target_iso3_codes or _load_target_iso3_codes()
    raw_payload = _download_admin0_sovereign_110m()

    kept_features: list[dict] = []
    for feature in raw_payload.get("features", []):
        iso3 = _extract_iso3(feature)
        if iso3 is None or iso3 not in target_iso3_codes:
            continue
        feature["properties"]["iso3"] = iso3
        kept_features.append(_tag_feature_with_provenance(feature))

    output_payload = {
        "type": "FeatureCollection",
        "properties": {
            "geometry_provenance": {
                "geometry_source": "Natural Earth",
                "geometry_license": "Public Domain",
                "natural_earth_dataset": NATURAL_EARTH_DATASET,
                "natural_earth_pinned_commit": NATURAL_EARTH_PINNED_COMMIT,
                "natural_earth_upstream_url": NATURAL_EARTH_URL,
                "contains_gadm_geometry": False,
            },
            "feature_count": len(kept_features),
            "iso3_kept": sorted({feature["properties"]["iso3"] for feature in kept_features}),
        },
        "features": kept_features,
    }
    NATURAL_EARTH_ADM0_PATH.write_text(json.dumps(output_payload, ensure_ascii=False))
    return NATURAL_EARTH_ADM0_PATH


def load_admin0_collection() -> dict:
    if not NATURAL_EARTH_ADM0_PATH.exists():
        raise FileNotFoundError(
            "Natural Earth ADM0 GeoJSON missing — run `civvec basis fetch-geometries` first."
        )
    return json.loads(NATURAL_EARTH_ADM0_PATH.read_text())


def extract_single_state_geojson(iso3: str) -> dict | None:
    """Return a standalone GeoJSON FeatureCollection for one ISO3, or None."""
    collection = load_admin0_collection()
    iso3 = iso3.upper()
    matching_features = [
        feature for feature in collection["features"]
        if feature["properties"].get("iso3") == iso3
    ]
    if not matching_features:
        return None
    return {
        "type": "FeatureCollection",
        "properties": {
            "iso3": iso3,
            "geometry_provenance": {
                "geometry_source": "Natural Earth",
                "geometry_license": "Public Domain",
                "natural_earth_dataset": NATURAL_EARTH_DATASET,
                "natural_earth_pinned_commit": NATURAL_EARTH_PINNED_COMMIT,
                "contains_gadm_geometry": False,
            },
        },
        "features": matching_features,
    }

"""Natural Earth ADM0 (sovereign states) geometries — fetch, filter, tag.

We pin Natural Earth Vector at a known commit so the build is reproducible.
Output: ``data_sources/natural_earth/admin0_countries_110m.geojson`` carrying
``properties.geometry_source = "Natural Earth"`` on every feature and a
top-level ``properties.geometry_provenance`` block compatible with
``schemas/geometry_provenance.schema.json`` (no GADM).

Pour couvrir l'intégralité des 193 États membres de l'ONU, on complète NE 110m
(simplification globale, qui agrège les micro-États) par NE 50m pour les
micro-États ONU manquants (Andorre, Monaco, Saint-Marin, Liechtenstein, Malte,
Singapour, etc.). Chaque feature porte ``properties.natural_earth_dataset`` qui
indique sa résolution d'origine.

Natural Earth Vector is **public domain** (https://www.naturalearthdata.com/about/terms-of-use/).
The pinned upstream commit gives a stable, auditable input.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from apps.basis_builder.paths import DATA_SOURCES_DIR
from apps.basis_builder.un_members import un_member_iso3_codes

NATURAL_EARTH_DIR = DATA_SOURCES_DIR / "natural_earth"
NATURAL_EARTH_ADM0_PATH = NATURAL_EARTH_DIR / "admin0_countries_110m.geojson"

NATURAL_EARTH_PINNED_COMMIT = "ca96624a56bd078437bca8184e78163e5039ad19"
NATURAL_EARTH_DATASET_110M = "ne_110m_admin_0_countries"
NATURAL_EARTH_DATASET_50M = "ne_50m_admin_0_countries"
NATURAL_EARTH_URL_110M = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    f"{NATURAL_EARTH_PINNED_COMMIT}/geojson/{NATURAL_EARTH_DATASET_110M}.geojson"
)
NATURAL_EARTH_URL_50M = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    f"{NATURAL_EARTH_PINNED_COMMIT}/geojson/{NATURAL_EARTH_DATASET_50M}.geojson"
)

# Conservé pour rétro-compatibilité (anciens imports).
NATURAL_EARTH_DATASET = NATURAL_EARTH_DATASET_110M
NATURAL_EARTH_URL = NATURAL_EARTH_URL_110M

# Antarctique exclu : aucune affiliation civilisationnelle, écrase visuellement
# la projection Mercator du choropleth.
EXCLUDED_ISO3_CODES = frozenset({"ATA"})


def _http_get_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "civvec-site-builder/2.0 (+https://github.com/s-geffroy/cvs)"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def _download_admin0_sovereign_110m() -> dict:
    return _http_get_json(NATURAL_EARTH_URL_110M)


def _download_admin0_sovereign_50m() -> dict:
    return _http_get_json(NATURAL_EARTH_URL_50M)


def _tag_feature_with_provenance(feature: dict, natural_earth_dataset: str) -> dict:
    properties = feature.setdefault("properties", {})
    properties["geometry_source"] = "Natural Earth"
    properties["geometry_license"] = "Public Domain"
    properties["geometry_pinned_commit"] = NATURAL_EARTH_PINNED_COMMIT
    properties["natural_earth_dataset"] = natural_earth_dataset
    return feature


def _extract_iso3(feature: dict) -> str | None:
    properties = feature.get("properties", {})
    for candidate_key in ("ISO_A3_EH", "ADM0_ISO", "ADM0_A3", "ADM0_A3_US"):
        candidate = properties.get(candidate_key)
        if isinstance(candidate, str) and len(candidate) == 3 and candidate.isalpha():
            return candidate.upper()
    return None


def _extract_name_fr(feature: dict) -> str | None:
    properties = feature.get("properties", {})
    for candidate_key in ("NAME_FR", "NAME_LONG", "NAME"):
        candidate = properties.get(candidate_key)
        if isinstance(candidate, str) and candidate.strip():
            return candidate
    return None


def _attach_iso3_and_name(feature: dict, iso3: str) -> None:
    name_fr = _extract_name_fr(feature)
    feature["properties"]["iso3"] = iso3
    if name_fr:
        feature["properties"]["name_fr"] = name_fr


def fetch_and_tag_natural_earth_admin0(force_refresh: bool = False) -> Path:
    """Télécharge NE 110m, complète avec NE 50m pour les États ONU manquants,
    et écrit le geojson tagué pour la carte.

    On ne filtre plus sur Hofstede/IW : toute la collection est conservée, et
    on ajoute les micro-États ONU absents de NE 110m. Antarctique exclu.
    """
    NATURAL_EARTH_DIR.mkdir(parents=True, exist_ok=True)
    if NATURAL_EARTH_ADM0_PATH.exists() and not force_refresh:
        return NATURAL_EARTH_ADM0_PATH

    raw_110m = _download_admin0_sovereign_110m()

    kept_features: list[dict] = []
    excluded_iso3s: list[str] = []
    iso3_seen: set[str] = set()
    for feature in raw_110m.get("features", []):
        iso3 = _extract_iso3(feature)
        if iso3 is None:
            continue
        if iso3 in EXCLUDED_ISO3_CODES:
            excluded_iso3s.append(iso3)
            continue
        if iso3 in iso3_seen:
            continue
        iso3_seen.add(iso3)
        _attach_iso3_and_name(feature, iso3)
        kept_features.append(_tag_feature_with_provenance(feature, NATURAL_EARTH_DATASET_110M))

    un_iso3 = un_member_iso3_codes()
    missing_un_iso3 = sorted(un_iso3 - iso3_seen)
    patched_from_50m: list[str] = []
    if missing_un_iso3:
        raw_50m = _download_admin0_sovereign_50m()
        index_50m: dict[str, dict] = {}
        for feature_50m in raw_50m.get("features", []):
            iso3_50m = _extract_iso3(feature_50m)
            if iso3_50m is None or iso3_50m in iso3_seen:
                continue
            if iso3_50m in EXCLUDED_ISO3_CODES:
                continue
            if iso3_50m in index_50m:
                continue
            index_50m[iso3_50m] = feature_50m
        for iso3 in missing_un_iso3:
            feature_50m = index_50m.get(iso3)
            if feature_50m is None:
                continue
            _attach_iso3_and_name(feature_50m, iso3)
            kept_features.append(
                _tag_feature_with_provenance(feature_50m, NATURAL_EARTH_DATASET_50M)
            )
            iso3_seen.add(iso3)
            patched_from_50m.append(iso3)

    output_payload = {
        "type": "FeatureCollection",
        "properties": {
            "geometry_provenance": {
                "geometry_source": "Natural Earth",
                "geometry_license": "Public Domain",
                "natural_earth_dataset": NATURAL_EARTH_DATASET_110M,
                "natural_earth_dataset_microstates": NATURAL_EARTH_DATASET_50M,
                "natural_earth_pinned_commit": NATURAL_EARTH_PINNED_COMMIT,
                "natural_earth_upstream_url": NATURAL_EARTH_URL_110M,
                "contains_gadm_geometry": False,
            },
            "feature_count": len(kept_features),
            "iso3_kept": sorted(iso3_seen),
            "iso3_excluded": sorted(set(excluded_iso3s)),
            "iso3_patched_from_50m": sorted(patched_from_50m),
            "iso3_un_still_missing": sorted(un_iso3 - iso3_seen),
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
                "natural_earth_dataset": matching_features[0]["properties"].get(
                    "natural_earth_dataset", NATURAL_EARTH_DATASET_110M
                ),
                "natural_earth_pinned_commit": NATURAL_EARTH_PINNED_COMMIT,
                "contains_gadm_geometry": False,
            },
        },
        "features": matching_features,
    }

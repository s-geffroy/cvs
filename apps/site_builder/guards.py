"""Publication guards: ethics warning + geometry source allowlist.

These constants and assertions are referenced by both the site builder and the
test suite. Touch with care.
"""
from __future__ import annotations

import json
from pathlib import Path

ETHICAL_WARNING: str = (
    "This profile is inferred from public aggregate sources. "
    "It must not be used to classify real individuals."
)

ETHICAL_WARNING_FR: str = (
    "Ce profil est inféré à partir de sources publiques agrégées. "
    "Il ne doit pas être utilisé pour classer des individus réels."
)

ALLOWED_GEOMETRY_SOURCES: frozenset[str] = frozenset({"Natural Earth", "geoBoundaries"})

FORBIDDEN_GEOMETRY_SOURCES: frozenset[str] = frozenset({"GADM"})


def assert_geometry_source_in_allowlist(geometry_source: str) -> None:
    if geometry_source not in ALLOWED_GEOMETRY_SOURCES:
        raise ValueError(
            f"Geometry source '{geometry_source}' is not in the allowlist "
            f"{sorted(ALLOWED_GEOMETRY_SOURCES)}; refusing to publish."
        )


def assert_no_gadm_geometry(geojson_payload: dict) -> None:
    provenance = geojson_payload.get("properties", {}).get("geometry_provenance", {})
    source = provenance.get("geometry_source", "")
    if source in FORBIDDEN_GEOMETRY_SOURCES:
        raise ValueError(
            "Refusing to publish: payload sources geometry from "
            f"forbidden provider '{source}'."
        )
    if provenance.get("contains_gadm_geometry") is True:
        raise ValueError("Refusing to publish: contains_gadm_geometry == True")


def scan_directory_for_gadm(directory: Path) -> list[Path]:
    """Return any *.geojson files in directory whose provenance mentions GADM."""
    offenders: list[Path] = []
    for geojson_path in directory.rglob("*.geojson"):
        try:
            payload = json.loads(geojson_path.read_text())
            assert_no_gadm_geometry(payload)
        except ValueError:
            offenders.append(geojson_path)
        except (json.JSONDecodeError, KeyError):
            continue
    return offenders

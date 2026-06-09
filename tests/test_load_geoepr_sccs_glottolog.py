"""Unit tests for the three external-dataset loaders (no network in tests).

The download functions themselves are not exercised — that would
require network access. Instead we test the pure-Python parsing
helpers on small synthetic fixtures and verify the public surface
(dataclasses, normalised JSON shapes) is stable.
"""
from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from apps.basis_builder.load_geoepr import (
    EthnicRecord,
    _polygon_centroid_and_area,
    write_normalised_json as write_geoepr_normalised_json,
)
from apps.basis_builder.load_glottolog import (
    GlottologLanguoid,
    _extract_languoid_csv_text,
    _row_to_languoid,
    write_normalised_json as write_glottolog_normalised_json,
)
from apps.basis_builder.load_sccs import (
    SccsSociety,
    _read_sccs_csv,
    write_normalised_json as write_sccs_normalised_json,
)


def test_polygon_centroid_for_unit_square_is_centre() -> None:
    """A 1°×1° square centred on (0, 0) → centroid (0, 0), area ≈ degree²."""
    unit_square_ring = [
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0),
        (0.0, 0.0),
    ]
    centroid_longitude, centroid_latitude, area_km_squared = _polygon_centroid_and_area(
        [unit_square_ring]
    )
    assert abs(centroid_longitude - 0.5) < 1e-9
    assert abs(centroid_latitude - 0.5) < 1e-9
    # At ~0° latitude, 1° ≈ 111 km in both directions → area ≈ 12 321 km².
    assert 10_000 < area_km_squared < 15_000


def test_sccs_csv_reader_parses_minimal_row(tmp_path: Path) -> None:
    csv_path = tmp_path / "societies.csv"
    csv_path.write_text(
        "id,pref_name_for_society,glottocode,Lat,Lon,region\n"
        "SCCS001,Nama,nama1265,-24.5,17.0,Africa\n"
        "SCCS002,Yoruba,yoru1245,7.5,4.5,Africa\n",
        encoding="utf-8",
    )
    societies = _read_sccs_csv(csv_path)
    assert len(societies) == 2
    assert societies[0].sccs_society_id == "SCCS001"
    assert societies[0].glottocode == "nama1265"
    assert societies[1].sccs_society_name == "Yoruba"


def test_sccs_write_normalised_json_round_trip(tmp_path: Path, monkeypatch) -> None:
    societies = [
        SccsSociety(
            sccs_society_id="SCCS001",
            sccs_society_name="Nama",
            glottocode="nama1265",
            latitude_deg=-24.5,
            longitude_deg=17.0,
            region="Africa",
        )
    ]
    sentinel_path = tmp_path / "sccs.json"
    monkeypatch.setattr(
        "apps.basis_builder.load_sccs.SCCS_NORMALISED_JSON_PATH", sentinel_path
    )
    monkeypatch.setattr(
        "apps.basis_builder.load_sccs.SCCS_CACHE_DIR", tmp_path
    )
    output_path = write_sccs_normalised_json(societies)
    assert output_path == sentinel_path
    payload = json.loads(output_path.read_text())
    assert payload["_meta"]["n_societies"] == 1
    assert payload["societies"][0]["sccs_society_id"] == "SCCS001"


def test_glottolog_row_parser_handles_minimal_columns() -> None:
    row = {
        "id": "yoru1245",
        "name": "Yoruba",
        "level": "language",
        "family_id": "atla1278",
        "macroarea": "Africa",
        "latitude": "8.0",
        "longitude": "4.5",
    }
    languoid = _row_to_languoid(row)
    assert languoid is not None
    assert languoid.glottocode == "yoru1245"
    assert languoid.level == "language"
    assert languoid.family_glottocode == "atla1278"
    assert languoid.latitude_deg == 8.0


def test_glottolog_extract_languoid_csv_text(tmp_path: Path) -> None:
    zip_path = tmp_path / "languoid.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr(
            "languoid.csv",
            "id,name,level,family_id,macroarea,latitude,longitude\n"
            "yoru1245,Yoruba,language,atla1278,Africa,8.0,4.5\n",
        )
    text = _extract_languoid_csv_text(zip_path)
    assert "Yoruba" in text


def test_geoepr_write_normalised_json_round_trip(
    tmp_path: Path, monkeypatch
) -> None:
    records = [
        EthnicRecord(
            ethnic_group_id="fra_breton",
            ethnic_group_label="Bretons",
            iso3="FRA",
            centroid_longitude_deg=-3.0,
            centroid_latitude_deg=48.0,
            area_km_squared=27000.0,
            state_population_estimate=67_000_000.0,
            group_population_share=0.02,
            political_status="powerless",
        )
    ]
    sentinel_path = tmp_path / "ethnic_records.json"
    monkeypatch.setattr(
        "apps.basis_builder.load_geoepr.GEOEPR_NORMALISED_JSON_PATH", sentinel_path
    )
    monkeypatch.setattr(
        "apps.basis_builder.load_geoepr.GEOEPR_CACHE_DIR", tmp_path
    )
    output_path = write_geoepr_normalised_json(records)
    assert output_path == sentinel_path
    payload = json.loads(output_path.read_text())
    assert payload["_meta"]["n_records"] == 1
    assert payload["ethnic_records"][0]["ethnic_group_id"] == "fra_breton"

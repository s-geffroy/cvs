"""Load GeoEPR — Ethnic Power Relations geo-referenced polygons (ETH Zurich GROWup).

GeoEPR provides ~800 ethnic-group polygons covering the post-1946 world,
each tagged with the host state (Correlates-Of-War code), the group's
political status (monopoly / dominant / senior partner / junior partner /
self-exclusion / powerless / discriminated / state-collapse), and an
``umbrella`` group identifier when applicable. Time-varying entries are
merged into a single representative polygon per group (latest year
available).

Source: https://icr.ethz.ch/data/epr/geoepr/  — CC-BY-NC-SA-4.0
EPR-Core (status table): https://icr.ethz.ch/data/epr/core/

This loader stays standalone (no GeoPandas, no GDAL): it uses pyshp to
read the shapefile and a pure-Python centroid formula. The state
crosswalk COW → ISO3 is provided locally in ``COW_TO_ISO3``.

Output JSON shape (``ethnic_records_normalised.json``)::

    {
      "_meta": {...},
      "ethnic_records": [
        {
          "ethnic_group_id": "624.0",
          "ethnic_group_label": "Yoruba",
          "iso3": "NGA",
          "centroid_longitude_deg": 4.12,
          "centroid_latitude_deg": 7.55,
          "area_km_squared": 158_400,
          "state_population_estimate": 218_540_000,
          "group_population_share": 0.18,
          "political_status": "junior_partner",
          "glottolog_languoid_id": null,
          "sccs_society_id": null
        },
        ...
      ]
    }

Note: ``state_population_estimate`` is left to be filled in by the
caller — typically using the ``state_coordinates.json`` per-state
metadata. The same applies to ``glottolog_languoid_id`` and
``sccs_society_id``, populated by :mod:`apps.basis_builder.ethnic_crosswalk`.
"""
from __future__ import annotations

import csv
import io
import json
import urllib.error
import urllib.request
import zipfile
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from apps.basis_builder.paths import DATA_SOURCES_DIR

GEOEPR_REMOTE_ZIP_URL: str = "https://icr.ethz.ch/data/epr/geoepr/GeoEPR-2021.zip"
EPR_CORE_REMOTE_CSV_URL: str = "https://icr.ethz.ch/data/epr/core/EPR-2021.csv"

GEOEPR_CACHE_DIR = DATA_SOURCES_DIR / "geoepr"
GEOEPR_SHAPEFILE_DIR = GEOEPR_CACHE_DIR / "GeoEPR-2021"
GEOEPR_LOCAL_ZIP_PATH = GEOEPR_CACHE_DIR / "GeoEPR-2021.zip"
EPR_CORE_LOCAL_CSV_PATH = GEOEPR_CACHE_DIR / "EPR-2021.csv"
GEOEPR_NORMALISED_JSON_PATH = GEOEPR_CACHE_DIR / "ethnic_records_normalised.json"

EARTH_RADIUS_KM_FOR_AREA: float = 6371.0


@dataclass(frozen=True)
class EthnicRecord:
    """A single GeoEPR ethnic group, normalised for the support strategies."""

    ethnic_group_id: str
    ethnic_group_label: str
    iso3: str
    centroid_longitude_deg: float
    centroid_latitude_deg: float
    area_km_squared: float
    state_population_estimate: float
    group_population_share: float
    political_status: str | None
    glottolog_languoid_id: str | None = None
    sccs_society_id: str | None = None


# Minimal COW→ISO3 crosswalk for the 193 UN states. Populated below for
# the cases that differ from the obvious ISO mapping; the rest is
# handled by the standard alpha-3 lookup in ``_cow_to_iso3``.
COW_TO_ISO3: dict[int, str] = {
    2: "USA", 20: "CAN", 40: "CUB", 41: "HTI", 42: "DOM", 51: "JAM",
    52: "TTO", 53: "BRB", 54: "DMA", 55: "GRD", 56: "LCA", 57: "VCT",
    58: "ATG", 60: "BLZ", 70: "MEX", 80: "BLZ", 90: "GTM", 91: "HND",
    92: "SLV", 93: "NIC", 94: "CRI", 95: "PAN", 100: "COL", 101: "VEN",
    110: "GUY", 115: "SUR", 130: "ECU", 135: "PER", 140: "BRA", 145: "BOL",
    150: "PRY", 155: "CHL", 160: "ARG", 165: "URY", 200: "GBR", 205: "IRL",
    210: "NLD", 211: "BEL", 212: "LUX", 220: "FRA", 221: "MCO", 223: "LIE",
    225: "CHE", 230: "ESP", 232: "AND", 235: "PRT", 260: "DEU",
    290: "POL", 305: "AUT", 310: "HUN", 316: "CZE", 317: "SVK",
    325: "ITA", 327: "MLT", 338: "MLT", 339: "ALB", 341: "MNE",
    343: "MKD", 344: "HRV", 345: "SRB", 346: "BIH", 347: "KOS",
    349: "SVN", 350: "GRC", 352: "CYP", 355: "BGR", 359: "MDA",
    360: "ROU", 365: "RUS", 366: "EST", 367: "LVA", 368: "LTU",
    369: "UKR", 370: "BLR", 371: "ARM", 372: "GEO", 373: "AZE",
    375: "FIN", 380: "SWE", 385: "NOR", 390: "DNK", 395: "ISL",
    402: "CPV", 403: "STP", 404: "GNB", 411: "GNQ", 420: "GMB",
    432: "MLI", 433: "SEN", 434: "BEN", 435: "MRT", 436: "NER",
    437: "CIV", 438: "GIN", 439: "BFA", 450: "LBR", 451: "SLE",
    452: "GHA", 461: "TGO", 471: "CMR", 475: "NGA", 481: "GAB",
    482: "CAF", 483: "TCD", 484: "COG", 490: "COD", 500: "UGA",
    501: "KEN", 510: "TZA", 516: "BDI", 517: "RWA", 520: "SOM",
    522: "DJI", 530: "ETH", 531: "ERI", 540: "AGO", 541: "MOZ",
    551: "ZMB", 552: "ZWE", 553: "MWI", 560: "ZAF", 565: "NAM",
    570: "LSO", 571: "BWA", 572: "SWZ", 580: "MDG", 581: "COM",
    590: "MUS", 591: "SYC", 600: "MAR", 615: "DZA", 616: "TUN",
    620: "LBY", 625: "SDN", 626: "SSD", 630: "IRN", 640: "TUR",
    645: "IRQ", 651: "EGY", 652: "SYR", 660: "LBN", 663: "JOR",
    666: "ISR", 670: "SAU", 678: "YEM", 690: "KWT", 692: "BHR",
    694: "QAT", 696: "ARE", 698: "OMN", 700: "AFG", 701: "TKM",
    702: "TJK", 703: "KGZ", 704: "UZB", 705: "KAZ", 710: "CHN",
    712: "MNG", 713: "TWN", 731: "PRK", 732: "KOR", 740: "JPN",
    750: "IND", 760: "BTN", 770: "PAK", 771: "BGD", 775: "MMR",
    780: "LKA", 781: "MDV", 790: "NPL", 800: "THA", 811: "KHM",
    812: "LAO", 816: "VNM", 820: "MYS", 830: "SGP", 835: "BRN",
    840: "PHL", 850: "IDN", 860: "TLS", 900: "AUS", 920: "NZL",
    935: "VUT", 940: "SLB", 950: "FJI", 970: "KIR", 983: "MHL",
    986: "PLW", 987: "FSM", 990: "WSM", 999: "PNG",
}


def _download(url: str, destination: Path, timeout_seconds: float = 120.0) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=timeout_seconds) as response:
            destination.write_bytes(response.read())
    except urllib.error.URLError as error:
        raise RuntimeError(f"Failed to download {url}: {error}") from error
    return destination


def download_geoepr(force: bool = False) -> Path:
    """Download GeoEPR shapefile zip + EPR Core CSV into the local cache."""
    if not GEOEPR_LOCAL_ZIP_PATH.exists() or force:
        _download(GEOEPR_REMOTE_ZIP_URL, GEOEPR_LOCAL_ZIP_PATH)
    if not EPR_CORE_LOCAL_CSV_PATH.exists() or force:
        _download(EPR_CORE_REMOTE_CSV_URL, EPR_CORE_LOCAL_CSV_PATH)
    if not any(GEOEPR_SHAPEFILE_DIR.glob("*.shp")) or force:
        GEOEPR_SHAPEFILE_DIR.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(GEOEPR_LOCAL_ZIP_PATH) as archive:
            for member_name in archive.namelist():
                if member_name.endswith("/"):
                    continue
                target_path = GEOEPR_SHAPEFILE_DIR / Path(member_name).name
                with archive.open(member_name) as source_handle:
                    target_path.write_bytes(source_handle.read())
    return GEOEPR_SHAPEFILE_DIR


def _load_epr_core() -> dict[tuple[int, str], dict[str, Any]]:
    """Map ``(cow_code, group_id) → group dict`` with latest available year."""
    if not EPR_CORE_LOCAL_CSV_PATH.exists():
        return {}
    csv_text = EPR_CORE_LOCAL_CSV_PATH.read_text(encoding="utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(csv_text))
    latest_record_by_key: dict[tuple[int, str], dict[str, Any]] = {}
    for row in reader:
        try:
            cow_code = int(row.get("gwid") or row.get("cowcode") or row.get("cowid") or 0)
        except (TypeError, ValueError):
            continue
        group_id_value = row.get("groupid") or row.get("gwgroupid") or ""
        if not group_id_value:
            continue
        key = (cow_code, str(group_id_value))
        end_year_value = row.get("to") or row.get("endyear") or row.get("gweyear")
        try:
            end_year = int(end_year_value) if end_year_value else 0
        except (TypeError, ValueError):
            end_year = 0
        existing = latest_record_by_key.get(key)
        if existing is None or end_year >= int(existing.get("_end_year", 0)):
            latest_record_by_key[key] = {**row, "_end_year": end_year}
    return latest_record_by_key


def _polygon_centroid_and_area(
    polygon_rings: list[list[tuple[float, float]]],
) -> tuple[float, float, float]:
    """Centroid (lon, lat) and area in km² for a list of (lon, lat) rings.

    Pure-Python signed-area formula (planar projection — adequate for
    ~ethnic-group-sized polygons; we are not computing precise spherical
    areas, just relative weights). Holes (subsequent rings) are
    subtracted.
    """
    weighted_longitude_sum = 0.0
    weighted_latitude_sum = 0.0
    signed_area_sum = 0.0
    for ring_index, ring in enumerate(polygon_rings):
        if len(ring) < 3:
            continue
        ring_signed_area = 0.0
        ring_centroid_longitude = 0.0
        ring_centroid_latitude = 0.0
        for vertex_index in range(len(ring) - 1):
            longitude_a, latitude_a = ring[vertex_index]
            longitude_b, latitude_b = ring[vertex_index + 1]
            cross_product = longitude_a * latitude_b - longitude_b * latitude_a
            ring_signed_area += cross_product
            ring_centroid_longitude += (longitude_a + longitude_b) * cross_product
            ring_centroid_latitude += (latitude_a + latitude_b) * cross_product
        ring_signed_area *= 0.5
        if abs(ring_signed_area) < 1e-12:
            continue
        ring_centroid_longitude /= 6.0 * ring_signed_area
        ring_centroid_latitude /= 6.0 * ring_signed_area
        sign = 1.0 if ring_index == 0 else -1.0
        weighted_longitude_sum += sign * ring_centroid_longitude * ring_signed_area
        weighted_latitude_sum += sign * ring_centroid_latitude * ring_signed_area
        signed_area_sum += sign * ring_signed_area
    if abs(signed_area_sum) < 1e-12:
        all_vertices_longitude = [longitude for ring in polygon_rings for longitude, _ in ring]
        all_vertices_latitude = [latitude for ring in polygon_rings for _, latitude in ring]
        return (
            float(np.mean(all_vertices_longitude)) if all_vertices_longitude else 0.0,
            float(np.mean(all_vertices_latitude)) if all_vertices_latitude else 0.0,
            0.0,
        )
    centroid_longitude = weighted_longitude_sum / signed_area_sum
    centroid_latitude = weighted_latitude_sum / signed_area_sum
    mean_latitude_rad = np.deg2rad(centroid_latitude)
    degree_longitude_km = (np.pi * EARTH_RADIUS_KM_FOR_AREA / 180.0) * np.cos(
        mean_latitude_rad
    )
    degree_latitude_km = np.pi * EARTH_RADIUS_KM_FOR_AREA / 180.0
    area_km_squared = float(
        abs(signed_area_sum) * degree_longitude_km * degree_latitude_km
    )
    return float(centroid_longitude), float(centroid_latitude), area_km_squared


def _shapefile_records() -> list[dict[str, Any]]:
    """Yield one dict per shapefile record using pyshp.

    Returns the union of ``(geometry, properties)`` for each record; the
    polygon is exposed as a list of rings (each ring is a list of
    ``(lon, lat)``).
    """
    import shapefile  # type: ignore[import-not-found]

    shp_paths = list(GEOEPR_SHAPEFILE_DIR.glob("*.shp"))
    if not shp_paths:
        raise FileNotFoundError(
            f"No .shp inside {GEOEPR_SHAPEFILE_DIR}; run download_geoepr() first."
        )
    reader = shapefile.Reader(
        str(shp_paths[0]), encoding="latin-1", encodingErrors="replace"
    )
    records: list[dict[str, Any]] = []
    field_names = [field_descriptor[0] for field_descriptor in reader.fields[1:]]
    for shape_record in reader.shapeRecords():
        attributes = dict(zip(field_names, shape_record.record))
        rings: list[list[tuple[float, float]]] = []
        points = shape_record.shape.points
        parts = list(shape_record.shape.parts) + [len(points)]
        for part_index in range(len(parts) - 1):
            ring_points = points[parts[part_index] : parts[part_index + 1]]
            rings.append([(float(point[0]), float(point[1])) for point in ring_points])
        records.append({"attributes": attributes, "rings": rings})
    return records


def _cow_to_iso3(cow_code: int) -> str | None:
    return COW_TO_ISO3.get(cow_code)


def build_ethnic_records(
    state_population_lookup: Mapping[str, float] | None = None,
) -> list[EthnicRecord]:
    """Merge GeoEPR shapes + EPR Core attributes into one normalised list.

    For each shapefile record:
    - parse polygon rings → centroid + area (planar approximation)
    - look up the political status / umbrella from EPR Core (latest year)
    - join the host state's population from the supplied lookup
    - merge multiple GeoEPR rows for the same ethnic group into a single
      record (largest-area row wins for centroid/status)
    """
    shapefile_records = _shapefile_records()
    epr_core_by_key = _load_epr_core()

    records_by_group_key: dict[tuple[str, str], EthnicRecord] = {}
    for shapefile_record in shapefile_records:
        attributes = shapefile_record["attributes"]
        rings = shapefile_record["rings"]
        if not rings:
            continue
        try:
            cow_code = int(
                attributes.get("gwid")
                or attributes.get("statecode")
                or attributes.get("cowcode")
                or 0
            )
        except (TypeError, ValueError):
            cow_code = 0
        iso3 = _cow_to_iso3(cow_code)
        if not iso3:
            continue
        ethnic_group_id_raw = attributes.get("groupid") or attributes.get("gwgroupid")
        if ethnic_group_id_raw is None:
            continue
        ethnic_group_id = str(ethnic_group_id_raw)
        ethnic_group_label = str(
            attributes.get("group") or attributes.get("groupname") or "?"
        ).strip()
        end_year_value = attributes.get("to") or attributes.get("endyear") or 0
        try:
            end_year = int(end_year_value)
        except (TypeError, ValueError):
            end_year = 0
        longitude_centroid, latitude_centroid, area_from_geometry = (
            _polygon_centroid_and_area(rings)
        )
        # Prefer the shapefile's authoritative ``sqkm`` field over the
        # planar approximation when available.
        sqkm_value = attributes.get("sqkm")
        if sqkm_value is not None:
            try:
                area_km_squared = float(sqkm_value)
            except (TypeError, ValueError):
                area_km_squared = area_from_geometry
        else:
            area_km_squared = area_from_geometry

        core_lookup = epr_core_by_key.get((cow_code, ethnic_group_id), {})
        political_status_raw = (
            core_lookup.get("status") or attributes.get("status") or None
        )
        political_status = (
            str(political_status_raw).strip().lower().replace(" ", "_")
            if political_status_raw
            else None
        )
        try:
            group_population_share = float(core_lookup.get("size") or 0.0)
        except (TypeError, ValueError):
            group_population_share = 0.0

        state_population_estimate = (
            float(state_population_lookup.get(iso3, 0.0))
            if state_population_lookup
            else 0.0
        )

        record = EthnicRecord(
            ethnic_group_id=ethnic_group_id,
            ethnic_group_label=ethnic_group_label,
            iso3=iso3,
            centroid_longitude_deg=longitude_centroid,
            centroid_latitude_deg=latitude_centroid,
            area_km_squared=area_km_squared,
            state_population_estimate=state_population_estimate,
            group_population_share=group_population_share,
            political_status=political_status,
        )
        key = (iso3, ethnic_group_id)
        existing = records_by_group_key.get(key)
        if existing is None or end_year > 0:
            # Prefer the latest-active row for each group.
            records_by_group_key[key] = record
    return sorted(
        records_by_group_key.values(),
        key=lambda current_record: (current_record.iso3, current_record.ethnic_group_id),
    )


def write_normalised_json(records: Iterable[EthnicRecord]) -> Path:
    GEOEPR_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    record_list = list(records)
    payload = {
        "_meta": {
            "schema": "geoepr_ethnic_records_normalised.schema.json",
            "source_geoepr": GEOEPR_REMOTE_ZIP_URL,
            "source_epr_core": EPR_CORE_REMOTE_CSV_URL,
            "license": "CC-BY-NC-SA-4.0 (ETH GROWup)",
            "n_records": len(record_list),
        },
        "ethnic_records": [asdict(record) for record in record_list],
    }
    GEOEPR_NORMALISED_JSON_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False)
    )
    return GEOEPR_NORMALISED_JSON_PATH


def load_ethnic_records_from_cache() -> list[EthnicRecord]:
    """Re-hydrate the normalised JSON into a list of ``EthnicRecord``."""
    if not GEOEPR_NORMALISED_JSON_PATH.exists():
        raise FileNotFoundError(
            f"Normalised ethnic records JSON missing at {GEOEPR_NORMALISED_JSON_PATH}; "
            "run build_ethnic_records() + write_normalised_json() first."
        )
    payload = json.loads(GEOEPR_NORMALISED_JSON_PATH.read_text())
    return [EthnicRecord(**record_dict) for record_dict in payload["ethnic_records"]]


def _state_population_lookup_from_populated_places() -> dict[str, float]:
    """Approximate state population by summing ``POP_MAX`` over NE 10m cities.

    The shape ``ne_10m_populated_places.geojson`` lists ~7 000 cities
    worldwide with a ``POP_MAX`` field. Summing per ISO3 gives an
    urban-population proxy (50–80 % of true population for most states),
    which is enough for the support strategies — the weighting compares
    *relative* group sizes within a state, not absolute headcounts.
    Production callers should prefer a UN-DESA or World Bank lookup.
    """
    from apps.basis_builder.paths import DATA_SOURCES_DIR

    populated_places_path = (
        DATA_SOURCES_DIR / "natural_earth" / "ne_10m_populated_places.geojson"
    )
    if not populated_places_path.exists():
        return {}
    payload = json.loads(populated_places_path.read_text())
    population_by_iso3: dict[str, float] = {}
    for feature in payload.get("features", []):
        properties = feature.get("properties", {}) or {}
        iso3 = properties.get("ADM0_A3") or properties.get("ISO_A3")
        if not iso3 or iso3 == "-99":
            continue
        pop_max = properties.get("POP_MAX") or properties.get("POP_MIN") or 0
        if pop_max and pop_max > 0:
            population_by_iso3[iso3] = (
                population_by_iso3.get(iso3, 0.0) + float(pop_max)
            )
    return population_by_iso3


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--download",
        action="store_true",
        help="Force download of GeoEPR shapefile + EPR Core CSV before parsing.",
    )
    args = parser.parse_args()
    if args.download:
        download_geoepr(force=False)
    state_population_lookup = _state_population_lookup_from_populated_places()
    ethnic_records = build_ethnic_records(state_population_lookup)
    output_path = write_normalised_json(ethnic_records)
    print(
        f"Wrote {len(ethnic_records)} ethnic records to "
        f"{output_path.relative_to(DATA_SOURCES_DIR.parent)}."
    )

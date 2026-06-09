"""Load the Standard Cross-Cultural Sample (SCCS) — Murdock 186 societies.

The SCCS is a curated sample of 186 pre-industrial societies designed for
cross-cultural comparison. We pull a minimal table (society id, name,
coordinates, language family, subsistence economy) from the D-PLACE
dataset (CC-BY-4.0).

The SCCS data is *not* fed into the GP — modern affinity/x_score vectors
are still country-level. Instead, SCCS societies are matched to GeoEPR
ethnic groups via :mod:`apps.basis_builder.ethnic_crosswalk` and exposed
as metadata on each ethnic sample point. The visualisation layer can
then offer tooltips like "Group: Yorùbá / SCCS society: Nupe (West
Africa, agricultural)".

Source: https://github.com/D-PLACE/dplace-data/blob/master/datasets/SCCS/societies.csv
"""
from __future__ import annotations

import csv
import io
import json
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path

from apps.basis_builder.paths import DATA_SOURCES_DIR

SCCS_REMOTE_URL: str = (
    "https://raw.githubusercontent.com/D-PLACE/dplace-data/master/"
    "datasets/SCCS/societies.csv"
)
SCCS_CACHE_DIR = DATA_SOURCES_DIR / "sccs"
SCCS_LOCAL_CSV_PATH = SCCS_CACHE_DIR / "societies.csv"
SCCS_NORMALISED_JSON_PATH = SCCS_CACHE_DIR / "sccs_societies_normalised.json"


@dataclass(frozen=True)
class SccsSociety:
    sccs_society_id: str
    sccs_society_name: str
    glottocode: str | None
    latitude_deg: float | None
    longitude_deg: float | None
    region: str | None


def download_sccs(force: bool = False) -> Path:
    """Fetch the D-PLACE SCCS societies CSV; skip if already cached."""
    SCCS_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if SCCS_LOCAL_CSV_PATH.exists() and not force:
        return SCCS_LOCAL_CSV_PATH
    try:
        with urllib.request.urlopen(SCCS_REMOTE_URL, timeout=60) as response:
            SCCS_LOCAL_CSV_PATH.write_bytes(response.read())
    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Failed to download SCCS societies CSV from {SCCS_REMOTE_URL}: {error}"
        ) from error
    return SCCS_LOCAL_CSV_PATH


def _read_sccs_csv(csv_path: Path) -> list[SccsSociety]:
    csv_content = csv_path.read_text(encoding="utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(csv_content))
    societies: list[SccsSociety] = []
    for row in reader:
        latitude_value = row.get("Lat") or row.get("Latitude") or row.get("lat")
        longitude_value = row.get("Lon") or row.get("Longitude") or row.get("lon")
        societies.append(
            SccsSociety(
                sccs_society_id=str(row.get("id") or row.get("ID") or row.get("xd_id") or "").strip(),
                sccs_society_name=str(
                    row.get("pref_name_for_society")
                    or row.get("Name")
                    or row.get("name")
                    or ""
                ).strip(),
                glottocode=(str(row.get("glottocode") or "").strip() or None),
                latitude_deg=(
                    float(latitude_value) if latitude_value not in (None, "") else None
                ),
                longitude_deg=(
                    float(longitude_value) if longitude_value not in (None, "") else None
                ),
                region=(str(row.get("region") or "").strip() or None),
            )
        )
    return [society for society in societies if society.sccs_society_id]


def load_sccs_societies(download_if_missing: bool = True) -> list[SccsSociety]:
    """Return the SCCS societies, downloading + caching the CSV if needed."""
    if not SCCS_LOCAL_CSV_PATH.exists() and download_if_missing:
        download_sccs()
    if not SCCS_LOCAL_CSV_PATH.exists():
        raise FileNotFoundError(
            f"SCCS CSV not found at {SCCS_LOCAL_CSV_PATH}; run with download_if_missing=True."
        )
    return _read_sccs_csv(SCCS_LOCAL_CSV_PATH)


def write_normalised_json(societies: list[SccsSociety]) -> Path:
    """Persist a normalised JSON sidecar for downstream crosswalk use."""
    SCCS_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "schema": "sccs_societies_normalised.schema.json",
            "source": SCCS_REMOTE_URL,
            "license": "CC-BY-4.0 (D-PLACE)",
            "n_societies": len(societies),
        },
        "societies": [asdict(society) for society in societies],
    }
    SCCS_NORMALISED_JSON_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False)
    )
    return SCCS_NORMALISED_JSON_PATH


if __name__ == "__main__":
    download_sccs()
    societies = load_sccs_societies(download_if_missing=False)
    output_path = write_normalised_json(societies)
    print(f"Wrote {output_path.name} with {len(societies)} SCCS societies.")

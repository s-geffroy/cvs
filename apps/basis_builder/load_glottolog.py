"""Load a Glottolog languoids subset — minimal columns for crosswalk.

We only require a tabular projection of languoids with::

    id, name, level (language|dialect|family), family_id, macroarea,
    latitude, longitude

Source: https://github.com/glottolog/glottolog-cldf v5.0
(Glottolog 5.0 languoid table, CC-BY-4.0).
"""
from __future__ import annotations

import csv
import io
import json
import urllib.error
import urllib.request
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path

from apps.basis_builder.paths import DATA_SOURCES_DIR

GLOTTOLOG_REMOTE_URL: str = (
    "https://raw.githubusercontent.com/glottolog/glottolog-cldf/v5.0/"
    "cldf/languages.csv"
)
GLOTTOLOG_CACHE_DIR = DATA_SOURCES_DIR / "glottolog"
GLOTTOLOG_LOCAL_CSV_PATH = GLOTTOLOG_CACHE_DIR / "languages.csv"
GLOTTOLOG_NORMALISED_JSON_PATH = (
    GLOTTOLOG_CACHE_DIR / "glottolog_languoids_normalised.json"
)


@dataclass(frozen=True)
class GlottologLanguoid:
    glottocode: str
    name: str
    level: str
    family_glottocode: str | None
    macroarea: str | None
    latitude_deg: float | None
    longitude_deg: float | None


def download_glottolog(force: bool = False) -> Path:
    """Fetch the Glottolog CLDF languages CSV into the local cache."""
    GLOTTOLOG_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if GLOTTOLOG_LOCAL_CSV_PATH.exists() and not force:
        return GLOTTOLOG_LOCAL_CSV_PATH
    try:
        with urllib.request.urlopen(GLOTTOLOG_REMOTE_URL, timeout=120) as response:
            GLOTTOLOG_LOCAL_CSV_PATH.write_bytes(response.read())
    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Failed to download Glottolog languages CSV from "
            f"{GLOTTOLOG_REMOTE_URL}: {error}"
        ) from error
    return GLOTTOLOG_LOCAL_CSV_PATH


def _extract_languoid_csv_text(zip_or_csv_path: Path) -> str:
    """Read CSV text from a plain CSV or, when given a ZIP, the first matching member."""
    if zipfile.is_zipfile(zip_or_csv_path):
        with zipfile.ZipFile(zip_or_csv_path) as archive:
            candidate_names = [
                name for name in archive.namelist() if name.endswith(".csv")
            ]
            if not candidate_names:
                raise RuntimeError(
                    f"No CSV inside Glottolog archive {zip_or_csv_path}; "
                    f"got {archive.namelist()}"
                )
            with archive.open(candidate_names[0]) as handle:
                return handle.read().decode("utf-8", errors="replace")
    return zip_or_csv_path.read_text(encoding="utf-8", errors="replace")


def _row_to_languoid(row: dict[str, str]) -> GlottologLanguoid | None:
    # CLDF ``languages.csv`` columns: ID, Name, Macroarea, Latitude, Longitude,
    # Glottocode, ISO639P3code, Family_ID, Parent_ID, Level, etc.
    glottocode_value = (
        row.get("Glottocode")
        or row.get("ID")
        or row.get("id")
        or row.get("glottocode")
        or ""
    )
    if not glottocode_value:
        return None
    latitude_value = (
        row.get("Latitude") or row.get("latitude") or row.get("Lat") or ""
    )
    longitude_value = (
        row.get("Longitude") or row.get("longitude") or row.get("Lon") or ""
    )
    family_value = (
        row.get("Family_ID")
        or row.get("family_id")
        or row.get("Family")
        or row.get("family")
        or ""
    )
    level_value = (row.get("Level") or row.get("level") or "").strip()
    return GlottologLanguoid(
        glottocode=glottocode_value.strip(),
        name=(row.get("Name") or row.get("name") or "").strip(),
        level=level_value.lower(),
        family_glottocode=(family_value.strip() or None),
        macroarea=(row.get("Macroarea") or row.get("macroarea") or None) or None,
        latitude_deg=(
            float(latitude_value) if latitude_value not in ("",) else None
        ),
        longitude_deg=(
            float(longitude_value) if longitude_value not in ("",) else None
        ),
    )


def load_glottolog_languoids(
    download_if_missing: bool = True,
    keep_levels: tuple[str, ...] = ("language", "family"),
) -> list[GlottologLanguoid]:
    if not GLOTTOLOG_LOCAL_CSV_PATH.exists() and download_if_missing:
        download_glottolog()
    if not GLOTTOLOG_LOCAL_CSV_PATH.exists():
        raise FileNotFoundError(
            f"Glottolog CSV missing at {GLOTTOLOG_LOCAL_CSV_PATH}; "
            "run with download_if_missing=True."
        )
    csv_text = _extract_languoid_csv_text(GLOTTOLOG_LOCAL_CSV_PATH)
    reader = csv.DictReader(io.StringIO(csv_text))
    languoids: list[GlottologLanguoid] = []
    for row in reader:
        languoid = _row_to_languoid(row)
        if languoid is None:
            continue
        if (
            keep_levels
            and languoid.level
            and languoid.level not in keep_levels
        ):
            continue
        languoids.append(languoid)
    return languoids


def write_normalised_json(languoids: list[GlottologLanguoid]) -> Path:
    GLOTTOLOG_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "schema": "glottolog_languoids_normalised.schema.json",
            "source": GLOTTOLOG_REMOTE_URL,
            "license": "CC-BY-4.0 (Glottolog)",
            "n_languoids": len(languoids),
        },
        "languoids": [asdict(languoid) for languoid in languoids],
    }
    GLOTTOLOG_NORMALISED_JSON_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False)
    )
    return GLOTTOLOG_NORMALISED_JSON_PATH


if __name__ == "__main__":
    download_glottolog()
    languoids = load_glottolog_languoids(download_if_missing=False)
    write_normalised_json(languoids)
    print(f"Wrote {len(languoids)} Glottolog languoids.")

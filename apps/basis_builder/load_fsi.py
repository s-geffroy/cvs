"""Load Fund For Peace Fragile States Index (total score)."""
from __future__ import annotations

import json
from dataclasses import dataclass

from .paths import DATA_SOURCES_DIR

FSI_TOTAL_PATH = DATA_SOURCES_DIR / "fsi" / "fragility_states_index_2024.json"


@dataclass(frozen=True)
class FSIProfile:
    iso3: str
    total_score: float  # 0 = stable, 120 = alert


def load_fsi() -> dict[str, FSIProfile]:
    payload = json.loads(FSI_TOTAL_PATH.read_text())
    profiles: dict[str, FSIProfile] = {}
    for entry in payload["values"]:
        iso3 = entry["iso3"]
        profiles[iso3] = FSIProfile(iso3=iso3, total_score=float(entry["value"]))
    return profiles

"""Load World Bank Worldwide Governance Indicators (rule of law z-score)."""
from __future__ import annotations

import json
from dataclasses import dataclass

from .paths import DATA_SOURCES_DIR

WGI_RULE_OF_LAW_PATH = DATA_SOURCES_DIR / "wgi" / "rule_of_law_2022.json"


@dataclass(frozen=True)
class WGIProfile:
    iso3: str
    rule_of_law: float  # z-score in [-2.5, +2.5]


def load_wgi() -> dict[str, WGIProfile]:
    payload = json.loads(WGI_RULE_OF_LAW_PATH.read_text())
    profiles: dict[str, WGIProfile] = {}
    for entry in payload["values"]:
        iso3 = entry["iso3"]
        profiles[iso3] = WGIProfile(iso3=iso3, rule_of_law=float(entry["value"]))
    return profiles

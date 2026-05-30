"""Load Hofstede 6D dimension scores per country."""
from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np

from .paths import HOFSTEDE_DIMENSIONS_PATH

HOFSTEDE_DIMENSION_ORDER: tuple[str, ...] = ("pdi", "idv", "mas", "uai", "lto", "ivr")


@dataclass(frozen=True)
class HofstedeProfile:
    iso3: str
    values: np.ndarray  # shape (6,), missing dims as NaN
    coverage: str  # "present" | "imputed" | "missing"


def load_hofstede() -> dict[str, HofstedeProfile]:
    """Return a mapping iso3 -> HofstedeProfile, with NaN for missing dimensions."""
    payload = json.loads(HOFSTEDE_DIMENSIONS_PATH.read_text())
    profiles: dict[str, HofstedeProfile] = {}
    for entry in payload["countries"]:
        iso3 = entry["iso3"]
        values = np.array(
            [
                entry.get(dim) if entry.get(dim) is not None else np.nan
                for dim in HOFSTEDE_DIMENSION_ORDER
            ],
            dtype=float,
        )
        coverage = "missing" if np.all(np.isnan(values)) else (
            "imputed" if np.any(np.isnan(values)) else "present"
        )
        profiles[iso3] = HofstedeProfile(iso3=iso3, values=values, coverage=coverage)
    return profiles

"""Load Pew Research religious composition per country (full 7-religion breakdown).

Reads ``data_sources/pew/religious_composition_full_2020.json`` extracted by
``_pew_extraction.py`` from the Pew 2020 dataset (percentages worksheet).
Each profile carries the share of population in each of the seven Pew
religious categories:

- Christians, Muslims, Hindus, Buddhists, Jews, religiously Unaffiliated,
  Other religions

Coverage: 182/193 UN member states; the 11 missing are micro-states (AND,
ATG, DMA, KNA, LIE, MCO, MHL, NRU, PLW, SMR, TUV) that Pew does not publish
country-level estimates for. These states fall back on UNDP HDR + UN voting
+ V-Dem signals in the cascade and are not penalised.

``PEW_RELIGION_FIELDS`` lists the seven proportions in canonical order so
calibration models can compose feature vectors deterministically.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from .paths import DATA_SOURCES_DIR

PEW_FULL_PATH = DATA_SOURCES_DIR / "pew" / "religious_composition_full_2020.json"

PEW_RELIGION_FIELDS: tuple[str, ...] = (
    "christians_pct",
    "muslims_pct",
    "hindus_pct",
    "buddhists_pct",
    "jews_pct",
    "unaffiliated_pct",
    "other_religions_pct",
)


@dataclass(frozen=True)
class PewProfile:
    iso3: str
    christians: float  # all proportions in [0, 1]
    muslims: float
    hindus: float
    buddhists: float
    jews: float
    unaffiliated: float
    other_religions: float

    @property
    def dominant_group(self) -> str:
        """Return the religion with the largest share, for backwards-compat labels."""
        candidates = [
            ("Christian", self.christians),
            ("Muslim", self.muslims),
            ("Hindu", self.hindus),
            ("Buddhist", self.buddhists),
            ("Jewish", self.jews),
            ("Unaffiliated", self.unaffiliated),
            ("Other", self.other_religions),
        ]
        return max(candidates, key=lambda pair: pair[1])[0]

    @property
    def dominant_share_pct(self) -> float:
        """Return the dominant religion's share in percent (0-100)."""
        return 100.0 * max(
            self.christians,
            self.muslims,
            self.hindus,
            self.buddhists,
            self.jews,
            self.unaffiliated,
            self.other_religions,
        )


# Backwards-compat constant: previously listed the dominant-group labels.
PEW_DOMINANT_GROUPS: tuple[str, ...] = (
    "Christian",
    "Muslim",
    "Hindu",
    "Buddhist",
    "Jewish",
    "Unaffiliated",
    "Other",
)


def load_pew() -> dict[str, PewProfile]:
    payload = json.loads(PEW_FULL_PATH.read_text())
    profiles: dict[str, PewProfile] = {}
    for entry in payload["values"]:
        iso3 = entry["iso3"]
        profiles[iso3] = PewProfile(
            iso3=iso3,
            christians=float(entry["christians_pct"]) / 100.0,
            muslims=float(entry["muslims_pct"]) / 100.0,
            hindus=float(entry["hindus_pct"]) / 100.0,
            buddhists=float(entry["buddhists_pct"]) / 100.0,
            jews=float(entry["jews_pct"]) / 100.0,
            unaffiliated=float(entry["unaffiliated_pct"]) / 100.0,
            other_religions=float(entry["other_religions_pct"]) / 100.0,
        )
    return profiles

"""Load V-Dem Varieties of Democracy indicators (latest year per state).

Source: ``data_sources/vdem/vdem_latest_year.json``, extracted from the
``vdem.RData`` bundle of the official R package ``vdeminstitute/vdemdata``
(CC-BY 4.0). The full dataset has 4618 columns × 28 092 country-year rows;
we keep only 12 high-level indices that have direct interpretive analogues
in the Hofstede 6D space and the Inglehart-Welzel axes, and only the latest
available year per ISO3.

Indices retained (range [0, 1] except where noted):

- ``libdem``: Liberal democracy — checks on the executive, civil liberties
- ``partipdem``: Participatory democracy
- ``delibdem``: Deliberative democracy
- ``egaldem``: Egalitarian democracy
- ``gender``: Women political empowerment
- ``corr``: Political corruption (0 = clean, 1 = corrupt) — sign-inverted
  relative to others
- ``transparent_laws``: Transparency and predictability of laws
- ``rule_of_law``: Equality before the law + individual liberty (rich
  V-Dem index, distinct from WGI Rule of Law)
- ``civlib``: Civil liberties
- ``priv_civlib``: Private civil liberties
- ``relig_freedom``: Freedom of religion
- ``equal_access``: Equal access to power

Coverage: 172/193 UN member states. States missing from V-Dem are the
micro-states without polity-tracking research focus (Andorra, Monaco, San
Marino, several Pacific states) — the cascade falls back on UNDP HDR
indicators for those, which already cover ~190 UN members.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from .paths import DATA_SOURCES_DIR

VDEM_PATH = DATA_SOURCES_DIR / "vdem" / "vdem_latest_year.json"


@dataclass(frozen=True)
class VDemProfile:
    iso3: str
    year: int
    libdem: float | None
    partipdem: float | None
    delibdem: float | None
    egaldem: float | None
    gender_empowerment: float | None
    corruption: float | None
    transparent_laws: float | None
    rule_of_law: float | None
    civil_liberties: float | None
    private_civil_liberties: float | None
    religious_freedom: float | None
    equal_access_power: float | None


def _coerce(raw: float | None) -> float | None:
    if raw is None:
        return None
    return float(raw)


def load_vdem() -> dict[str, VDemProfile]:
    payload = json.loads(VDEM_PATH.read_text())
    profiles: dict[str, VDemProfile] = {}
    for entry in payload["values"]:
        iso3 = entry["iso3"]
        profiles[iso3] = VDemProfile(
            iso3=iso3,
            year=int(entry["year"]),
            libdem=_coerce(entry.get("v2x_libdem")),
            partipdem=_coerce(entry.get("v2x_partipdem")),
            delibdem=_coerce(entry.get("v2x_delibdem")),
            egaldem=_coerce(entry.get("v2x_egaldem")),
            gender_empowerment=_coerce(entry.get("v2x_gender")),
            corruption=_coerce(entry.get("v2x_corr")),
            transparent_laws=_coerce(entry.get("v2cltrnslw")),
            rule_of_law=_coerce(entry.get("v2xcl_rol")),
            civil_liberties=_coerce(entry.get("v2x_civlib")),
            private_civil_liberties=_coerce(entry.get("v2x_clpriv")),
            religious_freedom=_coerce(entry.get("v2clrelig")),
            equal_access_power=_coerce(entry.get("v2xeg_eqaccess")),
        )
    return profiles

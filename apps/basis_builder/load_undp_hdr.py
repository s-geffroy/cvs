"""Load UNDP Human Development Report composite indices (2023 cross-section).

Source: `data_sources/undp/hdr_2023.json`, extracted from the official UNDP
2025 HDR release covering 1990-2023 (we keep only the latest year). Indicators:

- `hdi`: Human Development Index (0-1)
- `gii`: Gender Inequality Index (0-1, 0 = perfect equality)
- `gnipc`: Gross National Income per capita (2017 PPP USD)
- `le`: Life expectancy at birth (years)
- `mys`: Mean years of schooling (adults 25+)
- `eys`: Expected years of schooling (children)
- `phdi`: Planetary pressures-adjusted HDI

Coverage: 193/193 UN member states for HDI; 172/193 for GII; 191/193 for
mean/expected years of schooling. Far broader than Hofstede (63) — this is
the source that lifts the `imputed_*` tier from "scaffolding" to "actually
useful for hundreds of states".
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from .paths import DATA_SOURCES_DIR

UNDP_HDR_PATH = DATA_SOURCES_DIR / "undp" / "hdr_2023.json"


@dataclass(frozen=True)
class UNDPProfile:
    iso3: str
    hdi: float | None
    gii: float | None
    gnipc: float | None
    life_expectancy: float | None
    mean_years_schooling: float | None
    expected_years_schooling: float | None
    planetary_hdi: float | None


def _coerce_optional_float(raw: float | None) -> float | None:
    if raw is None:
        return None
    return float(raw)


def load_undp_hdr() -> dict[str, UNDPProfile]:
    payload = json.loads(UNDP_HDR_PATH.read_text())
    profiles: dict[str, UNDPProfile] = {}
    for entry in payload["values"]:
        iso3 = entry["iso3"]
        profiles[iso3] = UNDPProfile(
            iso3=iso3,
            hdi=_coerce_optional_float(entry.get("hdi_2023")),
            gii=_coerce_optional_float(entry.get("gii_2023")),
            gnipc=_coerce_optional_float(entry.get("gnipc_2023")),
            life_expectancy=_coerce_optional_float(entry.get("le_2023")),
            mean_years_schooling=_coerce_optional_float(entry.get("mys_2023")),
            expected_years_schooling=_coerce_optional_float(entry.get("eys_2023")),
            planetary_hdi=_coerce_optional_float(entry.get("phdi_2023")),
        )
    return profiles

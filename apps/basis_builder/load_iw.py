"""Load Inglehart-Welzel wave 7 cultural map coordinates."""
from __future__ import annotations

import json
from dataclasses import dataclass

from .paths import IW_CULTURAL_MAP_PATH


@dataclass(frozen=True)
class IWCoordinate:
    iso3: str
    ts: float
    se: float
    ts_ci: float
    se_ci: float
    n: int | None
    wave: int | None


def load_inglehart_welzel() -> dict[str, IWCoordinate]:
    """Return a mapping iso3 -> IWCoordinate for all WVS-covered countries."""
    payload = json.loads(IW_CULTURAL_MAP_PATH.read_text())
    coords: dict[str, IWCoordinate] = {}
    for entry in payload["countries"]:
        iso3 = entry["iso3"]
        coords[iso3] = IWCoordinate(
            iso3=iso3,
            ts=float(entry["ts"]),
            se=float(entry["se"]),
            ts_ci=float(entry.get("ts_ci", 0.15)),
            se_ci=float(entry.get("se_ci", 0.15)),
            n=entry.get("n"),
            wave=entry.get("wave"),
        )
    return coords

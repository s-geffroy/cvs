"""Load Inglehart-Welzel cultural map coordinates (waves 5-7 pooled when available).

If ``data_sources/inglehart_welzel/cultural_map_pooled.json`` exists (produced
by ``_wvs_extraction.py`` from the WVS Time-Series 1981-2022), it is used as
the source — it includes both the 62 official wave-7 countries and ~60
additional countries with coordinates predicted from raw WVS items via ridge
regression. Each entry carries a ``source`` field so the projector can
distinguish the official observations (``wvs_wave7_official``) from the
WVS-item-derived predictions (``wvs_wave{N}_predicted_from_items``).

Otherwise the loader falls back on the original ``cultural_map_wave7.json``
(62 countries, all official).
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from .paths import DATA_SOURCES_DIR, IW_CULTURAL_MAP_PATH

IW_CULTURAL_MAP_POOLED_PATH = (
    DATA_SOURCES_DIR / "inglehart_welzel" / "cultural_map_pooled.json"
)


@dataclass(frozen=True)
class IWCoordinate:
    iso3: str
    ts: float
    se: float
    ts_ci: float
    se_ci: float
    n: int | None
    wave: int | None
    source: str  # "wvs_wave7_official" | "wvs_wave{N}_predicted_from_items"


def load_inglehart_welzel() -> dict[str, IWCoordinate]:
    """Return a mapping iso3 -> IWCoordinate using the pooled file when present."""
    if IW_CULTURAL_MAP_POOLED_PATH.exists():
        payload = json.loads(IW_CULTURAL_MAP_POOLED_PATH.read_text())
    else:
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
            source=str(entry.get("source", "wvs_wave7_official")),
        )
    return coords


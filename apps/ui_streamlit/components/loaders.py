"""Cached loaders for taxonomy, centroids, state coordinates, second moments."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from apps.basis_builder.paths import (
    CIVILIZATION_CENTROIDS_PATH,
    MACRO_CIVILIZATIONS_V2_PATH,
    STATE_COORDINATES_PATH,
    STATE_MOMENTS_PATH,
)


def _safe_load(target_path: Path) -> dict[str, Any] | None:
    if not target_path.exists():
        return None
    return json.loads(target_path.read_text())


@st.cache_data(show_spinner=False)
def load_taxonomy_v2() -> dict[str, Any]:
    data = _safe_load(MACRO_CIVILIZATIONS_V2_PATH)
    if data is None:
        raise FileNotFoundError(
            "macro_civilizations.v2.json missing — run `civvec basis build` first."
        )
    return data


@st.cache_data(show_spinner=False)
def load_centroids() -> dict[str, Any] | None:
    return _safe_load(CIVILIZATION_CENTROIDS_PATH)


@st.cache_data(show_spinner=False)
def load_state_coordinates() -> dict[str, Any] | None:
    return _safe_load(STATE_COORDINATES_PATH)


@st.cache_data(show_spinner=False)
def load_state_moments() -> dict[str, Any] | None:
    return _safe_load(STATE_MOMENTS_PATH)

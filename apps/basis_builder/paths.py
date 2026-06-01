"""Filesystem locations for canonical data and computed basis artefacts."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

DATA_SOURCES_DIR = REPO_ROOT / "data_sources"
IW_CULTURAL_MAP_PATH = DATA_SOURCES_DIR / "inglehart_welzel" / "cultural_map_wave7.json"
HOFSTEDE_DIMENSIONS_PATH = DATA_SOURCES_DIR / "hofstede" / "dimensions_v2015.json"

TAXONOMIES_DIR = REPO_ROOT / "taxonomies"
MACRO_CIVILIZATIONS_V2_PATH = TAXONOMIES_DIR / "macro_civilizations.v2.json"

BASIS_DIR = REPO_ROOT / "packages" / "civvec_core" / "basis"
B_VIZ_PATH = BASIS_DIR / "B_viz.json"
B_SCORE_PATH = BASIS_DIR / "B_score.json"
CIVILIZATION_CENTROIDS_PATH = BASIS_DIR / "civilization_centroids.json"
STATE_COORDINATES_PATH = BASIS_DIR / "state_coordinates.json"
STATE_MOMENTS_PATH = BASIS_DIR / "state_moments.json"

SCHEMAS_DIR = REPO_ROOT / "schemas"

OUTPUTS_DIR = REPO_ROOT / "outputs"
DISTANCES_DIR = OUTPUTS_DIR / "distances"
EMPIRICAL_DIR = OUTPUTS_DIR / "empirical"

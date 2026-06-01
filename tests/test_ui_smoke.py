"""UI smoke test: ensure pages import cleanly and components expose key constants."""
from __future__ import annotations

import importlib

import pytest

pytest.importorskip("streamlit", reason="Streamlit not installed in this image (e.g. site builder).")
pytest.importorskip("plotly", reason="Plotly not installed in this image (e.g. site builder).")


def test_ethics_banner_constants_present() -> None:
    module = importlib.import_module("apps.ui_streamlit.components.ethics_banner")
    assert "inférée" not in module.ETHICAL_WARNING_FR  # spelling guard
    assert "inferred" in module.ETHICAL_WARNING_EN
    assert "individuals" in module.ETHICAL_WARNING_EN


def test_loaders_module_imports() -> None:
    module = importlib.import_module("apps.ui_streamlit.components.loaders")
    assert hasattr(module, "load_taxonomy_v2")
    assert hasattr(module, "load_centroids")


def test_charts_module_imports() -> None:
    module = importlib.import_module("apps.ui_streamlit.components.charts")
    assert hasattr(module, "scatter_viz")
    assert hasattr(module, "radar_score")
    assert hasattr(module, "moment_heatmap")

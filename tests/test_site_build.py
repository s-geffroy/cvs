"""Phase 1b site build invariants.

These tests render the Phase 1b pages (templates → site_src/docs) and then
build the static site via mkdocs in strict mode. They assert the ethics
warning appears on every page, that no GADM geometry is published, and that
the methodology + taxonomy + sources + schemas indexes are present.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from apps.basis_builder.paths import REPO_ROOT
from apps.site_builder.guards import (
    ALLOWED_GEOMETRY_SOURCES,
    ETHICAL_WARNING_FR,
    scan_directory_for_gadm,
)

pytest.importorskip("mkdocs", reason="mkdocs not installed in this image (e.g. UI builder).")

SITE_SRC_DIR = REPO_ROOT / "site_src"
if not SITE_SRC_DIR.exists():
    pytest.skip("site_src/ not bundled in this image", allow_module_level=True)

from apps.site_builder.builder import render_all  # noqa: E402

DIST_DIR = REPO_ROOT / "dist"


@pytest.fixture(scope="module")
def built_dist() -> Path:
    if DIST_DIR.exists():
        for entry in DIST_DIR.iterdir():
            if entry.is_dir():
                shutil.rmtree(entry)
            else:
                entry.unlink()
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    render_all()
    result = subprocess.run(
        ["mkdocs", "build", "--strict", "-d", str(DIST_DIR)],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(
            f"mkdocs build --strict failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return DIST_DIR


def test_mkdocs_strict_build(built_dist: Path) -> None:
    assert (built_dist / "index.html").exists()


def test_ethics_warning_on_landing_page(built_dist: Path) -> None:
    landing_html = (built_dist / "index.html").read_text()
    assert "ne doit pas être utilisé" in landing_html


def test_ethics_warning_on_every_html_page(built_dist: Path) -> None:
    missing: list[str] = []
    for html_path in built_dist.rglob("*.html"):
        body = html_path.read_text()
        if "ne doit pas être utilisé" not in body:
            missing.append(str(html_path.relative_to(built_dist)))
    assert not missing, f"Pages missing ethics warning: {missing}"


def test_taxonomy_civilization_pages_present(built_dist: Path) -> None:
    expected_ids = [
        "western", "orthodox", "islamic", "sinic", "hindic",
        "japanese", "buddhist", "latin_american", "african",
        "indigenous", "oceanian",
    ]
    for civ_id in expected_ids:
        page_path = built_dist / "taxonomy" / "civilizations" / civ_id / "index.html"
        assert page_path.exists(), f"missing civilization page: {civ_id}"


def test_methodology_pages_complete(built_dist: Path) -> None:
    expected_prefixes = [f"{i:02d}_" for i in range(11)]
    methodology_dir = built_dist / "methodology"
    rendered_files = {p.parent.name for p in methodology_dir.glob("*/index.html")}
    for prefix in expected_prefixes:
        match = any(name.startswith(prefix) for name in rendered_files)
        assert match, f"missing methodology page starting with {prefix}; got {sorted(rendered_files)}"


def test_sources_index_renders_bibliography(built_dist: Path) -> None:
    sources_html = (built_dist / "sources" / "index.html").read_text()
    assert "huntington_1996" in sources_html
    assert "hofstede_2010" in sources_html
    assert "wvs_wave7_2022" in sources_html


def test_schemas_index_lists_all_schemas(built_dist: Path) -> None:
    schemas_html = (built_dist / "schemas" / "index.html").read_text()
    for schema_name in (
        "macro_civilizations.schema.json",
        "state_tension.schema.json",
        "distance_matrix.schema.json",
        "adm1_profile.v2.schema.json",
    ):
        assert schema_name in schemas_html


def test_adm1_policy_published(built_dist: Path) -> None:
    adm1_html = (built_dist / "adm1_policy" / "index.html").read_text()
    assert "prepared_not_active" in adm1_html or "préparée" in adm1_html


def test_no_gadm_geometry_in_published_geojson(built_dist: Path) -> None:
    offenders = scan_directory_for_gadm(built_dist)
    assert not offenders, f"GADM geometry found in: {offenders}"


def test_only_allowed_geometry_sources_constant() -> None:
    assert ALLOWED_GEOMETRY_SOURCES == frozenset({"Natural Earth", "geoBoundaries"})


def test_ethical_warning_fr_includes_individuals_clause() -> None:
    assert "individus réels" in ETHICAL_WARNING_FR

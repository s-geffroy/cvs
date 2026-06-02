"""Invariants for the standalone 'vulgarisation' mini-site.

These tests verify that:
- The hub and the three stratified levels are present.
- The sticky ethics warning appears on every HTML page.
- The mini-site does not bleed Material theme classes.
- Cross-links back to the main MkDocs site exist on at least one Level-3 page.
- Assets are copied through.
- mkdocs.yml excludes the subtree from the nav (via `not_in_nav`) and adds an
  external nav entry to it.

The fixture reuses the same end-to-end build path as `test_site_build.py`.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from apps.basis_builder.paths import REPO_ROOT

pytest.importorskip("mkdocs", reason="mkdocs not installed in this image (e.g. UI builder).")

SITE_SRC_DIR = REPO_ROOT / "site_src"
if not SITE_SRC_DIR.exists():
    pytest.skip("site_src/ not bundled in this image", allow_module_level=True)

from apps.site_builder.builder import render_all  # noqa: E402

DIST_DIR = REPO_ROOT / "dist"
VULG_DIR = DIST_DIR / "vulgarisation"
MKDOCS_YML = REPO_ROOT / "mkdocs.yml"

ETHICS_TOKEN = "ne doit pas être utilisé"
STICKY_TOKEN = "ethics-sticky"


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
            "mkdocs build --strict failed:\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return DIST_DIR


def test_vulgarisation_hub_present(built_dist: Path) -> None:
    hub = built_dist / "vulgarisation" / "index.html"
    assert hub.exists(), "vulgarisation/index.html missing"
    body = hub.read_text(encoding="utf-8")
    assert "Niveau 1" in body
    assert "Niveau 2" in body
    assert "Niveau 3" in body


def test_vulgarisation_three_levels_present(built_dist: Path) -> None:
    expected = [
        "vulgarisation/niveau-1-citoyen/index.html",
        "vulgarisation/niveau-2-journaliste/index.html",
        "vulgarisation/niveau-3-etudiant-shs/index.html",
    ]
    missing = [path for path in expected if not (built_dist / path).exists()]
    assert not missing, f"Stratified-level indexes missing: {missing}"


def test_vulgarisation_ethics_sticky_on_every_html(built_dist: Path) -> None:
    missing_ethics: list[str] = []
    missing_sticky: list[str] = []
    for html_path in (built_dist / "vulgarisation").rglob("*.html"):
        body = html_path.read_text(encoding="utf-8")
        relative = str(html_path.relative_to(built_dist))
        if ETHICS_TOKEN not in body:
            missing_ethics.append(relative)
        if STICKY_TOKEN not in body:
            missing_sticky.append(relative)
    assert not missing_ethics, f"Missing ethics token: {missing_ethics}"
    assert not missing_sticky, f"Missing sticky class hook: {missing_sticky}"


def test_vulgarisation_no_material_theme_leakage(built_dist: Path) -> None:
    leaking = []
    for html_path in (built_dist / "vulgarisation").rglob("*.html"):
        body = html_path.read_text(encoding="utf-8")
        if "md-content" in body or "md-nav" in body or "md-header" in body:
            leaking.append(str(html_path.relative_to(built_dist)))
    assert not leaking, (
        f"Pages contain Material theme classes (md-*) — bleed: {leaking}"
    )


def test_vulgarisation_links_back_to_methodology(built_dist: Path) -> None:
    found = False
    for html_path in (built_dist / "vulgarisation" / "niveau-3-etudiant-shs").rglob("*.html"):
        body = html_path.read_text(encoding="utf-8")
        if "../../methodology/" in body or "../methodology/" in body:
            found = True
            break
    assert found, "No Level-3 page links back to methodology/"


def test_vulgarisation_footer_links_back_to_main_site(built_dist: Path) -> None:
    hub = built_dist / "vulgarisation" / "index.html"
    body = hub.read_text(encoding="utf-8")
    assert 'href="../states/"' in body
    assert 'href="../map/"' in body
    assert 'href="../ethics/"' in body


def test_vulgarisation_assets_present(built_dist: Path) -> None:
    assets_dir = built_dist / "vulgarisation" / "assets" / "css"
    assert (assets_dir / "vulgarisation.css").exists()
    assert (assets_dir / "reset.css").exists()


def test_vulgarisation_no_gadm_in_subtree(built_dist: Path) -> None:
    from apps.site_builder.guards import scan_directory_for_gadm

    offenders = scan_directory_for_gadm(built_dist / "vulgarisation")
    assert not offenders, f"GADM provenance leaked into vulgarisation/: {offenders}"


def test_mkdocs_yml_excludes_vulgarisation_from_nav() -> None:
    body = MKDOCS_YML.read_text(encoding="utf-8")
    assert "/vulgarisation/**" in body, "vulgarisation not excluded via not_in_nav"


def test_mkdocs_yml_has_external_nav_entry_to_vulgarisation() -> None:
    body = MKDOCS_YML.read_text(encoding="utf-8")
    assert "/cvs/vulgarisation/" in body, "no external nav entry pointing to /cvs/vulgarisation/"


def test_main_site_index_links_to_vulgarisation(built_dist: Path) -> None:
    home = (built_dist / "index.html").read_text(encoding="utf-8")
    assert "vulgarisation/index.html" in home or "vulgarisation/" in home, (
        "main site landing page does not link to the vulgarisation sub-site"
    )

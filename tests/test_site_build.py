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
        "state_moment.schema.json",
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


# ---------------------------------------------------------------------------
# Phase 2 invariants — states + map + basis + moments + distances.
# These tests only run when the basis artefacts (state_coordinates, moments,
# centroids) are available — they're produced by `civvec basis build`, which
# is always run before pytest in the container CMD.
# ---------------------------------------------------------------------------


def _phase2_artefact_paths_present() -> bool:
    from apps.basis_builder.paths import (
        B_SCORE_PATH,
        B_VIZ_PATH,
        CIVILIZATION_CENTROIDS_PATH,
        STATE_COORDINATES_PATH,
        STATE_MOMENTS_PATH,
    )

    return all(
        path.exists()
        for path in (
            B_VIZ_PATH,
            B_SCORE_PATH,
            CIVILIZATION_CENTROIDS_PATH,
            STATE_COORDINATES_PATH,
            STATE_MOMENTS_PATH,
        )
    )


def test_phase2_states_index_present(built_dist: Path) -> None:
    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    states_index_html = (built_dist / "states" / "index.html").read_text()
    assert "ne doit pas être utilisé" in states_index_html


def test_phase2_state_page_FRA_contains_x_viz_hofstede_and_second_moment(built_dist: Path) -> None:
    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    fra_html = (built_dist / "states" / "FRA" / "index.html").read_text()
    assert "x_viz" in fra_html
    assert "Power Distance" in fra_html
    assert "Second moment civilisationnel" in fra_html
    assert "FRA.profile.json" in fra_html


def test_phase2_state_data_assets_present(built_dist: Path) -> None:
    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    for relative_path in (
        "assets/data/state_coordinates.json",
        "assets/data/civilization_centroids.json",
        "assets/data/state_moments.json",
        "assets/data/state_distance_matrix.json",
        "assets/data/B_viz.json",
        "assets/data/B_score.json",
        "assets/data/global_state_baseline.geojson",
    ):
        assert (built_dist / relative_path).exists(), f"missing Phase 2 asset: {relative_path}"


def test_phase2_map_page_wires_maplibre_and_geojson(built_dist: Path) -> None:
    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    map_html = (built_dist / "map" / "index.html").read_text()
    assert 'id="civvec-map"' in map_html
    assert "maplibre-gl" in map_html
    assert "global_state_baseline.geojson" in map_html


def test_phase2_basis_page_loads_plotly_and_centroids(built_dist: Path) -> None:
    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    basis_html = (built_dist / "basis" / "index.html").read_text()
    assert 'id="civvec-basis-scatter"' in basis_html
    assert 'id="civvec-basis-radar"' in basis_html
    assert "plotly" in basis_html.lower()


def test_phase2_moments_page_present(built_dist: Path) -> None:
    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    moments_html = (built_dist / "moments" / "index.html").read_text()
    assert 'id="civvec-moments-heatmap"' in moments_html
    assert "anisotropie" in moments_html.lower()


def test_phase2_distances_page_present(built_dist: Path) -> None:
    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    distances_html = (built_dist / "distances" / "index.html").read_text()
    assert 'id="civvec-distances-heatmap"' in distances_html
    assert "d_hyb" in distances_html


def test_phase2_global_state_baseline_geojson_has_natural_earth_provenance(
    built_dist: Path,
) -> None:
    import json

    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    geojson_payload = json.loads(
        (built_dist / "assets" / "data" / "global_state_baseline.geojson").read_text()
    )
    provenance = geojson_payload["properties"]["geometry_provenance"]
    assert provenance["geometry_source"] == "Natural Earth"
    assert provenance["contains_gadm_geometry"] is False
    assert provenance["geometry_source"] in ALLOWED_GEOMETRY_SOURCES


def test_geojson_includes_full_natural_earth_coverage(built_dist: Path) -> None:
    import json

    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    geojson_payload = json.loads(
        (built_dist / "assets" / "data" / "global_state_baseline.geojson").read_text()
    )
    feature_count = geojson_payload["properties"]["feature_count"]
    iso3_set = {feature["properties"]["iso3"] for feature in geojson_payload["features"]}
    iso3_excluded = set(geojson_payload["properties"].get("iso3_excluded", []))
    assert feature_count >= 170, f"expected >=170 features, got {feature_count}"
    for required_iso3 in ("POL", "PAK", "ZAF", "EGY", "CHE", "PRT", "AUT"):
        assert required_iso3 in iso3_set, f"{required_iso3} should appear after de-filtering"
    assert "ATA" not in iso3_set, "Antarctica must be excluded"
    assert "ATA" in iso3_excluded


def test_state_coordinates_curated_membership(built_dist: Path) -> None:
    import json

    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    state_payload = json.loads(
        (built_dist / "assets" / "data" / "state_coordinates.json").read_text()
    )
    states_by_iso3 = {state["iso3"]: state for state in state_payload["states"]}
    expectations = {
        "DEU": "western",
        "ESP": "western",
        "SAU": "islamic",
        "MYS": "islamic",
        "JPN": "japanese",
        "USA": "western",
        "CHN": "sinic",
        "IND": "hindic",
    }
    for iso3, expected_civilization in expectations.items():
        assert iso3 in states_by_iso3, f"{iso3} missing from state_coordinates"
        assert states_by_iso3[iso3]["curated_civilization"] == expected_civilization, (
            f"{iso3}: expected curated={expected_civilization}, "
            f"got {states_by_iso3[iso3].get('curated_civilization')}"
        )


def test_state_coordinates_sub_clusters(built_dist: Path) -> None:
    import json

    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    state_payload = json.loads(
        (built_dist / "assets" / "data" / "state_coordinates.json").read_text()
    )
    states_by_iso3 = {state["iso3"]: state for state in state_payload["states"]}
    expectations = {
        "USA": "english_speaking",
        "DEU": "protestant_europe",
        "ESP": "catholic_europe",
        "MYS": "southeast_asian_islamic",
        "SAU": "arab_islamic",
    }
    for iso3, expected_sub_cluster in expectations.items():
        assert states_by_iso3[iso3]["sub_cluster_id"] == expected_sub_cluster, (
            f"{iso3}: expected sub_cluster={expected_sub_cluster}, "
            f"got {states_by_iso3[iso3].get('sub_cluster_id')}"
        )


def test_map_page_has_mode_toggle(built_dist: Path) -> None:
    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    map_html = (built_dist / "map" / "index.html").read_text()
    assert 'id="civvec-map-mode"' in map_html
    assert 'value="macro"' in map_html
    assert 'value="sub"' in map_html


def test_phase2_per_state_geojson_files_all_natural_earth(built_dist: Path) -> None:
    import json

    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    states_dir = built_dist / "assets" / "data" / "states"
    geojson_files = list(states_dir.glob("*.geojson"))
    assert geojson_files, "expected per-state GeoJSON files under assets/data/states/"
    for geojson_path in geojson_files:
        payload = json.loads(geojson_path.read_text())
        provenance = payload["properties"]["geometry_provenance"]
        assert provenance["geometry_source"] == "Natural Earth", geojson_path.name
        assert provenance["contains_gadm_geometry"] is False, geojson_path.name


def test_phase2_distance_matrix_is_symmetric_and_zero_diagonal(built_dist: Path) -> None:
    import json

    if not _phase2_artefact_paths_present():
        pytest.skip("Phase 2 artefacts not built — skipping")
    distance_payload = json.loads(
        (built_dist / "assets" / "data" / "state_distance_matrix.json").read_text()
    )
    iso3_order = distance_payload["iso3_order"]
    n_states = len(iso3_order)
    for metric_key, matrix in distance_payload["matrices"].items():
        for index in range(n_states):
            assert abs(matrix[index][index]) < 1e-9, f"{metric_key} diagonal not 0 at {iso3_order[index]}"
        for left in range(n_states):
            for right in range(left + 1, n_states):
                assert abs(matrix[left][right] - matrix[right][left]) < 1e-6, (
                    f"{metric_key} asymmetric at ({iso3_order[left]}, {iso3_order[right]})"
                )

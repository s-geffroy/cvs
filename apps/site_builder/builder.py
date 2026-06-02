"""Orchestrator: render Phase 1b + Phase 2 pages into site_src/docs/ so mkdocs can build dist/."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import numpy as np
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from apps.basis_builder.geometries import (
    NATURAL_EARTH_ADM0_PATH,
    NATURAL_EARTH_PINNED_COMMIT,
    extract_single_state_geojson,
    load_admin0_collection,
)
from apps.basis_builder.un_members import load_un_member_names_fr
from apps.basis_builder.paths import (
    B_SCORE_PATH,
    B_VIZ_PATH,
    CIVILIZATION_CENTROIDS_PATH,
    EMPIRICAL_DIR,
    REPO_ROOT,
    STATE_COORDINATES_PATH,
    STATE_MOMENTS_PATH,
)
from apps.site_builder.guards import ETHICAL_WARNING, ETHICAL_WARNING_FR
from apps.site_builder.loaders import (
    SOURCES_MD_PATH,
    iter_methodology_docs,
    iter_schemas,
    load_schema_title,
    load_sources_markdown,
    load_taxonomy_v2,
)

SITE_SRC_DIR = REPO_ROOT / "site_src"
SITE_DOCS_DIR = SITE_SRC_DIR / "docs"
TEMPLATES_DIR = SITE_SRC_DIR / "templates"
METHODOLOGY_OUT_DIR = SITE_DOCS_DIR / "methodology"
TAXONOMY_OUT_DIR = SITE_DOCS_DIR / "taxonomy"
CIVILIZATIONS_OUT_DIR = TAXONOMY_OUT_DIR / "civilizations"
SOURCES_OUT_DIR = SITE_DOCS_DIR / "sources"
SCHEMAS_OUT_DIR = SITE_DOCS_DIR / "schemas"
SCHEMAS_ASSETS_DIR = SITE_DOCS_DIR / "assets" / "schemas"

STATES_OUT_DIR = SITE_DOCS_DIR / "states"
MAP_OUT_DIR = SITE_DOCS_DIR / "map"
BASIS_OUT_DIR = SITE_DOCS_DIR / "basis"
MOMENTS_OUT_DIR = SITE_DOCS_DIR / "moments"
DISTANCES_OUT_DIR = SITE_DOCS_DIR / "distances"
DATA_ASSETS_DIR = SITE_DOCS_DIR / "assets" / "data"
DATA_STATES_DIR = DATA_ASSETS_DIR / "states"
DATA_EMPIRICAL_DIR = DATA_ASSETS_DIR / "empirical"

PHASE2_PINNED_MAPLIBRE_VERSION = "4.7.1"
PHASE2_PINNED_PLOTLY_VERSION = "2.35.2"

METHODOLOGY_TITLES = {
    "00": "Décisions du projet",
    "01": "Modèle conceptuel",
    "02": "Méthodologie source-only",
    "03": "Scope État (V1)",
    "04": "ADM1 préparé",
    "05": "Calibration du scoring",
    "06": "Outputs et stockage",
    "07": "Éthique de publication",
    "08": "Base civilisationnelle (B_doc + B_vec)",
    "09": "Second moment civilisationnel",
    "10": "Algèbre des distances",
    "11": "Critiques et réponses",
    "12": "Validation empirique externe",
    "13": "Analyse de sensibilité",
    "14": "Baseline non-supervisé",
    "15": "Glossaire",
}


def _jinja_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
    )


def _iso3_to_name_fr() -> dict[str, str]:
    """Charge la table ISO3 → nom court en français (193 États ONU)."""
    return load_un_member_names_fr()


def _format_state_label(iso3: str, name_fr_index: dict[str, str]) -> str:
    """Forme courte 'Nom (ISO3)' lorsque le nom français est connu."""
    name_fr = name_fr_index.get(iso3)
    return f"{name_fr} ({iso3})" if name_fr else iso3


def render_methodology() -> None:
    METHODOLOGY_OUT_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()
    methodology_docs_metadata: list[dict[str, str]] = []
    for source_path in iter_methodology_docs():
        target_path = METHODOLOGY_OUT_DIR / source_path.name
        target_path.write_text(source_path.read_text())
        number_prefix = source_path.stem.split("_", 1)[0]
        title = METHODOLOGY_TITLES.get(number_prefix, source_path.stem)
        methodology_docs_metadata.append(
            {
                "number": number_prefix,
                "title": title,
                "filename": source_path.name,
            }
        )
    index_template = env.get_template("methodology_index.md.j2")
    (METHODOLOGY_OUT_DIR / "index.md").write_text(
        index_template.render(
            ethical_warning_fr=ETHICAL_WARNING_FR,
            methodology_docs=methodology_docs_metadata,
        )
    )


def render_taxonomy() -> None:
    CIVILIZATIONS_OUT_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()
    taxonomy = load_taxonomy_v2()
    biblio_index = {entry["id"]: entry for entry in taxonomy["bibliography"]}
    iso3_to_name_fr = _iso3_to_name_fr()

    civilization_template = env.get_template("civilization_page.md.j2")
    for civ in taxonomy["civilizations"]:
        rendered = civilization_template.render(
            civ=civ,
            biblio_index=biblio_index,
            iso3_to_name_fr=iso3_to_name_fr,
            ethical_warning=ETHICAL_WARNING,
            ethical_warning_fr=ETHICAL_WARNING_FR,
        )
        (CIVILIZATIONS_OUT_DIR / f"{civ['id']}.md").write_text(rendered)

    index_template = env.get_template("taxonomy_index.md.j2")
    (TAXONOMY_OUT_DIR / "index.md").write_text(
        index_template.render(
            taxonomy=taxonomy,
            version_major=taxonomy["version"].split(".")[0] or "2",
            iso3_to_name_fr=iso3_to_name_fr,
            ethical_warning_fr=ETHICAL_WARNING_FR,
        )
    )


def render_sources() -> None:
    SOURCES_OUT_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()
    taxonomy = load_taxonomy_v2()
    sources_md_content = load_sources_markdown()
    sources_md_content = sources_md_content.replace(
        "(../docs/07_ethics_publication_policy.md)",
        "(../methodology/07_ethics_publication_policy.md)",
    )
    index_template = env.get_template("sources_index.md.j2")
    (SOURCES_OUT_DIR / "index.md").write_text(
        index_template.render(
            bibliography=taxonomy["bibliography"],
            sources_md_content=sources_md_content,
            ethical_warning_fr=ETHICAL_WARNING_FR,
        )
    )


def render_schemas() -> None:
    SCHEMAS_OUT_DIR.mkdir(parents=True, exist_ok=True)
    SCHEMAS_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()
    schemas_metadata: list[dict[str, str]] = []
    for schema_path in iter_schemas():
        destination = SCHEMAS_ASSETS_DIR / schema_path.name
        shutil.copyfile(schema_path, destination)
        schemas_metadata.append(
            {
                "name": schema_path.name,
                "title": load_schema_title(schema_path),
                "relative_url": f"../assets/schemas/{schema_path.name}",
            }
        )
    index_template = env.get_template("schemas_index.md.j2")
    (SCHEMAS_OUT_DIR / "index.md").write_text(
        index_template.render(
            schemas=schemas_metadata,
            ethical_warning_fr=ETHICAL_WARNING_FR,
        )
    )


def _load_phase2_artefacts() -> dict | None:
    """Return a bundle of artefacts needed by Phase 2; None if any are missing."""
    required_paths = [
        STATE_COORDINATES_PATH,
        CIVILIZATION_CENTROIDS_PATH,
        STATE_MOMENTS_PATH,
        B_VIZ_PATH,
        B_SCORE_PATH,
    ]
    if not all(path.exists() for path in required_paths):
        return None
    return {
        "state_coordinates": json.loads(STATE_COORDINATES_PATH.read_text()),
        "centroids": json.loads(CIVILIZATION_CENTROIDS_PATH.read_text()),
        "moments": json.loads(STATE_MOMENTS_PATH.read_text()),
        "b_viz": json.loads(B_VIZ_PATH.read_text()),
        "b_score": json.loads(B_SCORE_PATH.read_text()),
    }


def _civilization_label_index(centroids_payload: dict) -> dict[str, str]:
    taxonomy = load_taxonomy_v2()
    label_by_id = {civ["id"]: civ["label"] for civ in taxonomy["civilizations"]}
    return {
        entry["civilization_id"]: label_by_id.get(entry["civilization_id"], entry["civilization_id"])
        for entry in centroids_payload["centroids"]
    }


def _copy_basis_artefacts_to_data_assets(artefacts: dict) -> None:
    DATA_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_EMPIRICAL_DIR.mkdir(parents=True, exist_ok=True)
    iso3_to_name_fr = _iso3_to_name_fr()

    def _dump_with_name_fr(source_path: Path, target_name: str) -> None:
        payload = json.loads(source_path.read_text())
        payload.setdefault("_meta", {})
        payload["_meta"]["iso3_to_name_fr"] = iso3_to_name_fr
        (DATA_ASSETS_DIR / target_name).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2)
        )

    _dump_with_name_fr(STATE_COORDINATES_PATH, "state_coordinates.json")
    _dump_with_name_fr(STATE_MOMENTS_PATH, "state_moments.json")
    shutil.copyfile(CIVILIZATION_CENTROIDS_PATH, DATA_ASSETS_DIR / "civilization_centroids.json")
    shutil.copyfile(B_VIZ_PATH, DATA_ASSETS_DIR / "B_viz.json")
    shutil.copyfile(B_SCORE_PATH, DATA_ASSETS_DIR / "B_score.json")
    if NATURAL_EARTH_ADM0_PATH.exists():
        shutil.copyfile(NATURAL_EARTH_ADM0_PATH, DATA_ASSETS_DIR / "global_state_baseline.geojson")

    if EMPIRICAL_DIR.exists():
        for empirical_path in EMPIRICAL_DIR.glob("*.json"):
            shutil.copyfile(empirical_path, DATA_EMPIRICAL_DIR / empirical_path.name)


def _affinity_table(state_entry: dict, label_index: dict[str, str]) -> list[dict]:
    affinity = state_entry.get("affinity_vector") or {}
    rows = [
        {"civ_id": civ_id, "label": label_index.get(civ_id, civ_id), "weight": weight}
        for civ_id, weight in affinity.items()
    ]
    rows.sort(key=lambda row: row["weight"], reverse=True)
    return rows


def render_states(artefacts: dict) -> None:
    STATES_OUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_STATES_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()
    state_template = env.get_template("state_page.md.j2")
    states_index_template = env.get_template("states_index.md.j2")

    state_entries = artefacts["state_coordinates"]["states"]
    moments_by_iso3 = {entry["iso3"]: entry for entry in artefacts["moments"]["moments"]}
    label_index = _civilization_label_index(artefacts["centroids"])
    affinity_beta = artefacts["state_coordinates"]["_meta"]["affinity_beta"]
    iso3_to_name_fr = _iso3_to_name_fr()

    iso3_with_geometry: set[str] = set()
    if NATURAL_EARTH_ADM0_PATH.exists():
        admin0_collection = load_admin0_collection()
        iso3_with_geometry = {
            feature["properties"].get("iso3") for feature in admin0_collection["features"]
        }
        iso3_with_geometry.discard(None)

    for state_entry in state_entries:
        iso3 = state_entry["iso3"]
        affinity_rows = _affinity_table(state_entry, label_index)
        has_geometry = iso3 in iso3_with_geometry

        rendered = state_template.render(
            state=state_entry,
            state_name_fr=iso3_to_name_fr.get(iso3),
            moment=moments_by_iso3.get(iso3),
            affinity_table=affinity_rows,
            affinity_beta=affinity_beta,
            has_geometry=has_geometry,
            iso3_to_name_fr=iso3_to_name_fr,
            ethical_warning_fr=ETHICAL_WARNING_FR,
        )
        (STATES_OUT_DIR / f"{iso3}.md").write_text(rendered)

        (DATA_STATES_DIR / f"{iso3}.profile.json").write_text(
            json.dumps(state_entry, indent=2, ensure_ascii=False)
        )

        if has_geometry:
            single_state_geojson = extract_single_state_geojson(iso3)
            if single_state_geojson is not None:
                (DATA_STATES_DIR / f"{iso3}.geojson").write_text(
                    json.dumps(single_state_geojson, ensure_ascii=False)
                )

    (STATES_OUT_DIR / "index.md").write_text(
        states_index_template.render(
            states=state_entries,
            iso3_with_geometry=iso3_with_geometry,
            iso3_to_name_fr=iso3_to_name_fr,
            ethical_warning_fr=ETHICAL_WARNING_FR,
        )
    )


def render_map_page(artefacts: dict) -> None:
    MAP_OUT_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()
    map_template = env.get_template("map_page.md.j2")
    (MAP_OUT_DIR / "index.md").write_text(
        map_template.render(
            ethical_warning_fr=ETHICAL_WARNING_FR,
            maplibre_version=PHASE2_PINNED_MAPLIBRE_VERSION,
            natural_earth_commit=NATURAL_EARTH_PINNED_COMMIT,
        )
    )


def render_basis_page(artefacts: dict) -> None:
    BASIS_OUT_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()
    basis_template = env.get_template("basis_page.md.j2")
    (BASIS_OUT_DIR / "index.md").write_text(
        basis_template.render(
            ethical_warning_fr=ETHICAL_WARNING_FR,
            plotly_version=PHASE2_PINNED_PLOTLY_VERSION,
            b_viz_axes_count=len(artefacts["b_viz"]["axes"]),
            b_score_axes_count=len(artefacts["b_score"]["axes"]),
            civilization_count=len(artefacts["centroids"]["centroids"]),
            state_count=len(artefacts["state_coordinates"]["states"]),
        )
    )


def render_moments_page(artefacts: dict) -> None:
    MOMENTS_OUT_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()
    moments_template = env.get_template("moments_page.md.j2")
    (MOMENTS_OUT_DIR / "index.md").write_text(
        moments_template.render(
            ethical_warning_fr=ETHICAL_WARNING_FR,
            state_count=len(artefacts["moments"]["moments"]),
        )
    )


def _compute_state_distance_matrix(artefacts: dict) -> dict:
    """Compute a global distance matrix between all states with complete B_score data."""
    from packages.civvec_core.algebra.distances import (
        HybridWeights,
        civilization_ground_cost_squared,
        d_hybrid,
        d_M_frobenius,
        d_score_euclidean,
        d_score_mahalanobis_centroids,
        d_score_mahalanobis_intra,
        d_viz,
        d_w_cosine,
        d_w_js,
        d_w_wasserstein,
        intra_civilizational_covariance_inverse,
        weighted_centroid_covariance_inverse,
    )

    states = artefacts["state_coordinates"]["states"]
    centroids = artefacts["centroids"]["centroids"]
    moments_by_iso3 = {
        entry["iso3"]: np.asarray(entry["M"], dtype=float)
        for entry in artefacts["moments"]["moments"]
    }

    civilization_id_order = [centroid["civilization_id"] for centroid in centroids]
    centroid_mu_scores = np.asarray(
        [centroid["mu_score"] for centroid in centroids], dtype=float
    )
    centroid_sigma_scores = np.asarray(
        [centroid["sigma_score"] for centroid in centroids], dtype=float
    )
    ground_cost_squared = civilization_ground_cost_squared(centroid_mu_scores)
    covariance_inverse_centroids = weighted_centroid_covariance_inverse(centroid_mu_scores)
    covariance_inverse_intra = intra_civilizational_covariance_inverse(centroid_sigma_scores)
    hybrid_weights = HybridWeights()

    eligible_states: list[dict] = []
    for state_entry in states:
        if not state_entry.get("x_score") or any(value is None for value in state_entry["x_score"]):
            continue
        if not state_entry.get("x_viz") or any(value is None for value in state_entry["x_viz"]):
            continue
        if state_entry["iso3"] not in moments_by_iso3:
            continue
        eligible_states.append(state_entry)

    iso3_order = [state_entry["iso3"] for state_entry in eligible_states]
    n_states = len(eligible_states)

    metric_keys = (
        "d_viz", "d_score_euclidean",
        "d_score_mahalanobis_centroids", "d_score_mahalanobis_intra",
        "d_w_cosine", "d_w_js", "d_w_wasserstein",
        "d_M_frobenius",
    )
    matrices_unnormalised: dict[str, np.ndarray] = {
        metric: np.zeros((n_states, n_states), dtype=float)
        for metric in metric_keys
    }

    x_viz_array = np.asarray(
        [state_entry["x_viz"] for state_entry in eligible_states], dtype=float
    )
    x_score_array = np.asarray(
        [state_entry["x_score"] for state_entry in eligible_states], dtype=float
    )
    affinity_array = np.asarray(
        [[state_entry["affinity_vector"].get(civ_id, 0.0) for civ_id in civilization_id_order]
         for state_entry in eligible_states],
        dtype=float,
    )
    moment_array = np.asarray(
        [moments_by_iso3[state_entry["iso3"]] for state_entry in eligible_states], dtype=float
    )

    for left in range(n_states):
        for right in range(left, n_states):
            d_v = d_viz(x_viz_array[left], x_viz_array[right])
            d_se = d_score_euclidean(x_score_array[left], x_score_array[right])
            d_sm_centroids = d_score_mahalanobis_centroids(
                x_score_array[left], x_score_array[right], covariance_inverse_centroids
            )
            d_sm_intra = d_score_mahalanobis_intra(
                x_score_array[left], x_score_array[right], covariance_inverse_intra
            )
            d_wc = d_w_cosine(affinity_array[left], affinity_array[right])
            d_wj = d_w_js(affinity_array[left], affinity_array[right])
            d_ww = d_w_wasserstein(affinity_array[left], affinity_array[right], ground_cost_squared)
            d_mf = d_M_frobenius(moment_array[left], moment_array[right])
            for matrix_key, value in (
                ("d_viz", d_v), ("d_score_euclidean", d_se),
                ("d_score_mahalanobis_centroids", d_sm_centroids),
                ("d_score_mahalanobis_intra", d_sm_intra),
                ("d_w_cosine", d_wc), ("d_w_js", d_wj), ("d_w_wasserstein", d_ww),
                ("d_M_frobenius", d_mf),
            ):
                matrices_unnormalised[matrix_key][left, right] = value
                matrices_unnormalised[matrix_key][right, left] = value

    from packages.civvec_core.algebra.distances import normalise_distances_by_panel_median
    median_normaliser: dict[str, float] = {}
    for metric_key in metric_keys:
        upper_triangle_values = matrices_unnormalised[metric_key][np.triu_indices(n_states, k=1)]
        median_normaliser[metric_key] = float(np.median(upper_triangle_values)) if n_states > 1 else 1.0

    normalised_d_sm_intra = normalise_distances_by_panel_median(
        matrices_unnormalised["d_score_mahalanobis_intra"]
    )
    normalised_d_ww = normalise_distances_by_panel_median(
        matrices_unnormalised["d_w_wasserstein"]
    )
    normalised_d_mf = normalise_distances_by_panel_median(
        matrices_unnormalised["d_M_frobenius"]
    )
    hybrid_matrix = (
        hybrid_weights.alpha * normalised_d_sm_intra
        + hybrid_weights.beta * normalised_d_ww
        + hybrid_weights.gamma * normalised_d_mf
    )

    matrices: dict[str, list[list[float]]] = {
        metric: matrices_unnormalised[metric].tolist() for metric in metric_keys
    }
    matrices["d_hybrid"] = hybrid_matrix.tolist()

    return {
        "_meta": {
            "schema": "distance_matrix.schema.json",
            "n_states": n_states,
            "hybrid_weights": {
                "alpha": hybrid_weights.alpha,
                "beta": hybrid_weights.beta,
                "gamma": hybrid_weights.gamma,
            },
            "hybrid_components_normalised_by": "panel_median",
            "hybrid_components": [
                "d_score_mahalanobis_intra",
                "d_w_wasserstein",
                "d_M_frobenius",
            ],
            "panel_medians": median_normaliser,
            "affinity_beta": artefacts["state_coordinates"]["_meta"]["affinity_beta"],
            "iso3_to_name_fr": _iso3_to_name_fr(),
        },
        "iso3_order": iso3_order,
        "matrices": matrices,
    }


def render_distances_page(artefacts: dict) -> None:
    DISTANCES_OUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()

    distance_payload = _compute_state_distance_matrix(artefacts)
    (DATA_ASSETS_DIR / "state_distance_matrix.json").write_text(
        json.dumps(distance_payload, indent=2, ensure_ascii=False)
    )

    distances_template = env.get_template("distances_page.md.j2")
    (DISTANCES_OUT_DIR / "index.md").write_text(
        distances_template.render(
            ethical_warning_fr=ETHICAL_WARNING_FR,
            state_count=distance_payload["_meta"]["n_states"],
        )
    )


def render_phase2() -> None:
    artefacts = _load_phase2_artefacts()
    if artefacts is None:
        print("[site] Phase 2 artefacts missing — skipping Phase 2 rendering")
        return
    _copy_basis_artefacts_to_data_assets(artefacts)
    render_states(artefacts)
    render_map_page(artefacts)
    render_basis_page(artefacts)
    render_moments_page(artefacts)
    render_distances_page(artefacts)
    print(
        f"[site] Phase 2 rendered: {len(artefacts['state_coordinates']['states'])} states, "
        "map + basis + moments + distances pages."
    )


def render_all() -> None:
    from apps.site_builder.vulgarisation import render_vulgarisation

    render_methodology()
    render_taxonomy()
    render_sources()
    render_schemas()
    render_phase2()
    render_vulgarisation()
    print("[site] rendered methodology, taxonomy, sources, schemas, phase2, vulgarisation")

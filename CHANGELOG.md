# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added — Phase 2 livrée (2026-06-01)

- **Géométries Natural Earth ADM0 110m** versionnées dans `data_sources/natural_earth/admin0_countries_110m.geojson` — pinned commit `nvkelso/natural-earth-vector @ ca96624a56`, domaine public ; 62/63 ISO3 couverts (HKG et SGP absents à cette résolution, mention explicite). Aucune géométrie GADM publiée.
- **Module `apps/basis_builder/geometries.py`** : `fetch_and_filter_natural_earth_admin0()` reproductible, tagging `geometry_source = "Natural Earth"` + `contains_gadm_geometry: false` sur chaque feature. CLI `civvec basis fetch-geometries`.
- **Templates Jinja2 Phase 2** (`site_src/templates/`) : `state_page.md.j2`, `states_index.md.j2`, `map_page.md.j2`, `basis_page.md.j2`, `tensions_page.md.j2`, `distances_page.md.j2` — bannière éthique sur chaque page.
- **Builder Phase 2** (`apps/site_builder/builder.py`) : `render_states`, `render_map_page`, `render_basis_page`, `render_tensions_page`, `render_distances_page` + calcul global de la matrice de distances (8 métriques : `d_viz`, `d_score^E`, `d_score^M`, `d_w^cos`, `d_w^JS`, `d_w^W`, `d_T`, `d_hyb`).
- **Pages publiées** : 63 fiches États (`/states/<ISO3>/`) + `/states/`, `/map/`, `/basis/`, `/tensions/`, `/distances/`.
- **Assets data** (`dist/assets/data/`) : `state_coordinates.json`, `civilization_centroids.json`, `state_tensors.json`, `state_distance_matrix.json`, `B_viz.json`, `B_score.json`, `global_state_baseline.geojson` + dossier `states/<ISO3>.profile.json` et `states/<ISO3>.geojson`.
- **Assets JS** (`site_src/docs/assets/js/`) : `map.js` (MapLibre GL JS 4.7.1, choropleth par civilisation dominante, sans fond externe), `basis_viz.js` (Plotly 2.35.2 scatter B_viz + radar B_score), `tensors.js` (anisotropie + heatmap 6×6 avec sélecteur ISO3), `distances.js` (heatmap matrice + détail toutes-distances par paire).
- **`mkdocs.yml`** : nav étendue (États / Carte / Base vectorielle / Tensions / Distances), CDN MapLibre + Plotly pinné, `not_in_nav` pour les 63 fiches États.
- **Tests Phase 2** (`tests/test_site_build.py`) : présence et provenance Natural Earth, FRA carry `x_viz` + Hofstede + tenseur, matrice de distance symétrique avec diagonale 0, JS hooks `civvec-*` présents, assets data téléchargeables (10 nouveaux tests).
- Vérification end-to-end : `docker compose build civvec_site` ✓, suite 51 tests ✓ en image site, suite 33 tests ✓ en image UI, nginx preview `HTTP 200` sur `/states/FRA/`, `/map/`, `/basis/`, `/tensions/`, `/distances/`.

### Published — Phase 1b en ligne (2026-05-30)

- Dépôt initialisé sur `git@github.com:s-geffroy/cvs.git` (public).
- GitHub Pages activé avec source = GitHub Actions.
- Premier déploiement automatique réussi via `.github/workflows/publish.yml`.
- URL Pages : <https://s-geffroy.github.io/cvs/> — accueil, fiches civilisations, méthodologie, ADM1, sources, schémas servis avec bannière éthique sur chaque page.

### Added — Phase 1b livrée (2026-05-30)

- `mkdocs.yml` Material avec navigation Phase 1b (Accueil, Méthodologie, Taxonomie, Civilisations ×11, Sources, Schémas, ADM1, Relecture).
- Bannière éthique persistante via override `site_src/overrides/main.html` (block `announce` de Material).
- `site_src/docs/index.md`, `ethics.md`, `adm1_policy.md`, `review/index.md`.
- `apps/site_builder/builder.py` + `loaders.py` + `guards.py` (whitelist géométries `{Natural Earth, geoBoundaries}`, scan GADM).
- Templates Jinja2 : `civilization_page.md.j2` (hyper-détaillé), `taxonomy_index.md.j2`, `sources_index.md.j2`, `schemas_index.md.j2`, `methodology_index.md.j2`.
- CLI `civvec site build` + `civvec site preview` + branchement dans `civvec` root.
- `Dockerfile.site` multi-stage (builder + nginx preview) + services `civvec_site` et `civvec_site_preview` dans `docker-compose.yml`.
- Tests `tests/test_site_build.py` (11 tests : éthique sur chaque page, 11 civilisations rendues, méthodo 00..10 présente, bibliographie/sources/schemas/ADM1 publiés, pas de géométrie GADM).
- Workflow GitHub Actions `.github/workflows/publish.yml` : build via container, exécution pytest, déploiement Pages.
- Vérification end-to-end : `docker compose run --rm civvec_site` ✓, suite 41 tests ✓ en image site, nginx preview `HTTP 200` sur Accueil, fiche Western, mécanique tensorielle.

### Added — Phase 1 livrée (2026-05-30)

- Vérification end-to-end : `docker compose build civvec_ui` ✓, `docker compose up civvec_ui` ✓ (HTTP 200 sur `/_stcore/health`), `pytest` 33/33 ✓.

### Added — Phase 1 bootstrap (2026-05-30)

- Initial `cvs/` project layout next to read-only reference `raw/`.
- Top-level `README.md`, `CHANGELOG.md`, `.gitignore`, `pyproject.toml` with extras `[basis,ui,site,dev]`.
- Directory skeleton: `apps/`, `packages/civvec_core/`, `schemas/`, `taxonomies/`, `data_sources/`, `docs/`, `site_src/`, `tests/`.
- JSON Schemas v2: `basis.schema.json`, `civilization_centroid.schema.json`, `state_coordinates.schema.json`, `state_tension.schema.json`, `distance_matrix.schema.json`, `macro_civilizations.schema.json`, `state_profile.v2.schema.json`, `adm1_profile.v2.schema.json`.
- B_doc canonical data: `data_sources/inglehart_welzel/cultural_map_wave7.json`, `data_sources/hofstede/dimensions_v2015.json`, `data_sources/SOURCES.md`.
- B_doc methodology: docs `00..07` rebased from `raw/docs/`, plus new `08_civilizational_basis.md`, `09_civilizational_mechanics.md`, `10_distance_algebra.md`.
- Hyper-detailed taxonomy `taxonomies/macro_civilizations.v2.json` covering 11 macro-civilisations with `huntington_label`, `iw_clusters`, `hofstede_archetype_states`, `member_states[]`, `sub_clusters[]`, `ambiguous_cases[]`, `citation_ids[]`, `bibliography[]`.
- B_vec formal definitions: `packages/civvec_core/basis/B_viz.json` (ℝ², Inglehart-Welzel), `B_score.json` (ℝ⁶, Hofstede).
- B_vec builder: `apps/basis_builder/{load_iw,load_hofstede,centroids,projector,tensors}.py`.
- Civilizational tensor mechanics: `state_tensors.json`, invariants, eigenvalues, anisotropy index, `09_civilizational_mechanics.md`.
- Distance algebra: `packages/civvec_core/algebra/{distances,transport}.py` with `d_viz`, `d_score^E`, `d_score^M`, `d_w^cos`, `d_w^JS`, `d_w^W` (Sinkhorn), `d_T`, `d_hyb`. Doc `10_distance_algebra.md`.
- Typer CLI `civvec` with subcommands `basis build`, `basis validate`, `ui`.
- Streamlit UI Phase 1: `Home.py` + 9 pages (Documentary Basis, Vector Basis, State Explorer, Compare States, Diagnostics, Sources, Methodology, State Tensions, Distance Algebra), shared `ethics_banner` and `charts` components.
- Docker: `Dockerfile.ui` + `docker-compose.yml` service `civvec_ui` (port 8501).
- Tests: `test_documentary_basis.py`, `test_vector_basis.py`, `test_bases_coupling.py`, `test_tensor_mechanics.py`, `test_distance_algebra.py`, `test_ui_smoke.py`, `test_adm1_anticipation.py`.
- ADM1 anticipation: `schemas/adm1_profile.v2.schema.json`, `docs/04_adm1_preparation_policy.md`, CLI hook returning `prepared_not_active`.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

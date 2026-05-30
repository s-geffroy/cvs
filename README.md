# cvs — Civilizational Vector State (v2)

> **Avertissement éthique** : Ce projet infère des profils civilisationnels d'**États souverains** à partir de **sources publiques agrégées** (WVS, Hofstede, Inglehart-Welzel, Natural Earth, geoBoundaries). **Ces profils ne doivent jamais être utilisés pour classer des individus réels.**

Pipeline Python bayésien produisant pour chaque État un vecteur d'affiliation civilisationnelle, ancré sur **deux bases** :

- **Base documentaire (B_doc)** — Huntington (1996) + Inglehart-Welzel (2005, 2010) + Hofstede (2010) + WVS wave 7.
- **Base vectorielle (B_vec)** — `B_viz = ℝ²` (Inglehart-Welzel : Traditional↔Secular-Rational, Survival↔Self-Expression) et `B_score = ℝ⁶` (Hofstede : PDI, IDV, MAS, UAI, LTO, IVR).

Étendu par :

- **Mécanique tensorielle** des tensions internes d'un État (`T(s) ∈ ℝ^{6×6}`, analogue au tenseur des contraintes en milieux continus).
- **Algèbre des distances** civilisationnelles (Euclidienne, Mahalanobis, cosinus, Jensen-Shannon, Wasserstein-2, Frobenius, hybride pondérée).

ADM1 préparé architecturalement, **non activé** en V1.

## Quickstart (Docker uniquement)

```bash
cd /Users/sge/civilizational-vector-state/cvs

# Build du builder + UI
docker compose build civvec_ui

# Construit les bases et lance Streamlit sur http://localhost:8501
docker compose up civvec_ui
```

Toute exécution se fait en container. **Ne jamais installer en local.**

## Repo cible

`git@github.com:s-geffroy/cvs.git` — publication GitHub Pages : `https://s-geffroy.github.io/cvs/`.

## Structure

```
cvs/
├── apps/
│   ├── cli/                  # Typer CLI (civvec)
│   ├── basis_builder/        # Builders B_vec, centroïdes, tenseurs
│   ├── site_builder/         # Builder MkDocs (Phase 1b/2)
│   └── ui_streamlit/         # UI multi-pages (Phase 1)
├── packages/civvec_core/
│   ├── basis/                # B_viz.json, B_score.json, centroïdes, tenseurs
│   └── algebra/              # distances.py, transport.py
├── schemas/                  # JSON Schemas v2
├── taxonomies/               # macro_civilizations.v2.json (charnière B_doc ↔ B_vec)
├── data_sources/             # IW wave 7, Hofstede, SOURCES.md
├── docs/                     # Méthodologie 00..10 (renumérotée + étendue)
├── site_src/                 # Source MkDocs Material (Phase 1b/2)
└── tests/                    # Suite pytest
```

## Bases

- `taxonomies/macro_civilizations.v2.json` — 11 civilisations enrichies : citations, sous-clusters, États membres, controverses, coordonnées B_vec.
- `packages/civvec_core/basis/civilization_centroids.json` — barycentres μ et covariances Σ par civilisation.
- `packages/civvec_core/basis/state_coordinates.json` — `x_viz` (ℝ²) + `x_score` (ℝ⁶) par État.
- `packages/civvec_core/basis/state_tensors.json` — tenseurs de tension `T(s)` + invariants + eigenvalues.

## Licences des sources

Cf. `data_sources/SOURCES.md`. WVS = CC-BY ; Hofstede = usage scientifique ; Natural Earth = domaine public ; geoBoundaries = CC-BY 4.0. **GADM jamais publié** (restriction de redistribution).

## Liens

- Plan d'implémentation : `/Users/sge/.claude/plans/tu-vas-lire-raw-groovy-allen.md`
- Source de référence v1 (lecture seule) : `../raw/`
- CHANGELOG : [`CHANGELOG.md`](./CHANGELOG.md)

# cvs — Civilizational Vector State (v2)

> **Avertissement éthique** : Ce projet infère des profils civilisationnels d'**États souverains** à partir de **sources publiques agrégées** (WVS, Hofstede, Inglehart-Welzel, Natural Earth, geoBoundaries). **Ces profils ne doivent jamais être utilisés pour classer des individus réels.**

Pipeline Python bayésien produisant pour chaque État un vecteur d'affiliation civilisationnelle, ancré sur **deux bases** :

- **Base documentaire (B_doc)** — Huntington (1996) + Inglehart-Welzel (2005, 2010) + Hofstede (2010) + WVS wave 7.
- **Base vectorielle (B_vec)** — `B_viz = ℝ²` (Inglehart-Welzel : Traditional↔Secular-Rational, Survival↔Self-Expression) et `B_score = ℝ⁶` (Hofstede : PDI, IDV, MAS, UAI, LTO, IVR).

Étendu par :

- **Mécanique tensorielle** des tensions internes d'un État (`T(s) ∈ ℝ^{6×6}`, analogue au tenseur des contraintes en milieux continus).
- **Algèbre des distances** civilisationnelles (Euclidienne, Mahalanobis, cosinus, Jensen-Shannon, Wasserstein-2, Frobenius, hybride pondérée).
- **Cascade d'imputation V2.1** ([`docs/16_imputation_cascade.md`](docs/16_imputation_cascade.md)) garantissant `x_viz ∈ ℝ²` et `x_score ∈ ℝ⁶` non-nuls pour les **193 États membres de l'ONU**, en cinq tiers de qualité décroissante alimentés par WVS Time-Series, Pew composition complète, UNDP HDR, UN GA voting (Voeten), V-Dem v16, WGI, FSI. Couverture finale : **0 État au tier `centroid_prior`**.

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

- `taxonomies/macro_civilizations.v2.json` — 11 civilisations enrichies, **193/193 États ONU mappés** : citations, sous-clusters, États membres, controverses, coordonnées B_vec.
- `packages/civvec_core/basis/civilization_centroids.json` — barycentres μ et covariances Σ par civilisation.
- `packages/civvec_core/basis/state_coordinates.json` — `x_viz` (ℝ²) + `x_score` (ℝ⁶) par État (**193 entrées non-nulles, provenance par coordonnée**).
- `packages/civvec_core/basis/state_moments.json` — tenseurs `M(s)` + invariants + eigenvalues (**193 entrées, inflation diagonale propagée pour les coordonnées imputées**).
- `data_sources/un_members/coverage_report.md` — rapport de couverture régénéré par `civvec basis coverage-report` avec distribution par tier de la cascade.

## Licences des sources

Cf. `data_sources/SOURCES.md`. WVS = CC-BY ; Hofstede = usage scientifique ; Natural Earth = domaine public ; geoBoundaries = CC-BY 4.0 ; UNDP HDR = libre avec citation ; Voeten UN GA voting = CC-0 ; V-Dem = CC-BY 4.0 ; Pew = citation académique. **GADM jamais publié** (restriction de redistribution). Les fichiers volumineux (WVS time-series 1.3 GB, V-Dem RData 33 MB, UNDP HDR CSV 2 MB) sont hors-tracking git (cf. `.gitignore`) ; re-téléchargeables via les URL et procédures documentées.

## Liens

- Plan d'implémentation : `/Users/sge/.claude/plans/tu-vas-lire-raw-groovy-allen.md`
- Source de référence v1 (lecture seule) : `../raw/`
- CHANGELOG : [`CHANGELOG.md`](./CHANGELOG.md)

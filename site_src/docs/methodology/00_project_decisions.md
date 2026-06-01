# 00 — Décisions structurantes du projet

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md`](07_ethics_publication_policy.md).

## 1. Portée — State-first

`cvs/` produit un **vecteur d'affiliation civilisationnelle** par État souverain. Le projet renonce dès cette version à toute prétention sub-nationale active : l'unité analytique de la v3.0 est l'**ADM0** (État souverain, code ISO3).

L'architecture est **préparée pour ADM1** (régions sub-nationales) — schémas JSON, hooks CLI, géométries geoBoundaries ADM1 versionnées — mais aucune sortie ADM1 n'est produite ni publiée. Cf. [doc 04 — Politique ADM1](04_adm1_preparation_policy.md).

## 2. Sources de données — *public aggregate sources only*

Le projet n'utilise **aucune** des sources suivantes :

- Questionnaires individuels.
- Réponses personnelles non agrégées.
- Graphes sociaux privés.
- Noms, patronymes, ou caractéristiques individuelles.
- Données scrapées de sources privées.

Il utilise **uniquement** :

- Datasets publics internationaux (WVS, Hofstede, Pew, WGI, FSI).
- Statistiques officielles publiées par les États ou organismes intergouvernementaux.
- Datasets de frontières publics (Natural Earth, geoBoundaries — **jamais GADM** en publication).
- Littérature académique pour la taxonomie et la méthodologie.

Cf. [doc 02 — Méthodologie source-only](02_source_only_methodology.md) pour les détails et [doc 07 — Éthique de publication](07_ethics_publication_policy.md) pour les règles d'inférence interdites.

## 3. Implémentation et stockage

- **Langage** : Python 3.11+.
- **Architecture** : librairie + CLI Typer + UI Streamlit + site MkDocs Material.
- **Runtime** : **Docker uniquement**. Aucune installation locale requise ni autorisée — cf. `Dockerfile.ui` et `Dockerfile.site`.
- **Stockage** :
    - Index SQLite (à venir, non encore activé) pour les query rapides.
    - JSON pour les artefacts canoniques (centroïdes, coordonnées, moments, distances).
    - Markdown pour les rapports humains.
    - GeoJSON pour l'interopérabilité cartographique.
- **Exports** : `json`, `markdown`, `geojson`.

## 4. Décisions méthodologiques majeures de la v3.0

Par rapport à la v2.0 :

1. **Renommage `T(s)` → `M(s)`** (second moment civilisationnel) — cf. [doc 09](09_civilizational_second_moment.md) et [doc 11 §C9–C13](11_critiques_and_responses.md).
2. **Mahalanobis intra-civilisationnelle** introduite à côté de l'inter — cf. [doc 10](10_distance_algebra.md).
3. **Normalisation par médiane panel** des composantes de `d_hyb` — cf. [doc 10 §2.8](10_distance_algebra.md).
4. **Pages de critiques anticipées, validation empirique, sensibilité, baseline, glossaire** publiées — cf. [doc 11](11_critiques_and_responses.md), [12](12_empirical_validation.md), [13](13_sensitivity_analysis.md), [14](14_baseline_unsupervised.md), [15](15_glossary.md).
5. **Politique éthique étoffée** — cf. [doc 07](07_ethics_publication_policy.md).
6. **Règle de désambiguïsation** explicite pour les civilisations chevauchantes (KOR, BOL, etc.) — cf. [doc 08 §3.4](08_civilizational_basis.md).

## 5. Décisions résolues sans ambiguïté

- **Sortie active** : profils État (`state_profile.json`, `.md`), GeoJSON ADM0, scoring par État.
- **Sortie préparée non active** : profils ADM1 (`prepared_not_active` retourné par le CLI), segments synthétiques ADM1, pilotes ADM1 approfondis, cartes ADM1.

## 6. Décisions explicitement réversibles

Toute modification d'un poids éditorial (`periphery=0.5`, `β=0.05`, `(α, β, γ)=(0.4, 0.4, 0.2)`) doit être consignée dans `CHANGELOG.md`. Toute modification d'un centroïde déclenche une révision automatique des `state_moments.json`, `state_distance_matrix.json`, et de la matrice publiée.

Toute modification d'une **règle de désambiguïsation** ([doc 08 §3.4](08_civilizational_basis.md)) doit être discutée publiquement via issue avant merge.

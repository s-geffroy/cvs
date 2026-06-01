# 06 — Outputs et stockage

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md`](07_ethics_publication_policy.md).

## 1. Formats supportés

| Format | Rôle | Validé par |
|---|---|---|
| **JSON** | Artefact canonique. Conserve tous les champs, schéma documenté. | JSON Schema (draft 2020-12). |
| **Markdown** | Rapport humain auditable. Généré depuis les JSON via Jinja2. | Rendu mkdocs strict. |
| **GeoJSON** | Interopérabilité cartographique. ADM0 Natural Earth uniquement. | Schéma `geometry_provenance` + scan GADM. |
| **SQLite** | Index rapide pour requêtes (préparé, **non activé** en V1). | Schéma à venir. |

## 2. Hiérarchie des artefacts publiés

```
data_sources/                              # Données canoniques sourcées (in)
  inglehart_welzel/cultural_map_wave7.json
  hofstede/dimensions_v2015.json
  natural_earth/admin0_countries_110m.geojson
  geoboundaries/adm1/                      # bundle ADM1, non publié en V1
  pew/, wgi/, fsi/                          # validation externe (doc 12)

packages/civvec_core/basis/                # Bases vectorielles construites (out)
  B_viz.json
  B_score.json
  civilization_centroids.json
  state_coordinates.json
  state_moments.json                       # renommé v3.0 (était state_tensors)

outputs/empirical/                         # Analyses empiriques (out)
  sensitivity_leave_one_out.json
  sensitivity_beta_sweep.json
  sensitivity_hybrid_weights.json
  baseline_clustering.json
  external_validation.json

site_src/docs/assets/data/                 # Snapshot pour le site (out)
  state_coordinates.json, state_moments.json, ...
  states/<ISO3>.profile.json, <ISO3>.geojson
  empirical/sensitivity_*.json, baseline_*.json, external_validation.json
```

## 3. Niveau ADM0 actif, ADM1 préparé

Tous les outputs V1 sont **à l'échelle de l'État souverain** (ADM0). Le format ADM1 est :

- **Schéma défini** (`schemas/adm1_profile.v2.schema.json`).
- **Géométries bundleées** (`data_sources/geoboundaries/adm1/`).
- **CLI hook** qui retourne `prepared_not_active`.

Aucun output ADM1 n'est généré ni publié — cf. [doc 04](04_adm1_preparation_policy.md).

## 4. Versioning des artefacts

Chaque output JSON porte dans `_meta` :

- Nom du schéma associé (validation).
- Date de génération.
- Identifiants de référence (commits, paramètres éditoriaux).

Toute modification d'un input (centroïde, État archétype, poids) régénère les outputs en aval et est consignée dans `CHANGELOG.md`. Les versions sont taguées Git.

## 5. Politique de licence et redistribution

- **Code** : MIT.
- **Documentation et artefacts dérivés** : CC-BY 4.0.
- **Géométries** : Natural Earth = domaine public ; geoBoundaries = CC-BY. **GADM strictement interdite en publication** (cf. [doc 04 §3](04_adm1_preparation_policy.md) et [doc 07](07_ethics_publication_policy.md)).
- **Datasets externes** (WVS, Hofstede, Pew, WGI, FSI) : cités avec attribution, jamais redistribués sans transformation.

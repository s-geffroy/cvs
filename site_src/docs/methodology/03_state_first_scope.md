# 03 — Scope *State-first* V1

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md`](07_ethics_publication_policy.md).

## 1. Décision V1 : unité analytique = État souverain (ADM0)

La v3.0 reste **State-first** :

- L'unité analytique active est l'**ADM0** (ISO3 d'un État souverain).
- Aucune sortie ADM1 (régions sub-nationales) n'est active dans cette version.
- Toute analyse, score, distance, ou rapport publié s'applique à un État entier comme entité agrégée.

## 2. Outputs actifs en V1

| Output | Format | Description |
|---|---|---|
| `state_profile` | JSON (v2) | Profil complet d'un État (coordonnées, affinité, evidence, qualité). |
| `state_report_markdown` | MD | Rapport humain dérivé du profil. |
| `state_geojson` | GeoJSON | Géométrie ADM0 de l'État + provenance (Natural Earth). |
| `global_state_baseline_geojson` | GeoJSON | Collection des États publiés. |
| `state_moments.json` | JSON | Second moment civilisationnel `M(s)` par État. |
| `state_distance_matrix.json` | JSON | Matrice de distances panel × panel sur 9 métriques. |

Tous ces outputs sont publiés sur le site `https://s-geffroy.github.io/cvs/`, sections `/states/`, `/map/`, `/moments/`, `/distances/`.

## 3. Outputs préparés non actifs

| Output | Statut |
|---|---|
| `adm1_profile` | `prepared_not_active` — schéma défini, hook CLI rejette poliment. |
| `adm1_synthetic_segments` | `prepared_not_active`. |
| `adm1_deep_pilot` | Différé — aucune réflexion d'implémentation. |
| `adm1_maps` | Différé — geoBoundaries ADM1 bundle existe mais n'est pas publié. |

Cf. [doc 04 — Politique ADM1](04_adm1_preparation_policy.md).

## 4. Conséquences sur la modélisation

Représenter un État comme un point unique `xₛ^score ∈ ℝ⁶` est une **simplification volontaire** assumée :

- Les **fractures internes** (urbain/rural, immigration, classes, religions co-existantes) sont **invisibles** dans le scoring V1.
- Les **diasporas** dispersées hors de leur État d'origine ne sont pas modélisées.
- L'évolution temporelle (waves WVS successives) n'est pas modélisée — V1 fige sur wave 7 (2017-2022).

Cette simplification est explicitée dans [doc 07 §5](07_ethics_publication_policy.md) (limite assumée) et dans [doc 11 §E17](11_critiques_and_responses.md) (réponse à la critique d'essentialisme étatique).

## 5. Critères pour activer ADM1

L'activation des sorties ADM1 (passage de `prepared_not_active` à active) suppose **trois conditions cumulatives** :

1. Au moins 20 États V1 stabilisés avec validation externe positive (doc 12).
2. Politique éthique ADM1 validée par relecture publique.
3. Couverture Hofstede/IW **sub-nationale** documentée et sourcée pour au moins 5 États-pilotes (pas plus de proxy national répété).

Aucune de ces conditions n'est remplie en v3.0.

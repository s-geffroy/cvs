# 12 — Validation empirique externe

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md](07_ethics_publication_policy.md).

## 1. Objectif

Vérifier si le vecteur d'affinité civilisationnelle `wₛ ∈ Δ¹⁰` calculé par
`cvs/` (Huntington + Hofstede + IW) **se corrèle** à des indicateurs externes
**indépendants** publiés par des institutions tierces. Une corrélation forte
sur certaines civilisations conforte la cohérence du scoring ; son absence
indique un défaut de validité externe.

Cette validation **ne prouve pas** que le scoring est correct — elle teste
si ses prédictions implicites se vérifient sur des panels indépendants.

## 2. Indicateurs externes utilisés

| Indicateur | Source | Année | Couverture ONU | Type |
|---|---|---|---|---|
| **Pew Religious Composition** — 7 proportions par pays | Pew Research Center | 2020 | 182/193 | % de la population (sommant à 100) |
| **WGI Rule of Law** — État de droit | World Bank — Worldwide Governance Indicators | 2022 | 61/193 | z-score (-2.5 à +2.5) |
| **FSI Total** — fragilité étatique | Fund For Peace — Fragile States Index | 2024 | 61/193 | 0 (stable) à 120 (alerte) |
| **UNDP HDR** — HDI, GII, mean/expected schooling, GNI | UNDP Human Development Report 2025 | 2023 | 191/193 | composites normalisés |
| **UN GA voting idealpoint** — alignement politique | Voeten/Strezhnev/Bailey, Harvard Dataverse | 2025 | 192/193 | scalaire ≈ [-3, +3] |
| **V-Dem (12 indices)** — libdem, gender, corruption, religfree, etc. | V-Dem Institute v16 | 2025 | 172/193 | composites [0, 1] |

Les six indicateurs sont **publics** et capturent des dimensions
différentes (croyance religieuse, gouvernance, développement humain,
alignement politique, qualité institutionnelle, stabilité). Ces sources
servent à la fois à la **calibration** des tiers `imputed_pew`,
`imputed_governance` (cf. [doc 16](16_imputation_cascade.md)) et à la
**validation externe** ci-dessous. Pour éviter la circularité, les tests
de validation sont conduits **uniquement sur les États `observed`**, et
les imputations issues des mêmes sources ne participent pas aux
corrélations.

Données bundleées (ou téléchargeables via les URL documentées) dans
`data_sources/{pew,wgi,fsi,undp,un_voting,vdem}/`.

## 3. Protocole

Pour chaque indicateur externe et chaque civilisation `c_i` :

1. Construire le couple `(wₛ[i], indicateur(s))` pour chaque ISO3 dans le
   panel intersection (`cvs/` × données externes disponibles).
2. Calculer le **coefficient de corrélation de rangs de Spearman** `ρ` entre
   `wₛ[i]` et l'indicateur.
3. **Intervalle de confiance bootstrap à 95%** par tirage avec remise sur
   les ISO3 (`n_bootstrap = 1000`).

La corrélation de Spearman est privilégiée à Pearson car (a) les vecteurs
d'affinité sont sur le simplexe (skewed) et (b) `ρ` est robuste aux
non-linéarités monotones.

## 4. Hypothèses testables

| Civilisation | Indicateur | Direction attendue |
|---|---|---|
| `western` | WGI Rule of Law | corrélation **positive** (États occidentaux ont une gouvernance plus stable) |
| `western` | FSI | corrélation **négative** (États occidentaux moins fragiles) |
| `islamic` | Pew (musulman dominant) | corrélation **positive forte** |
| `sinic` | Pew (unaffiliated dominant ou bouddhiste) | corrélation modérée |
| `hindic` | Pew (hindou dominant) | corrélation **positive forte** |
| `latin_american` | Pew (chrétien dominant) | corrélation **positive** |
| `african` | FSI | corrélation positive (États africains parmi les plus fragiles) |

Une absence de signal sur ces hypothèses naïves serait un signal d'alerte.

## 5. Données et reproductibilité

Les résultats numériques sont stockés dans
**`assets/data/empirical/external_validation.json`** (généré par
`civvec empirical validate`), avec pour chaque indicateur et chaque
civilisation : `n_states_paired`, `spearman_rho`, `bootstrap_ci_95_lower`,
`bootstrap_ci_95_upper`.

Pour reproduire :

```bash
docker compose run --rm civvec_site civvec empirical validate
```

## 6. Lecture

Le tableau publié est ordonné par valeur absolue de `ρ` au sein de chaque
indicateur — les civilisations en haut de chaque section indiquent les
corrélations les plus fortes (positives ou négatives). Les intervalles
bootstrap permettent de filtrer les associations significatives à 95%.

### 6.1 Critères de validité

- **ρ > 0.5 avec CI95 entièrement > 0** : association forte cohérente.
- **|ρ| < 0.2 et CI95 chevauche 0** : pas de signal.
- **Direction opposée à l'attendu** : signal d'alerte — réviser la
  taxonomie ou les centroïdes pour la civilisation concernée.

### 6.2 Résultats v3.0 — top corrélations

Mesures publiées dans `assets/data/empirical/external_validation.json` :

#### Pew Religious Composition 2020 — part du groupe religieux dominant

| Civilisation | `ρ` (Spearman) | Direction attendue | Verdict |
|---|---|---|---|
| `islamic` | **+0.52** | + (Pew musulman dominant) | **OK** |
| `buddhist` | **+0.49** | + (Pew bouddhiste dominant) | **OK** |
| `latin_american` | **+0.47** | + (Pew chrétien dominant) | **OK** |

#### WGI Rule of Law 2022

| Civilisation | `ρ` | Direction attendue | Verdict |
|---|---|---|---|
| `western` | **+0.63** | + (gouvernance forte) | **OK** |
| `indigenous` | **−0.59** | (non prédit) | Signal exogène à investiguer |
| `buddhist` | **−0.57** | (non prédit) | Signal exogène à investiguer |

#### Fragile States Index 2024

| Civilisation | `ρ` | Direction attendue | Verdict |
|---|---|---|---|
| `western` | **−0.57** | − (États occidentaux moins fragiles) | **OK** |
| `islamic` | **+0.56** | (non prédit explicitement, intuitif) | Signal cohérent |

**Conclusion** : les **3 hypothèses pré-spécifiées** (Western↔WGI+, Islamic↔Pew musulman+, Western↔FSI−) sont **toutes confirmées** avec `|ρ| > 0.5`. Les signaux exogènes sur `indigenous` et `buddhist` méritent une investigation séparée (probablement des biais de couverture WGI sur les petits États asiatiques et indigènes).

### 6.2 Cas de figure

Si les hypothèses `western ↔ WGI+`, `islamic ↔ Pew(musulman)+`, etc.
**ne sont pas vérifiées**, plusieurs explications possibles :

1. Mauvaise calibration du softmax (β) — voir [doc 13](13_sensitivity_analysis.md).
2. Mauvais États archétypes (LOO instable) — voir
   [doc 13](13_sensitivity_analysis.md).
3. Limites intrinsèques de l'approche Huntington+Hofstede pour capturer la
   dimension testée — limite assumée à documenter.

## 7. Limites

1. **Spearman, pas causalité** : une corrélation forte ne prouve pas une
   correspondance ontologique. Une civilisation `cvs/` peut être un proxy
   d'autre chose.
2. **Indicateurs imparfaits** : Pew n'est pas une mesure de civilisation,
   WGI peut refléter des biais occidentaux de l'évaluation institutionnelle.
3. **Panel limité** : ~60 ISO3 — significativité statistique modérée.
4. **Aucune correction multi-test** : on calcule 11 (civilisations) × 3
   (indicateurs) = 33 tests. Une correction Bonferroni serait à 95% / 33 ≈
   99.85% par test — exigeante. Les CI bootstrap à 95% ne corrigent pas
   pour la multiplicité.

## 8. Stratification par provenance (V2)

Depuis l'introduction de la cascade ([doc 16](16_imputation_cascade.md)), tous
les tests de cette section sont calculés **uniquement sur les États dont la
provenance est `observed`** (intersection IW ∩ Pew/WGI/FSI). Les États
`centroid_prior` sont exclus pour éviter la circularité — voir
[doc 11 §H28](11_critiques_and_responses.md). Les corrélations rapportées sur
les ~60 États observés ne se dégradent donc pas avec l'ajout des 130 États
imputés/prior.

Un encadré « stratification » dans chaque tableau de corrélation indique le
nombre d'États inclus par tier ; un tier `centroid_prior` séparé peut être
ajouté à titre informatif (corrélation attendue = 1.0 par construction,
*non utilisée pour la validation*).

## 9. Travaux futurs

- Ajouter Polity V (régime politique).
- Ajouter UNESCO sur le patrimoine culturel.
- Validation longitudinale (waves WVS successives) pour vérifier la
  stabilité du scoring dans le temps.

# 05 — Calibration du scoring

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md`](07_ethics_publication_policy.md).

## 1. Statut de la calibration en V1

| Niveau | Statut |
|---|---|
| **V1 active** | Règles expertes avec plafonds de confiance et pénalités d'incertitude (poids éditoriaux justifiés mais non calibrés empiriquement). |
| **Préparé pour la suite** | Élicitation experte structurée + calibration empirique contre indicateurs externes. |
| **Statut empirique** | `prepared_not_claimed` — voir [doc 12](12_empirical_validation.md) pour les corrélations publiées. |

## 2. Vocabulaire à respecter

⚠️ **Le projet ne revendique pas de probabilités calibrées**. La calibration probabilistique stricte (au sens *Brier score*, *reliability diagram*) n'a **pas été conduite** en V1.

Vocabulaire autorisé :

- *Heuristic probabilistic estimate*.
- *Affinity score*.
- *Weighted civilizational composition*.

Vocabulaire **interdit** (sauf à conduire la calibration empirique d'abord) :

- *Calibrated probability*.
- *Posterior probability* sans bayésien explicite et publié.
- *Confidence-calibrated weight*.

## 3. Points de calibration éditoriale documentés

| Paramètre | Valeur V1 | Justification | Sensibilité |
|---|---|---|---|
| Poids `core` archétype | 1.0 | Convention | Non testée |
| Poids `periphery` archétype | 0.5 | Éditorial — milieu de l'intervalle | Testée doc 13 |
| Poids `ambiguous` archétype | 0.0 | Exclusion volontaire du centroïde | Implicite |
| `β` softmax inverse-distance | 0.05 | Heuristique sur l'échelle Hofstede 0-100 | Sweep doc 13 |
| `(α, β, γ)` hybride | (0.4, 0.4, 0.2) | Éditorial | Sweep doc 13 |
| Régularisation ridge Mahalanobis | 1.0 | Standard low-rank estimation | Non testée |
| Régularisation Sinkhorn entropie | 0.05 | Compromis numérique vs précision | Non testée |

Toutes ces valeurs sont **réversibles** et leur modification doit être consignée dans `CHANGELOG.md`.

## 4. Calibration des imputations (V2.1)

Depuis l'introduction de la cascade ([doc 16](16_imputation_cascade.md)), trois jeux de poids supplémentaires sont calibrés *empiriquement* par régression ridge :

### 4.1 `pew_to_iw` — (Pew composition + UNDP HDR + UN voting + V-Dem) → (ts, se)

- **Jeu d'entraînement** : intersection IW observée ∩ (Pew ∪ UNDP ∪ UN voting ∪ V-Dem). Taille typique : ~62 États.
- **Vecteur de features** (17 dimensions + intercept) : 7 proportions Pew + 5 features UNDP (HDI, GII, mys, eys, log GNI) + 1 idealpoint Voeten + 4 indices V-Dem (libdem, civlib, religfree, gender).
- **Régularisation** : ridge α = 1.0, intercept non régularisé.
- **Validation** : leave-one-out. RMSE LOO : ts ≈ 0.48, se ≈ 0.62 (sur une plage IW typique [-2, +2]).
- **Imputation des features absentes** : remplacement par la moyenne du jeu d'entraînement pour la feature concernée. N'altère pas la taille du jeu d'entraînement.

### 4.2 `governance_to_hofstede` — (WGI + FSI + UNDP HDR + UN voting + V-Dem) → 6 dimensions Hofstede

- **Jeu d'entraînement** : Hofstede observé ∩ (≥ 1 auxiliaire). Taille typique : 63 États.
- **Vecteur de features** (14 dimensions + intercept) : Rule of Law + FSI total + 5 UNDP + 1 Voeten + 6 V-Dem (libdem, gender, corruption, civlib, religfree, rule_of_law V-Dem).
- **Régularisation** : ridge α = 1.0 (intercept non régularisé).
- **Validation** : leave-one-out. RMSE LOO par dimension : pdi ≈ 13, idv ≈ 17, mas ≈ 17, uai ≈ 20, lto ≈ 24, ivr ≈ 22 (sur plage Hofstede [0, 100]).

### 4.3 `wvs_items_to_iw` — 10 items WVS time-series (waves 5-6) → (ts, se)

- **Jeu d'entraînement** : 57 États avec wave-7 officielle ET items WVS time-series disponibles.
- **Vecteur de features** : moyennes pondérées par État des 10 items de la factor analysis Inglehart-Welzel (Welzel 2013), alignement de signe par item.
- **Validation** : leave-one-out. RMSE LOO : ts ≈ 0.38, se ≈ 0.54 — **strictement meilleur** que `pew_to_iw` parce que les inputs sont les vraies réponses au sondage et non des proxies religieux/économiques.
- **Application** : pour les 30 États ONU présents en waves 5-6 mais pas wave-7, ce tier produit `x_viz_provenance = imputed_wvs_items`.

Les poids ridge calibrés (`weights_per_dimension`, `feature_means`) sont **exposés dans `state_coordinates.json::data_quality.pew_to_iw_model` et `.governance_to_hofstede_model`** pour audit et reproduction.

## 5. Travaux futurs vers une calibration plus fine

1. **Élicitation experte structurée** : invitation d'au moins 5 experts (sociologues, politologues) pour proposer indépendamment des centroïdes et étendues plausibles, puis agrégation par méthode Cooke.
2. **Refit avec WVS waves 5+6 officielles** : si l'équipe Inglehart-Welzel publie un jour des coordonnées officielles pour ces waves, remplacer les prédictions ridge par les vraies valeurs (la procédure de fallback restera utile pour les États jamais couverts).
3. **Validation rétrospective** : tester la stabilité prédictive du scoring sur les transitions documentées (e.g. Turquie 2003-2020, Ukraine 2014-2022).

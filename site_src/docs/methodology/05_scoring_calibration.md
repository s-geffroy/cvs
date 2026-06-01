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

## 4. Travaux futurs vers une calibration

1. **Élicitation experte structurée** : invitation d'au moins 5 experts (sociologues, politologues) pour proposer indépendamment des centroïdes et étendues plausibles, puis agrégation par méthode Cooke.
2. **Calibration externe** : régression des `wₛ` contre indicateurs Pew/WGI/FSI (déjà partiellement fait, cf. [doc 12](12_empirical_validation.md)) pour identifier les poids optimaux.
3. **Validation rétrospective** : tester la stabilité prédictive du scoring sur les transitions documentées (e.g. Turquie 2003-2020, Ukraine 2014-2022).

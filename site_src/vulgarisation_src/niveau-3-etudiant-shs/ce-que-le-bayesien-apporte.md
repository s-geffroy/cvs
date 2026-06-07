---
title: Ce que le bayésien apporte (sans dériver)
---

cvs se présente comme un **pipeline bayésien**. Cette page explique **ce que ça veut dire concrètement** sans aucune formule (toutes les démonstrations sont sur le site principal).

## Bayésien = on part d'un prior, on confronte aux données, on publie un posterior

### 1. Un **prior** : la taxonomie de Huntington

cvs ne **part** pas d'un tableau blanc. Il part de la **carte de Huntington** (11 familles civilisationnelles enrichies). Cette carte est un **prior** : une croyance de départ sur le découpage du monde.

### 2. Des **données** : WVS + Hofstede + Inglehart-Welzel

Les enquêtes mondiales fournissent, pour chaque pays, une grande quantité de **mesures** : 6 chiffres Hofstede, ~250 questions WVS, 2 coordonnées Inglehart-Welzel.

### 3. Un **posterior** : le vecteur d'affiliation civilisationnelle

Pour chaque pays, cvs calcule un **vecteur** qui dit « voici, à la lumière des données, à quel point ce pays appartient à chaque famille du prior ».

C'est un **mélange** (au sens probabiliste : mixture model), pas une affectation dure. C'est ce qui fait que la France n'est pas « occidentale » au sens binaire, mais « occidentale à 70 %, latine à 10 %, etc. ».

## Pourquoi le bayésien plutôt qu'un clustering classique ?

| Approche | Caractéristique | Limite |
|---|---|---|
| **Clustering classique (k-means)** | On ne **part** de rien, on laisse l'algo trouver des groupes | Les groupes sont **arbitraires** et peu interprétables |
| **Classification supervisée** | On apprend à reproduire un découpage donné | Pas de **doute** : un pays est affecté à un cluster, point |
| **Bayésien (mélange)** | On part d'un prior théorique, on le révise avec les données, on publie l'**incertitude** | Plus complexe à implémenter, demande des choix explicites |

cvs publie aussi un **baseline non-supervisé** (k-means + HDBSCAN-lite, cf. [doc 14](../../methodology/14_baseline_unsupervised/)) **pour comparaison**. Si les clusters non-supervisés diffèrent énormément du prior huntingtonien, c'est un signal que le prior est mauvais — et **cvs le publie**.

## Le second moment `M(s)` : ce qui n'existe pas chez Huntington

En physique des milieux continus, le **second moment** d'un objet décrit sa **dispersion autour de son centre**. cvs reprend cette idée pour mesurer, par État, **à quel point un pays est intérieurement « tendu »** (présence de sous-cultures, dispersion des réponses WVS).

> Un pays homogène a un `M(s)` faible.
>
> Un pays composite (Inde, Russie, Suisse) a un `M(s)` élevé.

C'est **précisément** ce que Huntington évacuait. Voir [doc 09](../../methodology/09_civilizational_second_moment/) du site principal pour le formalisme.

## Les choix de calibration

cvs fait plusieurs **choix de calibration** explicites :

1. **`β`** (le « softmax » qui transforme des distances en probabilités) — sa valeur est défendue dans [doc 05](../../methodology/05_scoring_calibration/) et **testée** par sweep dans [doc 13](../../methodology/13_sensitivity_analysis/).
2. **`(α, β, γ)`** (les poids de la distance hybride) — également testés par sweep.
3. **Méthode de désambiguïsation** pour les pays charnières — explicite dans [doc 08 §3.4](../../methodology/08_civilizational_basis/).

Aucun de ces choix n'est « la vérité » ; ils sont tous **publiés**, **discutés** et **testés en sensibilité**.

## Validation empirique externe

cvs ne se contente pas de **publier des chiffres** : il vérifie qu'ils **corrèlent** avec des sources externes indépendantes :

- **Pew** (composition religieuse 2020)
- **World Bank WGI** (Rule of Law 2022)
- **Fund For Peace FSI** (Fragility States Index 2024)

Les coefficients de corrélation de Spearman + intervalles de confiance bootstrap sont publiés en [doc 12](../../methodology/12_empirical_validation/).

## Quand les données manquent : le posterior **dégénère** vers le prior

Sur 193 États membres de l'ONU, seuls ~60 sont mesurés par WVS *et* Hofstede. Pour les ~130 autres, la cascade d'imputation de cvs ([doc 16](../../methodology/16_imputation_cascade/)) procède en trois temps :

1. **Observation directe** quand elle existe ;
2. **Calibration** depuis une source corrélative publique (composition religieuse Pew, indicateurs de gouvernance WGI/FSI) si la régression est statistiquement défendable ;
3. **Repli sur le centroïde de civilisation** sinon — `x = μ(civ)` avec la covariance Σ(civ) intégralement reportée comme ellipse d'incertitude.

Le tier 3 est strictement bayésien : sans observation, le posterior **dégénère** vers le prior. Ce n'est pas un bug, c'est exactement ce que dicte la règle de mise à jour. Chaque coordonnée publiée porte un champ `provenance` qui signale son tier — pour qu'un lecteur ne confonde jamais une mesure et un prior.

## En résumé : trois apports du bayésien

1. **Un prior théorique explicite** (Huntington), confronté aux données — pas un clustering aveugle.
2. **Un mélange** (pas une affectation dure) → publication de l'**incertitude** sous forme de vecteur de pourcentages.
3. **Un second moment** `M(s)` qui rend visible la **dispersion intra-pays** que les approches non-bayésiennes occultent. Sa diagonale est gonflée pour les États imputés afin que l'incertitude soit *visible* dans les invariants.

## Pour aller plus loin

- Site principal cvs : [doc 09 — Second moment](../../methodology/09_civilizational_second_moment/), [doc 12 — Validation empirique](../../methodology/12_empirical_validation/), [doc 13 — Sensibilité](../../methodology/13_sensitivity_analysis/).
- Gelman, Carlin, Stern, Rubin, *Bayesian Data Analysis*, 3ᵉ éd., pour la formalisation.

---
title: Inglehart-Welzel en 2 pages
---

## L'idée principale

Ronald **Inglehart** (1934-2021) et Christian **Welzel** sont les figures principales du projet *World Values Survey* (WVS). Ils proposent depuis les années 80 une **carte 2D** qui place les pays selon deux axes :

| Axe | Pôle 1 | Pôle 2 |
|---|---|---|
| **Vertical** | Valeurs **traditionnelles** : religion, famille, autorité | Valeurs **séculières-rationnelles** : laïcité, autorité de l'État, raison |
| **Horizontal** | Valeurs de **survie** : sécurité économique, conformité, méfiance | Valeurs d'**expression de soi** : tolérance, créativité, participation |

Cette carte est **construite empiriquement** à partir des réponses WVS (analyses factorielles). Elle évolue à chaque vague — on parle de la « carte d'Inglehart-Welzel » comme d'un objet vivant, mis à jour tous les 5 ans environ.

## La thèse de fond : la **modernisation post-matérialiste**

> Quand un pays atteint un certain niveau de sécurité économique, ses habitants se tournent vers des valeurs **post-matérialistes** (expression de soi, autonomie, environnement, démocratie participative).

C'est une thèse **développementiste** : les pays se déplaceraient « du sud-ouest au nord-est » de la carte au fur et à mesure de leur développement. La pandémie et les crises géopolitiques de 2020-2024 ont mis à mal cette linéarité.

## Pourquoi c'est utile pour cvs

- Une **carte 2D facile à visualiser** → cvs construit `B_viz = ℝ²` à partir de cet axe.
- **Compatible avec WVS** (même équipe, mêmes données) → cohérence interne.
- Permet de placer chaque pays comme un **point** sur un plan, comparable visuellement aux autres.

## Critiques principales

| Critique | Auteur clé |
|---|---|
| **Linéarité de la modernisation** : tous les pays n'évoluent pas du même côté | Acemoglu & Robinson (2012, sur d'autres bases) |
| **Eurocentrisme** : « valeurs post-matérialistes » est défini en miroir de l'Europe scandinave | Davutoğlu (2014) |
| **Stabilité contestée** : les pays ont **reculé** sur certaines dimensions (Russie, Turquie, États-Unis post-2016) | Norris (2020) |
| **Construction factorielle** : les deux axes sont des **construits** d'analyse factorielle, pas des choses « réelles » | Schwartz (2014) |
| **Données manquantes** : la couverture WVS est très inégale (peu de pays africains, Pacifique sous-représenté) | Heath et al. (2019) |

## Comment cvs traite ces critiques

- **Linéarité** : cvs **ne** suppose **pas** d'évolution dans le temps — c'est un **instantané** statique.
- **Eurocentrisme** : cvs **ne classe pas** les pays sur un axe de « modernité ». Les axes sont des **dimensions descriptives**, pas des échelles normatives.
- **Stabilité** : la **date de capture** est publiée explicitement (vague 7 de WVS, 2017-2022).
- **Construction factorielle** : cvs publie aussi **B_score** (les 6 dimensions de Hofstede) en parallèle, pour ne pas dépendre d'un seul construit.
- **Données manquantes** : cvs marque explicitement les pays **non couverts** (≈130/190).

## La carte en 2026

> Une version récente (vague 7) place :
>
> - **Suède, Norvège, Pays-Bas** dans le coin nord-est (séculier + expression de soi).
> - **États-Unis** plutôt à l'est (expression de soi) mais avec une teinte **traditionnelle** marquée (singularité parmi les pays riches).
> - **Russie, Bulgarie** dans le coin nord-ouest (séculier + survie).
> - **Égypte, Maroc, Jordanie** dans le coin sud-ouest (tradition + survie).
> - **Mexique, Brésil, Colombie** plutôt au centre-sud (tradition modérée + expression de soi).

## Pour aller plus loin

- Inglehart, *Cultural Evolution: People's Motivations are Changing, and Reshaping the World*, 2018.
- Welzel, *Freedom Rising: Human Empowerment and the Quest for Emancipation*, 2013.
- Site WVS : <https://www.worldvaluessurvey.org/>
- Site principal cvs : [doc 08 — Base civilisationnelle](../../methodology/08_civilizational_basis/).

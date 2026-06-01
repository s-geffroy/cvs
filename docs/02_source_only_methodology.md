# 02 — Méthodologie *source-only*

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md`](07_ethics_publication_policy.md).

## 1. Principe directeur

Le projet est **strictement *source-only*** : aucune inférence basée sur des données individuelles, et aucune utilisation de sources non-publiques. Cf. également [doc 07 — Éthique de publication](07_ethics_publication_policy.md) pour les règles d'inférence interdites.

Concrètement, **chaque valeur publiée** doit être traçable à :

1. Un dataset international public (WVS, Hofstede Insights, Pew, World Bank WGI, FFP FSI), ou
2. Une statistique officielle publiée par un État ou une organisation intergouvernementale, ou
3. Un dataset de frontières public sous licence permissive (Natural Earth = domaine public, geoBoundaries = CC-BY).
4. **Jamais** : questionnaires individuels, graphes sociaux privés, scraping non autorisé, données nominatives.

## 2. Périmètre des sources utilisées

| Source | Type | Année | Licence | Rôle dans `cvs/` |
|---|---|---|---|---|
| Huntington (1996) | Académique — théorie | 1996 | Citation académique | Vocabulaire civilisationnel (8 macro + 3 extensions). |
| Inglehart-Welzel (2005, 2010) | Académique — analyse factorielle | 2005, 2010 | Citation académique | Justifie B_viz (axes TS, SE). |
| WVS wave 7 | Dataset public | 2017-2022 | CC-BY 4.0 | Coordonnées IW par pays. |
| Hofstede et al. (2010) | Dataset public + théorie | 2010 (mise à jour 2015) | Usage scientifique | Définit B_score (6 axes). |
| Natural Earth | Datasets géo public | continu | Domaine public | Géométries ADM0 publiées. |
| geoBoundaries | Datasets géo public | continu | CC-BY 4.0 | Géométries ADM1 préparées. |
| Smith (2012), Hau'ofa (1994), UN UNPFII | Académique + institutionnel | divers | Citation académique | Justifie les extensions Indigenous, Oceanian. |
| Pew Religious Composition | Dataset public | 2020 | Citation académique | Validation externe (doc 12). |
| World Bank WGI | Dataset public | annuel | CC-BY 4.0 | Validation externe (doc 12). |
| Fund For Peace FSI | Dataset public | annuel | Méthodologie publique | Validation externe (doc 12). |

Les **données canoniques** utilisées par le pipeline sont stockées sous `data_sources/`, avec citation et URL dans chaque fichier.

## 3. Extension préparée : littérature académique structurée comme source

Le projet **prépare** (sans encore activer) l'usage de la littérature académique comme **source structurée** : extraction de records bibliographiques avec citation, claim, evidence_level. Cette extension ne change pas la nature *source-only* — la littérature est publique — mais ajoute une couche d'analyse structurée. À implémenter au besoin.

## 4. Conséquences opérationnelles

- Tout pipeline qui scraperait des sources privées **serait refusé en review**.
- Tout artefact publié **doit** porter `source_refs[]` pointant vers la bibliographie de `taxonomies/macro_civilizations.v2.json`.
- Toute modification d'une source canonique impose une **bump de version** des artefacts dérivés et un changelog.

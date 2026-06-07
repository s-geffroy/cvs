# 02 — Méthodologie *source-only*

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md`](07_ethics_publication_policy.md).

## 1. Principe directeur

Le projet est **strictement *source-only*** : aucune inférence basée sur des données individuelles, et aucune utilisation de sources non-publiques. Cf. également [doc 07 — Éthique de publication](07_ethics_publication_policy.md) pour les règles d'inférence interdites.

Concrètement, **chaque valeur publiée** doit être traçable à :

1. Un dataset international public (WVS, Hofstede Insights, Pew, World Bank WGI, FFP FSI), ou
2. Une statistique officielle publiée par un État ou une organisation intergouvernementale, ou
3. Un dataset de frontières public sous licence permissive (Natural Earth = domaine public, geoBoundaries = CC-BY).
4. **Jamais** : questionnaires individuels, graphes sociaux privés, scraping non autorisé, données nominatives.

### 1.1 Stratification *source-only* en cascade (V2)

Depuis l'introduction de la cascade d'imputation ([doc 16](16_imputation_cascade.md)), la doctrine *source-only* est stratifiée selon la qualité observationnelle, sans la diluer :

| Tier | Nature | Sources effectivement utilisées |
|---|---|---|
| `observed` | Sondage culturel direct | WVS wave 7 (IW), Hofstede Insights 2010 (B_score) |
| `imputed_wvs_items` | Sondage WVS direct + factor analysis ridge calibrée sur wave-7 | WVS Time-Series 1981-2022 (waves 5-6) — 10 items Inglehart-Welzel |
| `imputed_pew` | Régression ridge auxiliaire vers IW | Pew composition religieuse complète (7 proportions) + UNDP HDR 2025 + UN voting Voeten + V-Dem v16 |
| `imputed_governance` | Régression ridge auxiliaire vers Hofstede | WGI Rule of Law + FSI 2024 + UNDP HDR 2025 + UN voting Voeten + V-Dem v16 |
| `centroid_prior` | Prior théorique de civilisation | Huntington (1996) + barycentres empiriques |

Aucune valeur n'est *inventée* : un État `centroid_prior` se voit attribuer la position du barycentre civilisationnel — la covariance du centroïde est intégralement reportée comme ellipse d'incertitude, et le tenseur du second moment voit sa diagonale gonflée d'autant. La cascade ne contredit donc pas la règle *source-only* ; elle en explicite la hiérarchie.

**Couverture résultante au 2026-06-07** : 193/193 États ONU avec `x_viz` et `x_score` non-nuls ; **0 État dans le tier `centroid_prior`** parce qu'au moins une source auxiliaire publique alimente chaque État. Cf. `data_sources/un_members/coverage_report.md` pour le décompte exact par tier.

## 2. Périmètre des sources utilisées

| Source | Type | Année | Licence | Rôle dans `cvs/` |
|---|---|---|---|---|
| Huntington (1996) | Académique — théorie | 1996 | Citation académique | Vocabulaire civilisationnel (8 macro + 3 extensions). |
| Inglehart-Welzel (2005, 2010) | Académique — analyse factorielle | 2005, 2010 | Citation académique | Justifie B_viz (axes TS, SE). |
| WVS wave 7 | Dataset public | 2017-2022 | CC-BY 4.0 | Coordonnées IW officielles (60 États). |
| WVS Time-Series 1981-2022 v5.0 | Dataset public | 2022 | CC-BY 4.0 | Extension IW waves 5-6 via ridge sur 10 items (+30 États). |
| Hofstede et al. (2010) | Dataset public + théorie | 2010 (mise à jour 2015) | Usage scientifique | Définit B_score (6 axes). 63 États couverts. |
| Natural Earth | Datasets géo public | continu | Domaine public | Géométries ADM0 publiées. |
| geoBoundaries | Datasets géo public | continu | CC-BY 4.0 | Géométries ADM1 préparées. |
| Smith (2012), Hau'ofa (1994), UN UNPFII | Académique + institutionnel | divers | Citation académique | Justifie les extensions Indigenous, Oceanian. |
| Pew religious composition (7 catégories) | Dataset public | 2020 | Citation académique | Feature pour `pew_to_iw` (182 États). |
| World Bank WGI Rule of Law | Dataset public | 2022 | CC-BY 4.0 | Feature pour `governance_to_hofstede` (63 États). |
| Fund For Peace FSI | Dataset public | 2024 | Méthodologie publique | Feature pour `governance_to_hofstede` (63 États). |
| **UNDP Human Development Report 2025** | Dataset public | 2023 | UNDP terms | HDI (193), GII (172), scolarité (191). Source pivot qui élimine le centroïde prior. |
| **Voeten/Strezhnev/Bailey UN GA voting** | Harvard Dataverse | 2025 | CC-0 | Idealpoint par État (192). Couvre les micro-États hors UNDP. |
| **V-Dem Varieties of Democracy v16** | Académique + dataset | 2025 | CC-BY 4.0 | 12 indices institutionnels (172 États). Améliore la calibration. |

Les **données canoniques** utilisées par le pipeline sont stockées sous `data_sources/`, avec citation et URL dans chaque fichier.

## 3. Extension préparée : littérature académique structurée comme source

Le projet **prépare** (sans encore activer) l'usage de la littérature académique comme **source structurée** : extraction de records bibliographiques avec citation, claim, evidence_level. Cette extension ne change pas la nature *source-only* — la littérature est publique — mais ajoute une couche d'analyse structurée. À implémenter au besoin.

## 4. Conséquences opérationnelles

- Tout pipeline qui scraperait des sources privées **serait refusé en review**.
- Tout artefact publié **doit** porter `source_refs[]` pointant vers la bibliographie de `taxonomies/macro_civilizations.v2.json`.
- Toute modification d'une source canonique impose une **bump de version** des artefacts dérivés et un changelog.

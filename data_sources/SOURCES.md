# Sources & Bibliographie — `cvs/`

> Toutes les sources listées ici sont **publiques**. Aucune donnée individuelle, aucun nom propre n'est utilisé pour inférer un profil personnel. Voir [`docs/07_ethics_publication_policy.md`](../docs/07_ethics_publication_policy.md).

## 1. Vocabulaire civilisationnel

### Huntington (1996)

- **Citation** : Huntington, S. P. (1996). *The Clash of Civilizations and the Remaking of World Order*. Simon & Schuster.
- **id** : `huntington_1996`
- **Usage** : fournit les 8 macro-civilisations canoniques (Western, Orthodox, Islamic, Sinic, Hindic, Japanese, Latin American, African). Concept de « fault lines ».
- **Limites** : critiqué par Sen (2006), Said (2001) pour réductionnisme. Utilisé comme vocabulaire de référence et non comme modèle prédictif.
- **Licence** : œuvre sous copyright — citation académique uniquement, aucun extrait reproduit.

## 2. Assise empirique culturelle

### Inglehart & Welzel (2005, 2010)

- **id** : `inglehart_welzel_2005`
  - Inglehart, R., & Welzel, C. (2005). *Modernization, Cultural Change, and Democracy: The Human Development Sequence*. Cambridge University Press.
- **id** : `inglehart_welzel_2010`
  - Inglehart, R., & Welzel, C. (2010). « Changing Mass Priorities: The Link Between Modernization and Democracy ». *Perspectives on Politics*, 8(2), 551-567.
- **Usage** : analyse factorielle qui justifie les axes `Traditional ↔ Secular-Rational` (TS) et `Survival ↔ Self-Expression` (SE) — fondement de `B_viz = ℝ²`.

### World Values Survey wave 7 (2017-2022)

- **id** : `wvs_wave7_2022`
- **Citation** : Haerpfer, C., Inglehart, R., Moreno, A., Welzel, C., Kizilova, K., Diez-Medrano J., Lagos, M., Norris, P., Ponarin E. & Puranen B. (eds.) (2022). *World Values Survey: Round Seven – Country-Pooled Datafile Version 5.0*. Madrid, Spain & Vienna, Austria: JD Systems Institute & WVSA Secretariat. doi:10.14281/18241.20.
- **URL** : https://www.worldvaluessurvey.org/WVSContents.jsp
- **Licence** : **CC-BY** (citation requise).
- **Usage** : coordonnées IW empiriques par pays (`data_sources/inglehart_welzel/cultural_map_wave7.json`).

## 3. Dimensions psycho-sociales

### Hofstede, Hofstede, Minkov (2010)

- **id** : `hofstede_2010`
- **Citation** : Hofstede, G., Hofstede, G. J., & Minkov, M. (2010). *Cultures and Organizations: Software of the Mind* (3rd ed.). McGraw-Hill.
- **URL** : https://www.hofstede-insights.com/country-comparison-tool
- **Licence** : usage scientifique. Les valeurs consolidées par Hofstede Insights (2015) sont largement référencées dans la littérature académique et peuvent être citées avec attribution. Reproduction commerciale interdite.
- **Usage** : 6 dimensions (`PDI, IDV, MAS, UAI, LTO, IVR`) par pays — fondement de `B_score = ℝ⁶` (`data_sources/hofstede/dimensions_v2015.json`).

## 4. Extensions (civilisations sous-représentées chez Huntington)

### Indigène (Indigenous)

- **id** : `smith_2012`
  - Smith, L. T. (2012). *Decolonizing Methodologies: Research and Indigenous Peoples* (2nd ed.). Zed Books.
- **id** : `un_unpfii`
  - United Nations Permanent Forum on Indigenous Issues. https://www.un.org/development/desa/indigenouspeoples/

### Océanienne (Oceanian)

- **id** : `hauofa_1994`
  - Hau'ofa, E. (1994). « Our Sea of Islands ». *The Contemporary Pacific*, 6(1), 147-161.

## 5. Sources géométriques

### Natural Earth

- **id** : `natural_earth_5_1`
- **URL** : https://www.naturalearthdata.com/
- **Licence** : **domaine public**.
- **Usage** : géométries ADM0 publiées sur GitHub Pages.

### geoBoundaries

- **id** : `geoboundaries_6_0`
- **Citation** : Runfola, D. et al. (2020). geoBoundaries: A global database of political administrative boundaries. *PLOS ONE*, 15(4).
- **URL** : https://www.geoboundaries.org/
- **Licence** : **CC-BY 4.0**.
- **Usage** : géométries ADM1 versionnées dans `data_sources/geoboundaries/adm1/` — **prêtes mais non utilisées** en V1 (cf. `docs/04_adm1_preparation_policy.md`).

### GADM — **INTERDIT EN PUBLICATION**

- **URL** : https://gadm.org/
- **Licence** : restriction de redistribution.
- **Politique** : utilisé uniquement en lecture locale pour validation interne, jamais publié dans `dist/` ni `site_src/docs/assets/data/`. Garde-fou : `assert_geometry_source_in_allowlist` dans `apps/site_builder/guards.py`.

## 6. Pour contraste / mention bibliographique

- Toynbee, A. (1934-1961). *A Study of History* (12 volumes). Oxford University Press.
- Quigley, C. (1961). *The Evolution of Civilizations*. Macmillan.
- Melko, M. (1969). *The Nature of Civilizations*. Porter Sargent.
- Sen, A. (2006). *Identity and Violence: The Illusion of Destiny*. W. W. Norton.

## 7. Sources auxiliaires pour la cascade d'imputation V2

Le chapitre méthodologique [`docs/16_imputation_cascade.md`](../methodology/16_imputation_cascade.md) décrit la cascade `observed > imputed > centroid_prior`. Les sources auxiliaires ci-dessous étendent la couverture *observée* au-delà des 63 États communs à Hofstede/Pew/WGI/FSI. **Trois ont été effectivement ingérées en 2026-06-07 et alimentent la cascade**, deux restent **à friction**.

### 7.1 ✅ INGÉRÉE — UNDP HDR 2025 (Human Development Report)

- **Source** : United Nations Development Programme, *Human Development Report 2025 — Composite Indices Complete Time Series*.
- **id** : `undp_hdr_2025`
- **URL** : `https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_complete_time_series.csv` (direct, sans inscription)
- **Licence** : libre réutilisation avec citation (UNDP terms of use).
- **Couverture** : **193/193 États ONU** pour HDI, 172/193 pour GII, 191/193 pour années de scolarité.
- **Apport** : c'est la source qui **élimine la quasi-totalité du fallback centroïde** pour x_score (130 États basculent de `centroid_prior` à `imputed_governance`). Aussi alimente l'imputation x_viz via Pew_to_IW.
- **Fichiers** : `data_sources/undp/HDR25_Composite_indices_complete_time_series.csv` (brut, 2 MB) + `data_sources/undp/hdr_2023.json` (extraction).
- **Loader** : `apps/basis_builder/load_undp_hdr.py`.

### 7.2 ✅ INGÉRÉE — UN voting Voeten Affinity of Nations

- **Source** : Bailey, M.A., Strezhnev, A., Voeten, E. (2017). « Estimating Dynamic State Preferences from United Nations Voting Data ». *Journal of Conflict Resolution*, 61(2), 430-456.
- **id** : `voeten_un_voting_2025`
- **URL** : `https://dataverse.harvard.edu/api/access/datafile/13642025` (Harvard Dataverse, direct sans authentification)
- **Licence** : CC-0 (public domain).
- **Couverture** : **192/193 États ONU** (latest year 2025 pour 190 d'entre eux).
- **Apport** : signal politique direct indépendant du développement, alimente l'imputation pour les 2 micro-États (MCO, PRK) que UNDP HDR ne couvrait pas. **Élimine le centroid_prior résiduel**.
- **Fichiers** : `data_sources/un_voting/Idealpointestimates1946-2025.tab` (brut, 1 MB) + `voeten_idealpoints_latest.json` (extraction).
- **Loader** : `apps/basis_builder/load_un_voting.py`.

### 7.3 ✅ INGÉRÉE — V-Dem Varieties of Democracy

- **Source** : V-Dem Institute, dataset bundled in the R package `vdeminstitute/vdemdata` (GitHub master branch ; CC-BY 4.0).
- **id** : `vdem_v_country_year_2025`
- **URL d'extraction** : `https://raw.githubusercontent.com/vdeminstitute/vdemdata/master/data/vdem.RData` (33 MB, format R)
- **Licence** : CC-BY 4.0.
- **Couverture** : **172/193 États ONU** sur 12 indices clés retenus (libdem, partipdem, delibdem, egaldem, gender_empowerment, corruption, civil_liberties, religious_freedom, rule_of_law, equal_access_power, transparent_laws, private_civil_liberties).
- **Apport** : améliore la qualité de la calibration (notamment SE axis : RMSE 0.731 → 0.625) et offre une seconde mesure indépendante du rule of law et de l'égalité de genre. **Ne change pas la topologie de couverture** (déjà à 0 prior) mais affine les imputations.
- **Fichiers** : `data_sources/vdem/vdem_latest_year.json` (extraction).
- **Loader** : `apps/basis_builder/load_vdem.py`. Le `.RData` n'est pas tracké git (33 MB) ; doit être re-téléchargé pour reproduire l'extraction.
- **Procédure d'extraction** : container Docker avec `pip install pyreadr` (one-shot, hors-image base), script de transformation `.RData` → JSON sélectif (12 indices, latest year per ISO3).

### 7.4 ⚠️ À FRICTION — WVS waves 5, 6, 7 fusionnées

- **Source** : World Values Survey Association, *Time-Series 1981-2022*.
- **id prévu** : `wvs_time_series_2022`
- **URL** : `https://www.worldvaluessurvey.org/WVSDocumentationWVL.jsp` (formulaire d'inscription avec email obligatoire)
- **Licence** : CC-BY (citation requise).
- **Couverture cible** : ~95 États avec `x_viz = observed` (vs. 62 sur la seule vague 7).
- **Apport prévu** : passer 33 États supplémentaires de `imputed_pew` à `observed` pour x_viz.
- **Statut** : pas ingéré automatiquement (inscription manuelle requise). Recherche d'un miroir public (OSF, GESIS) infructueuse au 2026-06-07. Si l'utilisateur souhaite fermer cette friction, télécharger manuellement et poser `cultural_map_pooled.csv` dans `data_sources/inglehart_welzel/` — l'extension du loader pour gérer 3 waves est ~30 lignes de code.

### 7.5 ⚠️ À FRICTION — Pew composition religieuse complète

- **Source** : Pew Research Center, *Religious Composition by Country, 2010-2050*.
- **id prévu** : `pew_religion_full_2022`
- **URL** : https://www.pewresearch.org/religion/feature/religious-composition-by-country-2010-2050/ (HTTP 403 en accès direct, contenu derrière JS)
- **Couverture cible** : ~200 États avec vecteur (christian, muslim, hindu, buddhist, jewish, folk, unaffiliated, other) sommant à 1.
- **Apport prévu** : remplace le scalaire `dominant_share_pct` actuel par 8 proportions, raffine la calibration `pew_to_iw`. **Pas d'impact sur la couverture** (déjà 0 prior).
- **Statut** : extraction automatique bloquée par 403 + JS. Si besoin, l'utilisateur peut télécharger manuellement le CSV depuis l'outil Excel/CSV publié par Pew (parfois disponible dans la section « download »).

### 7.6 ❎ NON INGÉRÉE — UNESCO World Heritage

- **Source** : UNESCO World Heritage Centre.
- **id** : `unesco_heritage_2024`
- **URL** : https://whc.unesco.org/en/syndication
- **Apport** : source de validation croisée pour la taxonomie (distribution sites par civilisation). **Pas d'apport à la cascade d'imputation** car non-quantitatif au niveau État.
- **Statut** : non prioritaire, peut être ajouté quand nécessaire pour la validation empirique (cf. [doc 12](../methodology/12_empirical_validation.md)).

### 7.7 État résultant de la cascade après V2.1 (sources étendues)

Sur les 193 États membres de l'ONU :

| Tier | x_viz | x_score |
|---|---|---|
| `observed` | 60 (WVS wave 7) | 52 (Hofstede complet) |
| `observed_with_dim_imputation` | — | 9 (Hofstede partiel) |
| `imputed_pew` (Pew + UNDP + UN voting + V-Dem) | 133 | — |
| `imputed_governance` (WGI + FSI + UNDP + UN voting + V-Dem) | — | 132 |
| `centroid_prior` | **0** | **0** |

L'angle mort coverage est entièrement supprimé. Les améliorations futures porteront sur la qualité (lever les frictions WVS/Pew pour réduire la zone `imputed_*` au profit de la zone `observed`).

## 8. Catalogue machine-lisible

Voir aussi :
- `../raw/data_sources/public_sources_catalog.v1.json`
- `../raw/data_sources/geometry_source_registry.v1.json`

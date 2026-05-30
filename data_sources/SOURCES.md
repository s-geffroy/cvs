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

## 7. Catalogue machine-lisible

Voir aussi :
- `../raw/data_sources/public_sources_catalog.v1.json`
- `../raw/data_sources/geometry_source_registry.v1.json`

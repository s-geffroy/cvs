# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added — WVS Time-Series + Pew composition complète : tier `imputed_wvs_items` (2026-06-07, suite)

- **WVS Time-Series 1981-2022 v5.0** (1.3 GB CSV téléchargé par l'utilisateur,
  posé dans `data_sources/inglehart_welzel/wvs_time_series_1981_2022.csv`,
  hors-tracking git via `.gitignore`).
- **Extracteur** `apps/basis_builder/_wvs_extraction.py` — streame le CSV
  (un milliard de cellules), agrège les **10 items de la factor analysis
  Inglehart-Welzel** par pays par vague (Welzel 2013, ch. 2), résout les
  codes COW alpha vers ISO3 (table de 80 mappings), et calibre une
  **régression ridge sur les 57 États de l'intersection wave-7 officiel
  ∩ WVS time-series** pour prédire `(ts, se)` sur les 36 États
  additionnels présents seulement en waves 5-6. RMSE LOO : ts=0.38,
  se=0.54.
- **Nouveau tier `imputed_wvs_items`** dans la cascade (entre `observed`
  et `imputed_pew`) — 30 États ONU supplémentaires gagnent un `x_viz`
  méthodologiquement aligné sur la chaîne de calcul WVS, sans dépendre
  des proxies religieux/économiques. `load_iw.py` lit
  `cultural_map_pooled.json` quand il est présent.
- **Pew composition complète** (`data_sources/pew/religious_composition_full_2020.csv`,
  ~52 KB déposé par l'utilisateur). Extracteur
  `apps/basis_builder/_pew_extraction.py` mappe les codes UN M49 vers
  ISO3 (matching par nom + alias table) et produit
  `religious_composition_full_2020.json` avec les **7 proportions**
  (Christians, Muslims, Hindus, Buddhists, Jews, Unaffiliated, Other)
  pour 182/193 États ONU. `load_pew.py` réécrit pour exposer
  `PewProfile` avec ces 7 champs. `pew_to_iw.py` remplace les dummies
  one-hot du `dominant_group` par les proportions directes — RMSE
  pew_to_iw : ts 0.485 → 0.482, se 0.625 → 0.618.

**Distribution finale de provenance** :

| Tier | `x_viz` | `x_score` |
|---|---|---|
| `observed` (WVS wave-7 / Hofstede) | 60 | 52 |
| `observed_with_dim_imputation` | — | 9 |
| `imputed_wvs_items` (WVS 5-6 ridge) | **30** | — |
| `imputed_pew` (Pew + UNDP + UN voting + V-Dem) | 103 | — |
| `imputed_governance` (WGI + FSI + UNDP + UN voting + V-Dem) | — | 132 |
| `centroid_prior` | **0** | **0** |

Soit **90 / 193 États** avec un `x_viz` directement adossé à des
données WVS (60 wave-7 officielles + 30 calibrées sur items WVS) — 47 %
de la couverture observée vs 31 % avant l'extension WVS+Pew.

### Added — Sources externes ingérées : zéro `centroid_prior` (2026-06-07, suite)

Trois sources publiques étendues ingérées pour combler l'« angle mort »
résiduel (États reposant sur le prior centroïde faute d'observation) :

- **UNDP HDR 2025** (`data_sources/undp/`) — Composite Indices Time Series
  téléchargé directement depuis `hdr.undp.org`. 193/193 États ONU pour HDI,
  172/193 pour GII. Loader `apps/basis_builder/load_undp_hdr.py`. **À elle
  seule, fait basculer 130 États de `centroid_prior` à `imputed_governance`
  pour `x_score`**.
- **UN voting Voeten/Strezhnev/Bailey** (`data_sources/un_voting/`) —
  ideal-point estimates 1946-2025 téléchargés directement depuis Harvard
  Dataverse (CC-0). 192/193 États ONU avec données 2025. Loader
  `apps/basis_builder/load_un_voting.py`. **Élimine les 2 derniers
  `centroid_prior` pour `x_viz` (MCO, PRK)**.
- **V-Dem Varieties of Democracy** (`data_sources/vdem/`) — 12 indices
  extraits depuis `vdem.RData` du package R officiel
  (`vdeminstitute/vdemdata`, CC-BY 4.0), via `pyreadr` en container. 172/193
  États ONU. Loader `apps/basis_builder/load_vdem.py`. Améliore les RMSE de
  calibration (notamment SE axis : 0.731 → 0.625).

Les régressions ridge `pew_to_iw` (axes IW) et `governance_to_hofstede`
(6 dimensions Hofstede) sont étendues à 18 et 15 features respectivement,
avec masking par-feature pour les sources manquantes (la moyenne du jeu
d'entraînement remplace la valeur absente sans réduire l'intersection).

**Résultat final** : sur 193 États ONU, distribution de provenance :

| Tier | `x_viz` | `x_score` |
|---|---|---|
| `observed` | 60 | 52 |
| `observed_with_dim_imputation` | 0 | 9 |
| `imputed_pew` | 133 | 0 |
| `imputed_governance` | 0 | 132 |
| `centroid_prior` | **0** | **0** |

L'angle mort coverage est supprimé. Améliorations futures = passer de
`imputed_*` à `observed` en ingérant WVS waves 5+6 (~30 États
supplémentaires en observé) et Pew composition complète — toutes deux à
friction (inscription/403) et donc non automatisables.

`data_sources/SOURCES.md` §7 mis à jour avec statut par source.

### Added — Cascade d'imputation : un vecteur pour les 193 États ONU (2026-06-07)

- **Cascade `observed` > `imputed_*` > `centroid_prior`** dans
  `apps/basis_builder/projector.py` : pour chaque ISO3 ONU, la coordonnée
  `x_viz` ∈ ℝ² et `x_score` ∈ ℝ⁶ est résolue selon trois tiers de qualité
  décroissante. **Résultat : `state_coordinates.json` contient désormais
  193 entrées non nulles** (vs. 70 auparavant ; vérifié par
  `tests/test_imputation_cascade.py`).
- **Taxonomie complétée aux 193 ONU** :
  `taxonomies/macro_civilizations.v2.json` voit 121 nouveaux
  `member_states` et 9 nouveaux `ambiguous_cases` injectés par
  `apps/basis_builder/_taxonomy_completion.py` (heuristique déterministe
  géographie + religion dominante + Huntington 1996). 187/193 ont un
  `curated_civilization` direct ; 6 cas réellement ambigus (BIH, CIV, ISR,
  KOR, LBN, TCD) restent en `ambiguous` avec `curated_civilizations_competing`.
- **Loaders auxiliaires** : `apps/basis_builder/load_pew.py`,
  `load_wgi.py`, `load_fsi.py` exposent les profils Pew, WGI et FSI sous
  forme de `dataclass` consommables par la cascade.
- **Modules de calibration** sous `packages/civvec_core/imputation/` :
  - `pew_to_iw.py` — régression ridge Pew → (ts, se), validation LOO.
  - `governance_to_hofstede.py` — six régressions ridge WGI+FSI → Hofstede 6D,
    RMSE par dimension.
  - `centroid_prior.py` — fallback `x = μ(civ)` avec covariance Σ(civ).
- **`moments.py` tolère `x_score` imputé** : la diagonale de M(s) est
  gonflée par `diag(σ_prior²)` (centroïde) ou `diag(RMSE_dim²)`
  (imputation gouvernance). La décomposition exposée comprend désormais
  `prior_variance_inflation`. Les 193 États produisent un M(s) fini.
- **Nouveau chapitre méthodologique** `docs/16_imputation_cascade.md`
  (miroir `site_src/docs/methodology/16_imputation_cascade.md`, ajouté à
  la nav `mkdocs.yml`). Documentations 02, 08, 09, 11, 12, 15 amendées en
  conséquence (stratification source-only, dégénérescence vers prior,
  décomposition étendue, critique de circularité H28, stratification de
  la validation empirique, glossaire de la cascade).
- **Section « Provenance des coordonnées » dans le rapport de couverture**
  (`apps/basis_builder/coverage_report.py`) — décompte par tier
  (`observed`, `observed_with_dim_imputation`, `imputed_pew`,
  `imputed_governance`, `centroid_prior`).
- **Vulgarisation** : avertissements ajoutés dans
  `site_src/vulgarisation_src/niveau-2-journaliste/ce-que-ces-chiffres-ne-disent-pas.md`
  (« tous les pays ne sont pas mesurés ») et
  `niveau-3-etudiant-shs/ce-que-le-bayesien-apporte.md` (« le posterior
  dégénère vers le prior »).
- **Tests** : `tests/test_imputation_cascade.py` — 7 tests garantissent
  193 entrées, provenance dans les tiers connus, États observés non
  dégradés, M(s) fini partout, inflation diagonale corrélée à la
  provenance.
- **Carte interactive** (`site_src/docs/assets/js/map.js`,
  `site_src/templates/map_page.md.j2`) :
  - nouveau mode de coloration « **Provenance (cascade)** » qui colore
    chaque État selon le tier (`observed` bleu foncé → `imputed_*` orange
    → `centroid_prior` gris) ;
  - **opacité variable par tier** appliquée à tous les modes : les États
    `centroid_prior` apparaissent volontairement estompés (opacité 0.42
    vs 0.82 pour `observed`) pour signaler visuellement que leur position
    n'est pas une mesure directe ;
  - popup au clic enrichi des champs `x_viz_provenance`, `x_score_provenance`
    et `fallback_civilization_id`, plus un avertissement quand au moins
    une coordonnée est imputée ;
  - **dézoom par défaut** : `zoom: 0.4`, `minZoom: 0.2` (au lieu de 1.2/1.0)
    pour afficher le monde entier d'emblée sans coupure aux bords ;
  - schémas et `civvec basis validate` étendus aux nouveaux champs
    (`data_quality.x_viz_provenance`, `x_score_provenance`,
    `x_score_sigma_prior`, `fallback_civilization_id`,
    `prior_variance_inflation` dans `state_moments.json`).

### Changed

- `schemas/macro_civilizations.schema.json` : champs `bibliography[].url`
  et `.license` acceptent désormais `null` (les livres comme Huntington
  1996 n'ont pas d'URL canonique).
- `apps/cli/basis.py::validate` valide maintenant 4 artefacts
  (taxonomie + centroïdes + state_coordinates + state_moments) au lieu
  de la seule taxonomie. Détection précoce des dérives de schéma.
- `apps/ui_streamlit/pages/3_State_Explorer.py` et
  `5_Diagnostics.py` affichent la provenance par État et les
  distributions globales par tier.

### Added — Couverture complète des États ONU + noms en français (2026-06-02)

- **Liste canonique des 193 États membres de l'ONU** dans
  `data_sources/un_members/iso3_to_name_fr.json` (ISO3 → nom court en français).
- **Complétion géométrique** : `apps/basis_builder/geometries.py` télécharge
  Natural Earth 110m **et** complète les 28 micro-États ONU absents à cette
  résolution depuis Natural Earth 50m (Andorre, Monaco, Saint-Marin,
  Liechtenstein, Malte, Singapour, Maldives, Seychelles, Maurice, Cabo Verde,
  Sao Tomé, Comores, Bahreïn, Antigua-et-Barbuda, Barbade, Dominique, Grenade,
  Sainte-Lucie, Saint-Vincent, Saint-Kitts-et-Nevis, Kiribati, Tuvalu, Nauru,
  Palaos, Îles Marshall, Micronésie, Samoa, Tonga). Le geojson final compte
  **201 features** et le champ `iso3_un_still_missing` est vide.
- **Rapport de couverture** : nouvelle commande `civvec basis coverage-report`
  qui écrit `data_sources/un_members/coverage_report.{md,json}` croisant les
  193 États ONU avec géométrie / Hofstede / Inglehart-Welzel / taxonomie
  pour matérialiser la liste des données encore à combler (132 Hofstede,
  133 IW, 127 sans civilisation curatée).
- **Noms en français sur l'ensemble des pages GitHub Pages** : nouveau
  module `apps/basis_builder/un_members.py`, injection dans le builder
  (`apps/site_builder/builder.py`) qui propage la table iso3→name_fr dans :
  - les templates `state_page.md.j2`, `states_index.md.j2`,
    `civilization_page.md.j2` (titres, breadcrumbs, tables membres et
    sous-clusters, cas ambigus) ;
  - les JSON servis aux visualisations Plotly (`state_coordinates.json`,
    `state_moments.json`, `state_distance_matrix.json` reçoivent un
    `_meta.iso3_to_name_fr`) ;
  - les scripts client `assets/js/basis_viz.js`, `assets/js/moments.js`,
    `assets/js/distances.js` qui étiquettent désormais les axes, hovers,
    titres et sélecteurs avec « Nom français (ISO3) » ;
  - le geojson global qui porte `properties.name_fr` sur chaque feature et
    la carte (`assets/js/map.js`) qui l'utilise dans le popup au clic et
    dans un tooltip suspendu au survol.
- `docker-compose.yml` : le mount `data_sources` n'est plus `:ro` afin que
  la commande `civvec basis fetch-geometries` puisse réécrire le geojson
  depuis le conteneur.

### Fixed — Carte choroplèthe : couverture, affiliations et sous-ensembles (2026-06-02)

- **Couverture géojson complète** : `apps/basis_builder/geometries.py` ne filtre
  plus Natural Earth 110m sur les pays disposant de données Hofstede/IW. Toute
  la collection (≈ 177 États souverains) est conservée, Antarctique exclu
  (`EXCLUDED_ISO3_CODES`). La carte affiche désormais Pologne, Suisse, Pakistan,
  Égypte, Asie centrale, Afrique entière, etc., avec bordures sur tous les pays.
  `fetch_and_filter_natural_earth_admin0` renommée en
  `fetch_and_tag_natural_earth_admin0` (CLI `civvec basis fetch-geometries`
  inchangée côté UX).
- **Affiliations civilisationnelles curatées** : nouveau module
  `apps/basis_builder/taxonomy_membership.py` qui index les `member_states[]`
  et `sub_clusters[]` de `taxonomies/macro_civilizations.v2.json`.
  `apps/basis_builder/projector.py` propage cinq champs jusqu'à
  `state_coordinates.json` : `curated_civilization`, `curated_role`,
  `curated_civilizations_competing`, `sub_cluster_id`, `sub_cluster_label`.
  Corrige les mauvaises affiliations argmax (Allemagne → western au lieu de
  japanese, Espagne → western au lieu de buddhist, Arabie saoudite et Malaisie
  → islamic). L'argmax du vecteur d'affinité reste utilisé en repli pour les
  pays absents de la taxonomie. Schéma `schemas/state_coordinates.schema.json`
  étendu en conséquence.
- **Sous-ensembles civilisationnels** propagés dans `state_coordinates.json`
  et rendus dans la carte par variation HSL stable de la couleur parente
  (Anglo, Europe protestante, Europe catholique, Arab islamic, etc.).
- **Toggle Macro/Sous-ensemble + popup enrichi** : `site_src/docs/assets/js/map.js`
  refondu — `decorateFeaturesWithMembership`, mode `macro`/`sub` piloté par
  radios dans `site_src/templates/map_page.md.j2`, bordures épaissies sur survol
  via `feature-state`, popup au clic indiquant la civilisation curatée, le
  sous-ensemble, l'argmax d'affinité et l'origine de la couleur (curatée vs
  affinité). Légende reconstruite selon le mode actif et avec entrée grise
  « Pas de données / hors taxonomie ».
- **Tests** : nouvelles assertions dans `tests/test_site_build.py`
  (`test_geojson_includes_full_natural_earth_coverage`,
  `test_state_coordinates_curated_membership`,
  `test_state_coordinates_sub_clusters`, `test_map_page_has_mode_toggle`).

### Added — Mini-site de vulgarisation grand public (2026-06-02)

- Nouveau **mini-site autonome** hébergé sous `/vulgarisation/` (hors thème
  MkDocs Material, identité visuelle propre — terre cuite, serif, ethics
  sticky en haut, plan responsive 2-colonnes). Trois portes d'entrée
  stratifiées : citoyen / journaliste / étudiant SHS, plus un hub d'accueil
  et trois pages transverses (glossaire illustré, FAQ, crédits).
- **Sources** : `site_src/vulgarisation_src/` (Markdown + Jinja2 layout).
- **Builder** : `apps/site_builder/vulgarisation.py::render_vulgarisation()`,
  branché dans `apps/site_builder/builder.py::render_all()`. Conversion
  Markdown→HTML via la lib `markdown` (transitivement installée par
  mkdocs-material), enveloppage Jinja2 dans `_layout.html.j2`. Le sous-arbre
  HTML est copié tel quel par `mkdocs build` (les `.html` non-Markdown ne
  sont pas enveloppés par Material).
- **mkdocs.yml** : `not_in_nav` étendu de `/vulgarisation/**` et entrée nav
  externe `Vulgarisation ↗ → /cvs/vulgarisation/`.
- **Pages livrées** (19 au total) :
  - Hub : `index.html` (3 portes + 1 porte « je veux les vraies maths »).
  - Niveau 1 — citoyen (5 pages) : `qu-est-ce-qu-une-civilisation`,
    `comment-on-classe-un-pays`, `si-la-france-etait`, `pourquoi-c-est-imparfait`.
  - Niveau 2 — journaliste/décideur (5 pages) : `comment-lire-la-carte`,
    `les-3-distances-en-1-image`, `ce-que-ces-chiffres-ne-disent-pas`,
    `boite-a-outils-redactionnelle`.
  - Niveau 3 — étudiant SHS (6 pages) : `huntington-en-2-pages`,
    `hofstede-en-2-pages`, `inglehart-welzel-en-2-pages`,
    `ce-que-le-bayesien-apporte`, `controverses-academiques`.
  - Transverses : `glossaire-illustre`, `faq`, `credits`.
- **Avertissement éthique sticky** sur chaque page HTML (token identique au
  site principal, vérifié par `test_vulgarisation_ethics_sticky_on_every_html`).
- **Cross-linking** : site principal → vulgarisation (encart `tip` sur
  `index.md` et lien « Voir aussi » sur `ethics.md`) ; vulgarisation →
  méthodologie/états/carte/distances/éthique (footer commun) + liens
  inline (« pour aller plus loin ») sur chaque page de niveau 3.
- **Tests** : `tests/test_vulgarisation.py` (11 cas) — présence du hub, des
  3 niveaux, sticky éthique partout, absence de classes Material (md-*),
  liens retour vers méthodologie, footer, assets présents, absence de
  GADM, exclusion `not_in_nav`, entrée nav externe, lien depuis l'accueil.

### Published — v3.0.0a1 en ligne (2026-06-01)

- Republication automatique via `.github/workflows/publish.yml` (workflow success).
- Nouvelles URLs live (HTTP 200 vérifié) sur <https://s-geffroy.github.io/cvs/> :
  - `/methodology/09_civilizational_second_moment/` (M(s) renommé)
  - `/methodology/11_critiques_and_responses/` (27 critiques anticipées + sources)
  - `/methodology/12_empirical_validation/`
  - `/methodology/13_sensitivity_analysis/`
  - `/methodology/14_baseline_unsupervised/`
  - `/methodology/15_glossary/`
  - `/moments/` (anciennement `/tensions/`)
  - `/assets/data/state_moments.json` (champ JSON `M` + décomposition `Cov_w + biais`)
  - `/assets/data/empirical/{sensitivity_leave_one_out, sensitivity_beta_sweep, sensitivity_hybrid_weights, baseline_clustering, external_validation}.json`
- Bannière éthique présente sur toutes les nouvelles pages méthodologiques.
- Pages renommées et termes-clés vérifiés en ligne (« Second moment civilisationnel », « physics envy », « McSweeney »).

### Changed — v3.0.0a1 : rigueur méthodologique étoffée (2026-06-01)

**Breaking change** : le **tenseur de tension `T(s)`** est renommé en
**second moment civilisationnel `M(s)`**. Contenu mathématique identique,
nom corrigé pour évacuer le *physics envy* et clarifier la nature de l'objet.

#### Code (synchrone, breaking)

- `apps/basis_builder/tensors.py` → `apps/basis_builder/moments.py` ; `compute_tension_tensor` → `compute_second_moment` ; `StateTension` → `StateSecondMoment`.
- `schemas/state_tension.schema.json` → `schemas/state_moment.schema.json` ; champ JSON `T` → `M` ; nouveaux champs `decomposition.{weighted_barycentre_mu_bar, intra_civilizational_covariance, bias_term, trace_intra, trace_bias}`.
- `packages/civvec_core/algebra/distances.py` : `d_T_frobenius` → `d_M_frobenius` ; **nouvelle métrique** `d_score_mahalanobis_intra` (covariance intra-civilisationnelle pondérée, plus robuste que la version centroïdes) ; ancienne version renommée `d_score_mahalanobis_centroids` ; **nouvelle fonction** `normalise_distances_by_panel_median` pour normaliser les composantes de `d_hyb` avant combinaison convexe.
- `apps/site_builder/builder.py` : ré-écriture du calcul de la matrice de distances ; publie désormais 9 métriques (avec les deux Mahalanobis et la normalisation par médiane).
- `tests/test_tensor_mechanics.py` → `tests/test_moment_mechanics.py` ; nouveau test `test_decomposition_consistency` (M = Cov_w + biais vérifié numériquement).
- Streamlit page `8_State_Tensions.py` → `8_State_Moments.py` ; JS `tensors.js` → `moments.js` ; CSS/HTML ids `civvec-tensions-*` → `civvec-moments-*`.
- Site nav : `/tensions/` → `/moments/`.
- `pyproject.toml` : version `2.0.0a1` → `3.0.0a1`.

#### Invariant `I2` von Mises — formule corrigée

L'ancien `I2 = tr(M²) − tr(M)²/n` n'était pas la définition canonique. Remplacé par `I2_von_mises = √(3/2 · s:s)` avec `s = M − tr(M)/6 · I` (déviateur), conforme à l'usage en mécanique des solides.

#### Documentation méthodologique

- **Nouvelle [doc 09](docs/09_civilizational_second_moment.md)** — *Second moment civilisationnel `M(s)`* (renommée et restructurée) avec dérivation rigoureuse `M = Cov_w + biais`, démonstration formelle, et discussion explicite de la valeur informationnelle au-delà de `xₛ`.
- **Nouvelle [doc 10](docs/10_distance_algebra.md)** — *Algèbre des distances* étoffée : Mahalanobis intra vs centroïdes, normalisation par médiane panel pour `d_hyb`, circularité de Wasserstein explicitement reconnue.
- **Nouvelle [doc 11](docs/11_critiques_and_responses.md)** — *Critiques académiques et réponses du projet* : 27 critiques anticipées (Huntington, Hofstede, IW, WVS, mélange hybride, physics envy, redondance M↔x, Mahalanobis, d_hyb, essentialisme étatique, etc.) avec sources académiques et statut de la réponse (fix, atténuée, admise, travail futur).
- **Nouvelle [doc 12](docs/12_empirical_validation.md)** — *Validation empirique externe* : corrélations Spearman + bootstrap CI95 de `wₛ` contre Pew Religious Composition (2020), World Bank WGI Rule of Law (2022), Fund For Peace FSI (2024).
- **Nouvelle [doc 13](docs/13_sensitivity_analysis.md)** — *Analyse de sensibilité* : LOO sur archétypes, sweep `β` softmax (0.01 à 0.2), sweep `(α, β, γ)` hybride sur grille simplexe.
- **Nouvelle [doc 14](docs/14_baseline_unsupervised.md)** — *Baseline non-supervisé* : k-means k=11 + HDBSCAN-lite sur WVS+Hofstede brut comparé à la taxonomie Huntington-informée (ARI, NMI).
- **Nouvelle [doc 15](docs/15_glossary.md)** — *Glossaire* complet : tous les symboles, distances, drapeaux qualité, sources, acronymes.
- **Doc 07 étoffée** (8 lignes → ~110 lignes) : audience cible, restrictions d'usage géopolitique, sources/licences/consent WVS, gouvernance des modifications, mécanisme de retrait, conflits d'intérêt, règles d'inférence interdites explicites.
- **Doc 08 corrigée** : orthogonalité Hofstede étiquetée *postulée non vérifiée empiriquement* (était trompeur en v2.0) ; nouvelle §3.4 « Règle de désambiguïsation » entre civilisations chevauchantes (KOR, THA, BOL, NZL, etc.) ; procédure d'imputation explicitée.
- **Docs 00–06 harmonisées** en prose long-form (~30-60 lignes chacune) au lieu du quasi-JSON cryptique de la v2.0.

#### Code empirique (nouveau)

- `apps/empirical/sensitivity.py` : LOO + β-sweep + `(α, β, γ)`-sweep.
- `apps/empirical/baseline_clustering.py` : k-means pure NumPy + HDBSCAN-lite (single-linkage + gap) + ARI + NMI.
- `apps/empirical/external_validation.py` : Spearman + bootstrap 1000.
- `apps/cli/empirical.py` : sous-commandes `civvec empirical {sensitivity, baseline, validate, all}`.
- Données curées committées : `data_sources/pew/religious_composition_2020.json`, `data_sources/wgi/rule_of_law_2022.json`, `data_sources/fsi/fragility_states_index_2024.json` (63 ISO3 chacune, citation complète).
- Artefacts générés : `outputs/empirical/{sensitivity_leave_one_out, sensitivity_beta_sweep, sensitivity_hybrid_weights, baseline_clustering, external_validation}.json` + copie dans `assets/data/empirical/`.

#### Tests étendus

- 22 tests Phase 2 sur le site, 16 tests `test_moment_mechanics.py` (avec `test_decomposition_consistency` nouveau), 15 tests `test_distance_algebra.py` (avec les deux Mahalanobis et `normalise_distances_by_panel_median`).
- Vérification end-to-end : `docker compose build` ✓, suite **56 tests** ✓ en image site, suite **38 tests** ✓ en image UI.

### Published — Phase 2 en ligne (2026-06-01)

- Republication automatique via `.github/workflows/publish.yml` (workflow run 26748986987, conclusion=success).
- URLs live (HTTP 200 vérifié) sur <https://s-geffroy.github.io/cvs/> :
  - `/states/` + 63 fiches État (`/states/<ISO3>/`)
  - `/map/` (MapLibre choropleth)
  - `/basis/` (Plotly scatter B_viz + radar B_score)
  - `/tensions/` (anisotropie + heatmap T(s))
  - `/distances/` (matrice d_hyb + détail toutes-distances)
  - `/assets/data/global_state_baseline.geojson` (provenance Natural Earth confirmée, `contains_gadm_geometry: false`)
- Bannière éthique présente sur chaque page Phase 2 (vérifié via grep sur HTML servi).

### Added — Phase 2 livrée (2026-06-01)

- **Géométries Natural Earth ADM0 110m** versionnées dans `data_sources/natural_earth/admin0_countries_110m.geojson` — pinned commit `nvkelso/natural-earth-vector @ ca96624a56`, domaine public ; 62/63 ISO3 couverts (HKG et SGP absents à cette résolution, mention explicite). Aucune géométrie GADM publiée.
- **Module `apps/basis_builder/geometries.py`** : `fetch_and_filter_natural_earth_admin0()` reproductible, tagging `geometry_source = "Natural Earth"` + `contains_gadm_geometry: false` sur chaque feature. CLI `civvec basis fetch-geometries`.
- **Templates Jinja2 Phase 2** (`site_src/templates/`) : `state_page.md.j2`, `states_index.md.j2`, `map_page.md.j2`, `basis_page.md.j2`, `tensions_page.md.j2`, `distances_page.md.j2` — bannière éthique sur chaque page.
- **Builder Phase 2** (`apps/site_builder/builder.py`) : `render_states`, `render_map_page`, `render_basis_page`, `render_tensions_page`, `render_distances_page` + calcul global de la matrice de distances (8 métriques : `d_viz`, `d_score^E`, `d_score^M`, `d_w^cos`, `d_w^JS`, `d_w^W`, `d_T`, `d_hyb`).
- **Pages publiées** : 63 fiches États (`/states/<ISO3>/`) + `/states/`, `/map/`, `/basis/`, `/tensions/`, `/distances/`.
- **Assets data** (`dist/assets/data/`) : `state_coordinates.json`, `civilization_centroids.json`, `state_tensors.json`, `state_distance_matrix.json`, `B_viz.json`, `B_score.json`, `global_state_baseline.geojson` + dossier `states/<ISO3>.profile.json` et `states/<ISO3>.geojson`.
- **Assets JS** (`site_src/docs/assets/js/`) : `map.js` (MapLibre GL JS 4.7.1, choropleth par civilisation dominante, sans fond externe), `basis_viz.js` (Plotly 2.35.2 scatter B_viz + radar B_score), `tensors.js` (anisotropie + heatmap 6×6 avec sélecteur ISO3), `distances.js` (heatmap matrice + détail toutes-distances par paire).
- **`mkdocs.yml`** : nav étendue (États / Carte / Base vectorielle / Tensions / Distances), CDN MapLibre + Plotly pinné, `not_in_nav` pour les 63 fiches États.
- **Tests Phase 2** (`tests/test_site_build.py`) : présence et provenance Natural Earth, FRA carry `x_viz` + Hofstede + tenseur, matrice de distance symétrique avec diagonale 0, JS hooks `civvec-*` présents, assets data téléchargeables (10 nouveaux tests).
- Vérification end-to-end : `docker compose build civvec_site` ✓, suite 51 tests ✓ en image site, suite 33 tests ✓ en image UI, nginx preview `HTTP 200` sur `/states/FRA/`, `/map/`, `/basis/`, `/tensions/`, `/distances/`.

### Published — Phase 1b en ligne (2026-05-30)

- Dépôt initialisé sur `git@github.com:s-geffroy/cvs.git` (public).
- GitHub Pages activé avec source = GitHub Actions.
- Premier déploiement automatique réussi via `.github/workflows/publish.yml`.
- URL Pages : <https://s-geffroy.github.io/cvs/> — accueil, fiches civilisations, méthodologie, ADM1, sources, schémas servis avec bannière éthique sur chaque page.

### Added — Phase 1b livrée (2026-05-30)

- `mkdocs.yml` Material avec navigation Phase 1b (Accueil, Méthodologie, Taxonomie, Civilisations ×11, Sources, Schémas, ADM1, Relecture).
- Bannière éthique persistante via override `site_src/overrides/main.html` (block `announce` de Material).
- `site_src/docs/index.md`, `ethics.md`, `adm1_policy.md`, `review/index.md`.
- `apps/site_builder/builder.py` + `loaders.py` + `guards.py` (whitelist géométries `{Natural Earth, geoBoundaries}`, scan GADM).
- Templates Jinja2 : `civilization_page.md.j2` (hyper-détaillé), `taxonomy_index.md.j2`, `sources_index.md.j2`, `schemas_index.md.j2`, `methodology_index.md.j2`.
- CLI `civvec site build` + `civvec site preview` + branchement dans `civvec` root.
- `Dockerfile.site` multi-stage (builder + nginx preview) + services `civvec_site` et `civvec_site_preview` dans `docker-compose.yml`.
- Tests `tests/test_site_build.py` (11 tests : éthique sur chaque page, 11 civilisations rendues, méthodo 00..10 présente, bibliographie/sources/schemas/ADM1 publiés, pas de géométrie GADM).
- Workflow GitHub Actions `.github/workflows/publish.yml` : build via container, exécution pytest, déploiement Pages.
- Vérification end-to-end : `docker compose run --rm civvec_site` ✓, suite 41 tests ✓ en image site, nginx preview `HTTP 200` sur Accueil, fiche Western, mécanique tensorielle.

### Added — Phase 1 livrée (2026-05-30)

- Vérification end-to-end : `docker compose build civvec_ui` ✓, `docker compose up civvec_ui` ✓ (HTTP 200 sur `/_stcore/health`), `pytest` 33/33 ✓.

### Added — Phase 1 bootstrap (2026-05-30)

- Initial `cvs/` project layout next to read-only reference `raw/`.
- Top-level `README.md`, `CHANGELOG.md`, `.gitignore`, `pyproject.toml` with extras `[basis,ui,site,dev]`.
- Directory skeleton: `apps/`, `packages/civvec_core/`, `schemas/`, `taxonomies/`, `data_sources/`, `docs/`, `site_src/`, `tests/`.
- JSON Schemas v2: `basis.schema.json`, `civilization_centroid.schema.json`, `state_coordinates.schema.json`, `state_tension.schema.json`, `distance_matrix.schema.json`, `macro_civilizations.schema.json`, `state_profile.v2.schema.json`, `adm1_profile.v2.schema.json`.
- B_doc canonical data: `data_sources/inglehart_welzel/cultural_map_wave7.json`, `data_sources/hofstede/dimensions_v2015.json`, `data_sources/SOURCES.md`.
- B_doc methodology: docs `00..07` rebased from `raw/docs/`, plus new `08_civilizational_basis.md`, `09_civilizational_mechanics.md`, `10_distance_algebra.md`.
- Hyper-detailed taxonomy `taxonomies/macro_civilizations.v2.json` covering 11 macro-civilisations with `huntington_label`, `iw_clusters`, `hofstede_archetype_states`, `member_states[]`, `sub_clusters[]`, `ambiguous_cases[]`, `citation_ids[]`, `bibliography[]`.
- B_vec formal definitions: `packages/civvec_core/basis/B_viz.json` (ℝ², Inglehart-Welzel), `B_score.json` (ℝ⁶, Hofstede).
- B_vec builder: `apps/basis_builder/{load_iw,load_hofstede,centroids,projector,tensors}.py`.
- Civilizational tensor mechanics: `state_tensors.json`, invariants, eigenvalues, anisotropy index, `09_civilizational_mechanics.md`.
- Distance algebra: `packages/civvec_core/algebra/{distances,transport}.py` with `d_viz`, `d_score^E`, `d_score^M`, `d_w^cos`, `d_w^JS`, `d_w^W` (Sinkhorn), `d_T`, `d_hyb`. Doc `10_distance_algebra.md`.
- Typer CLI `civvec` with subcommands `basis build`, `basis validate`, `ui`.
- Streamlit UI Phase 1: `Home.py` + 9 pages (Documentary Basis, Vector Basis, State Explorer, Compare States, Diagnostics, Sources, Methodology, State Tensions, Distance Algebra), shared `ethics_banner` and `charts` components.
- Docker: `Dockerfile.ui` + `docker-compose.yml` service `civvec_ui` (port 8501).
- Tests: `test_documentary_basis.py`, `test_vector_basis.py`, `test_bases_coupling.py`, `test_tensor_mechanics.py`, `test_distance_algebra.py`, `test_ui_smoke.py`, `test_adm1_anticipation.py`.
- ADM1 anticipation: `schemas/adm1_profile.v2.schema.json`, `docs/04_adm1_preparation_policy.md`, CLI hook returning `prepared_not_active`.

# 16 — Cascade d'imputation pour atteindre 193/193 États

> **Avertissement éthique** : ce chapitre formalise comment les coordonnées d'un État sont obtenues quand les sondages culturels directs (WVS, Hofstede) ne le couvrent pas. **Aucune donnée n'est inventée** : toute valeur publiée reste traçable à une source publique (sondage, indicateur agrégé) ou à un *prior* explicite (centroïde de civilisation). Voir [`07_ethics_publication_policy.md`](07_ethics_publication_policy.md).

## 1. Motivation

L'objectif central du projet est d'attribuer à chaque État souverain un vecteur dans la base civilisationnelle `(x_viz ∈ ℝ², x_score ∈ ℝ⁶)`. Avant V2, seuls ~70 États apparaissaient dans `state_coordinates.json` ; les 123 autres États membres de l'ONU étaient silencieusement absents — car le projecteur filtrait sur l'union des États présents dans WVS, Hofstede ou la taxonomie curatée.

Le rapport de couverture (`data_sources/un_members/coverage_report.md`) chiffre les déficits :

- 132 États sans Hofstede
- 133 États sans Inglehart-Welzel
- 0 État sans géométrie (résolu en V1)

La cascade d'imputation décrite ici garantit que **tous les 193 États membres de l'ONU possèdent un `x_viz` et un `x_score` non nuls**, chacun marqué d'une *provenance* qui permet aux consommateurs aval (algèbre des distances, tenseur du second moment, carte UI) de stratifier l'analyse selon la qualité de l'observation.

## 2. Définition de la cascade

Pour chaque ISO3 ONU `s`, le projecteur (`apps/basis_builder/projector.py`) cherche une coordonnée selon les tiers de qualité décroissante :

| Rang | Tier | x_viz | x_score | Quand est-il utilisé ? |
|---|---|---|---|---|
| 1 | `observed` | IW wave-7 officiel | Hofstede direct | L'État est mesuré par les sondages canoniques |
| 1b | `observed_with_dim_imputation` | — | Hofstede partiel (NaN remplis par moyenne ligne) | Certaines dimensions Hofstede sont manquantes |
| 2 | `imputed_wvs_items` | Régression ridge sur 10 items WVS waves 5-6 calibrée sur wave-7 (RMSE LOO 0.38/0.54) | — | L'État apparaît dans WVS 5/6 mais pas dans le cultural map wave-7 |
| 3a | `imputed_pew` | Régression Pew + UNDP HDR + UN voting + V-Dem → (ts, se) | — | Aucune donnée WVS, mais au moins une source auxiliaire |
| 3b | `imputed_governance` | — | Régression WGI + FSI + UNDP HDR + UN voting + V-Dem → 6 dim Hofstede | Hofstede manquant, ≥1 auxiliaire |
| 4 | `centroid_prior` | μ_viz(civ curatée) | μ_score(civ curatée) | Aucune observation et aucune source auxiliaire disponible |

Une dimension `x_score` Hofstede partiellement renseignée (manque LTO ou IVR, par exemple) reste classée `observed_with_dim_imputation` — le remplissage par moyenne ligne existait déjà en V1.

L'ordre des tiers est appliqué **indépendamment** sur `x_viz` et sur `x_score`. Un État peut donc avoir un `x_viz = observed` (présent dans IW) et un `x_score = centroid_prior` (absent de Hofstede). Le champ `data_quality` du `StateCoordinates` enregistre les deux provenances.

## 3. Calibration des tiers d'imputation

### 3.1 Pew → Inglehart-Welzel (ts, se)

Module : `packages/civvec_core/imputation/pew_to_iw.py`.

- **Entrée** : profil Pew par État `(dominant_group ∈ {Christian, Muslim, Hindu, Buddhist, Jewish, Folk, Unaffiliated, Other}, dominant_share_pct ∈ [0, 100])`.
- **Vecteur de caractéristiques** : one-hot 8D du groupe dominant + part normalisée — soit 9 features.
- **Cibles** : deux régressions ridge indépendantes pour `ts` et `se`.
- **Jeu d'entraînement** : intersection Pew ∩ IW observée (= |Pew ∩ IW| États).
- **Régularisation** : α = 1.0, intercept implicite.
- **Validation** : leave-one-out, RMSE rapporté sur chaque axe.

Le jeu de données Pew local actuellement présent dans `data_sources/pew/` couvre 63 États qui se confondent presque entièrement avec ceux d'Hofstede ∩ IW. La couverture marginale réelle apportée par ce tier est donc faible tant que des sources Pew/DESA enrichies (cf. §6) ne sont pas ajoutées.

### 3.2 Gouvernance (WGI + FSI) → Hofstede 6D

Module : `packages/civvec_core/imputation/governance_to_hofstede.py`.

- **Entrée** : score WGI Rule of Law (z-score) + score FSI total (normalisé /120).
- **Vecteur de caractéristiques** : 2 scalaires + intercept.
- **Cibles** : six régressions ridge indépendantes pour `(pdi, idv, mas, uai, lto, ivr)`.
- **Jeu d'entraînement** : intersection WGI ∩ FSI ∩ Hofstede observée.
- **Régularisation** : α = 1.0, intercept non régularisé.
- **Validation** : leave-one-out, RMSE par dimension.

Avec seulement deux entrées scalaires, la capacité de récupération des 6 dimensions Hofstede est limitée. C'est par conception un *garde-fou* : nous documentons les RMSE pour chaque dimension afin que les consommateurs puissent décider si l'imputation est suffisante ou s'il vaut mieux retomber sur le centroïde.

### 3.3 Centroïde civilisationnel (`centroid_prior`)

Module : `packages/civvec_core/imputation/centroid_prior.py`.

- **Entrée** : `curated_civilization` (ou première civilisation listée dans `curated_civilizations_competing` si l'État est ambigu, cf. §5).
- **Sortie** :
  - `x_viz(s) = mu_viz(civ)`
  - `x_score(s) = mu_score(civ)`
  - `x_viz_ellipse(s) = sigma_viz(civ)` (covariance 2×2 du centroïde)
  - `sigma_score(s) = sigma_score(civ)` (vecteur d'écarts-types 6D)

C'est le **prior bayésien** sur la position d'un État dans sa civilisation. Sans observation, le *posterior* dégénère vers ce prior — comportement attendu, pas un bug. Le projecteur expose `sigma_score` dans `data_quality.x_score_sigma_prior` afin que le tenseur du second moment (cf. §4) puisse propager l'incertitude.

## 4. Propagation de l'incertitude dans `M(s)`

Le second moment civilisationnel est défini par :

$$M(s) = \sum_i w_s[i] \cdot (\mu_i - x_s)(\mu_i - x_s)^\top \in \mathbb{R}^{6 \times 6}$$

Pour un État dont `x_score_provenance != observed`, l'imputation introduit une incertitude qui doit être visible dans `M(s)`. Le projecteur passe `x_score_sigma_prior` au calculateur de moments (`apps/basis_builder/moments.py`), qui **gonfle la diagonale** :

$$M_{\text{inflated}}(s) = M(s) + \mathrm{diag}(\sigma_{\text{prior}}^2)$$

La décomposition canonique est étendue d'un troisième terme :

$$M = \mathrm{Cov}_w(\mu;w) + (\bar{\mu} - x_s)(\bar{\mu} - x_s)^\top \cdot \sum w + \mathrm{diag}(\sigma_{\text{prior}}^2)$$

Le champ `decomposition.prior_variance_inflation` expose explicitement le terme ajouté. Sans cela, les invariants de `M(s)` seraient lus comme des observations dures, gommant la différence entre un État réellement mesuré et un État ramené au prior.

## 5. Cas ambigus (multi-civilisation contestée)

Six États membres de l'ONU ont `curated_civilization = None` mais figurent dans `curated_civilizations_competing` de plusieurs civilisations : `BIH` (Bosnie-Herzégovine), `CIV` (Côte d'Ivoire), `ISR` (Israël), `KOR` (Corée du Sud), `LBN` (Liban), `TCD` (Tchad). Le projecteur utilise alors la **première civilisation listée** dans `curated_civilizations_competing` comme civilisation par défaut pour le centroïde de repli. Un raffinement futur pourrait calculer une moyenne pondérée des centroïdes contestés au lieu de choisir le premier.

## 6. Sources externes ingérées (V2.1, 2026-06-07)

La cascade est alimentée par les sources publiques suivantes, intégrées dans cet ordre :

| Source | Couverture ONU | Tier(s) alimenté(s) | État |
|---|---|---|---|
| WVS wave 7 (cultural_map_wave7.json) | 60 | `observed` (x_viz) | ✅ historique |
| WVS Time-Series 1981-2022 v5.0 | +30 | `imputed_wvs_items` (x_viz) | ✅ 2026-06-07 |
| Hofstede 2010 | 63 | `observed` (x_score) | ✅ historique |
| Pew composition religieuse complète (7 props) | 182 | feature pour `imputed_pew` | ✅ 2026-06-07 |
| World Bank WGI Rule of Law 2022 | 63 | feature pour `imputed_governance` | ✅ historique |
| Fund For Peace FSI 2024 | 63 | feature pour `imputed_governance` | ✅ historique |
| UNDP HDR 2025 (HDI + GII + scolarité + GNI) | 191 | features pour `imputed_pew` ET `imputed_governance` | ✅ 2026-06-07 |
| Voeten/Strezhnev/Bailey UN GA voting 1946-2025 | 192 | features pour les deux régressions | ✅ 2026-06-07 |
| V-Dem v16 (12 indices retenus) | 172 | features pour les deux régressions | ✅ 2026-06-07 |

**Sources à friction (non-ingérables automatiquement)** :

- **WVS waves 5, 6 directs avec coordonnées officielles** : nous prédisons via ridge sur les items au lieu d'utiliser des coordonnées officielles publiées (qui n'existent pas pour ces waves). RMSE LOO 0.38/0.54 par axe — meilleur que les imputations Pew+UNDP.
- **UNESCO World Heritage** : non prioritaire (validation croisée uniquement, pas d'apport à la cascade quantitative).

Cf. [Catalogue des sources](../sources/index.md) §7 pour les URL, citations et procédures d'ingestion détaillées.

## 7. Critique anticipée : circularité

> « Vous imputez la position d'un État via la taxonomie que vous prétendez ensuite valider empiriquement. »

Réponse :

- La validation empirique (cf. [doc 12](12_empirical_validation.md)) est **stratifiée par provenance** : les tests de cohérence avec WGI, Pew, FSI sont rapportés *uniquement sur les États `observed`*, jamais sur les États `centroid_prior` (où la corrélation serait artificielle par construction).
- Les distances civilisationnelles entre deux États `centroid_prior` de la même civilisation tombent à zéro (modulo l'inflation de variance) — c'est *honnête*, ces deux États sont indiscernables sous le prior. La carte UI matérialise ce statut (marqueur ou opacité distincts).
- La taxonomie elle-même est ajustée à partir de la littérature (Huntington 1996 + Pew religion) et des centroïdes empiriques calculés sur les `core/periphery` observés, *pas* sur les `centroid_prior`. La boucle de rétroaction est interrompue.

## 8. Vérification

Le rapport de couverture (`civvec basis coverage-report`) produit désormais une section « Provenance des coordonnées » donnant le décompte par tier. La condition `len(states) == 193 ∧ aucun null` est testée dans `tests/test_imputation_cascade.py`. La régression `test_observed_states_retain_observed_provenance` garantit qu'aucun État réellement mesuré n'est dégradé en imputé après chaque évolution du pipeline.

## 9. Références

- Inglehart, R. & Welzel, C. (2010). *Changing Mass Priorities*. Voir [doc 02](02_source_only_methodology.md) §2.
- Hofstede, G. *et al.* (2010). *Cultures and Organizations*. Voir [doc 05](05_scoring_calibration.md).
- Huntington, S. P. (1996). *The Clash of Civilizations*. Voir [doc 08](08_civilizational_basis.md).
- Pew Research Center (2020). *Religious Composition by Country*.
- Kaufmann, D. & Kraay, A. (2023). *Worldwide Governance Indicators*.
- Fund For Peace (2024). *Fragile States Index Annual Report*.

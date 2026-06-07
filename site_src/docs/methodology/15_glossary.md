# 15 — Glossaire

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md](07_ethics_publication_policy.md).

## Bases et espaces

| Terme | Définition |
|---|---|
| **`B_doc`** | Base **documentaire** : bibliographie (Huntington, IW, Hofstede, WVS, extensions) + taxonomie sourcée. Ce sur quoi le modèle s'appuie. |
| **`B_vec`** | Base **vectorielle** : `B_viz ⊕ B_score`. Espace mathématique de représentation. |
| **`B_viz`** | Sous-espace ℝ² des coordonnées Inglehart-Welzel : axe `TS` (Traditional ↔ Secular-Rational) × axe `SE` (Survival ↔ Self-Expression). |
| **`B_score`** | Sous-espace ℝ⁶ des dimensions Hofstede : `PDI`, `IDV`, `MAS`, `UAI`, `LTO`, `IVR`. |

## Dimensions Hofstede

| Code | Définition | Échelle |
|---|---|---|
| `PDI` | Power Distance Index — acceptation des inégalités hiérarchiques | 0-100 |
| `IDV` | Individualism vs Collectivism — primauté de l'individu vs groupe | 0-100 |
| `MAS` | Masculinity vs Femininity — compétition vs coopération culturelle | 0-100 |
| `UAI` | Uncertainty Avoidance Index — tolérance à l'ambiguïté | 0-100 |
| `LTO` | Long-Term Orientation — perspective temporelle | 0-100 |
| `IVR` | Indulgence vs Restraint — gratification vs retenue | 0-100 |

## Objets calculés par État

| Symbole | Définition | Espace |
|---|---|---|
| `xₛ^viz` | Coordonnée Inglehart-Welzel de l'État `s` | `B_viz = ℝ²` |
| `xₛ^score` | Vecteur Hofstede 6D de l'État `s` | `B_score = ℝ⁶` |
| `wₛ` | Vecteur d'affinité civilisationnelle (simplexe) | `Δ¹⁰` (11 civilisations, somme=1) |
| `Σₛ^viz` | Matrice de covariance 2×2 de l'incertitude IW | ℝ^{2×2} PSD |
| `M(s)` | Second moment civilisationnel pondéré | ℝ^{6×6} PSD |
| `eₖ(s)`, `λₖ(s)` | Vecteurs/valeurs propres de `M(s)` | ℝ⁶, ℝ |
| `A(s)` | Anisotropie `(λ₁−λ₆)/λ₁` | `[0, 1]` |
| `μ̄(s)` | Barycentre pondéré `Σᵢ wₛ[i] · μᵢ` | ℝ⁶ |

## Objets calculés par civilisation

| Symbole | Définition |
|---|---|
| `μᵢ^viz` | Centroïde IW de la civilisation `i` (moyenne pondérée des États archétypes) |
| `Σᵢ^viz` | Covariance IW intra-civilisationnelle |
| `μᵢ^score` | Centroïde Hofstede de la civilisation `i` |
| `σᵢ^score` | Dispersion par-axe Hofstede (écart-types pondérés) |

## Rôles des États archétypes

| Rôle | Poids `αⱼ` | Description |
|---|---|---|
| `core` | 1.0 | État archétype certain de la civilisation |
| `periphery` | 0.5 | Membre périphérique — fait partie mais avec moindre poids |
| `interface` | 0.0 | État à l'interface (membres listés mais non comptés dans le centroïde) |
| `ambiguous` | 0.0 | Cas controversé (membres listés mais non comptés) |

## Distances

| Symbole | Définition | Espace |
|---|---|---|
| `d_viz(s, t)` | Distance Euclidienne dans `B_viz` | ℝ² |
| `d_score^E(s, t)` | Distance Euclidienne dans `B_score` | ℝ⁶ |
| `d_score^M_centroids(s, t)` | Mahalanobis avec **inter-civ** covariance (centroïdes) | ℝ⁶ |
| `d_score^M_intra(s, t)` | Mahalanobis avec **intra-civ** covariance pondérée | ℝ⁶ |
| `d_w^cos(s, t)` | Dissimilarité cosinus sur `wₛ` (pas triangle — pas une distance) | `Δ¹⁰` |
| `d_w^JS(s, t)` | Distance Jensen-Shannon sur `wₛ` (vraie distance) | `Δ¹⁰` |
| `d_w^W(s, t)` | Wasserstein-2 sur `wₛ` (Sinkhorn) | `Δ¹⁰` |
| `d_M_F(s, t)` | Distance de Frobenius sur les seconds moments `M` | ℝ^{6×6} |
| `d_hyb(s, t)` | Combinaison convexe `α · d_score^M_intra + β · d_w^W + γ · d_M_F` (normalisée par médiane panel) | — |

## Paramètres du modèle

| Paramètre | Valeur par défaut | Description |
|---|---|---|
| `β_softmax` | 0.05 | Température du softmax inverse-distance utilisé pour dériver `wₛ` |
| `α` (hybride) | 0.4 | Poids de `d_score^M_intra` dans `d_hyb` |
| `β` (hybride) | 0.4 | Poids de `d_w^W` dans `d_hyb` |
| `γ` (hybride) | 0.2 | Poids de `d_M_F` dans `d_hyb` |
| `ε_Sinkhorn` | 0.05 | Régularisation entropique de Sinkhorn pour Wasserstein-2 |
| `ridge` | 1.0 | Régularisation de la covariance Mahalanobis |

## Sources et bibliographie

| Citation ID | Source courte |
|---|---|
| `huntington_1996` | Huntington, S. P. (1996). *The Clash of Civilizations*. |
| `inglehart_welzel_2005` | Inglehart & Welzel (2005). *Modernization, Cultural Change, and Democracy*. |
| `inglehart_welzel_2010` | Inglehart & Welzel (2010). « Changing Mass Priorities ». |
| `hofstede_2010` | Hofstede et al. (2010). *Cultures and Organizations* 3rd ed. |
| `wvs_wave7_2022` | Haerpfer et al. (2022). World Values Survey Wave 7. |
| `smith_2012` | Smith (2012). *Decolonizing Methodologies*. |
| `hauofa_1994` | Hau'ofa (1994). « Our Sea of Islands ». |
| `un_unpfii` | UN Permanent Forum on Indigenous Issues. |

## Indicateurs externes (validation doc 12)

| Code | Source |
|---|---|
| `pew_dominant_religion_share_2020` | Pew Research Center — share of largest religious group, 2020. |
| `wgi_rule_of_law_2022` | World Bank Worldwide Governance Indicators — Rule of Law, 2022. |
| `fsi_total_2024` | Fund For Peace — Fragile States Index Total, 2024. |

## Drapeaux qualité

| Flag | Sur quel objet | Sens |
|---|---|---|
| `low_archetype_coverage` | Civilisation | < 3 États archétypes avec données complètes |
| `low_evidence` | État | Au moins une source (IW ou Hofstede) manque |
| `iw_coverage: missing` | État | Pas de coordonnée IW disponible |
| `hofstede_coverage: missing` | État | Pas de vecteur Hofstede disponible |
| `hofstede_coverage: imputed` | État | Vecteur Hofstede partiellement imputé par moyenne |
| `monocivilizational` | Second moment `M(s)` | État proche d'un archétype unique, `M(s) ≈ 0` |
| `computed_from_imputed` | Second moment `M(s)` | Calculé sur vecteurs imputés |
| `contains_gadm_geometry` | GeoJSON publié | Doit être `false` (politique stricte) |
| `geometry_source` | GeoJSON publié | Doit être `"Natural Earth"` ou `"geoBoundaries"` |

## Acronymes externes

| Acronyme | Développement |
|---|---|
| `ADM0` | Unité administrative niveau 0 — État souverain |
| `ADM1` | Unité administrative niveau 1 — Régions sub-nationales |
| `ARI` | Adjusted Rand Index — métrique de clustering |
| `B_doc / B_vec` | Voir « Bases et espaces » |
| `CI` | Confidence Interval — intervalle de confiance |
| `FSI` | Fragile States Index |
| `GADM` | Global Administrative Areas — base géométrique académique, **interdite en publication cvs** |
| `IW` | Inglehart-Welzel |
| `JSD` | Jensen-Shannon Divergence |
| `LOO` | Leave-One-Out — protocole de validation par exclusion |
| `MapLibre` | Bibliothèque JavaScript de cartes interactives |
| `NMI` | Normalised Mutual Information |
| `PSD` | Positive Semi-Definite — matrice symétrique à valeurs propres ≥ 0 |
| `WGI` | Worldwide Governance Indicators (World Bank) |
| `WVS` | World Values Survey |
| `V-Dem` | Varieties of Democracy — V-Dem Institute, Université de Göteborg |
| `UNDP HDR` | United Nations Development Programme Human Development Report |
| `UN GA voting` | UN General Assembly votes ; idealpoint estimates par Voeten/Strezhnev/Bailey (Harvard Dataverse) |
| `Pew RC` | Pew Research Center Religious Composition by Country (7 catégories : Christians, Muslims, Hindus, Buddhists, Jews, Unaffiliated, Other) |
| `COW alpha` | Correlates of War 3-letter country code (différent de ISO3 pour ~60 États ; mapping dans `_wvs_extraction.py`) |

## Cascade d'imputation (V2)

| Terme | Définition |
|---|---|
| **Cascade** | Procédure de repli en trois tiers utilisée par le projecteur pour garantir un vecteur `(x_viz, x_score)` non nul pour chaque ISO3 ONU. Voir [doc 16](16_imputation_cascade.md). |
| **`provenance`** | Étiquette par coordonnée précisant son origine : `observed`, `observed_with_dim_imputation`, `imputed_pew`, `imputed_governance`, `centroid_prior`. Présente dans `data_quality.x_viz_provenance` et `data_quality.x_score_provenance`. |
| **`observed`** | Coordonnée tirée directement d'un sondage canonique (IW wave 7 pour `x_viz`, Hofstede 2010 pour `x_score`). |
| **`observed_with_dim_imputation`** | `x_score` partiellement observé : Hofstede présent mais certaines dimensions remplies par moyenne ligne. |
| **`imputed_wvs_items`** | `x_viz` prédit par régression ridge sur les 10 items de la factor analysis Inglehart-Welzel agrégés depuis WVS Time-Series (waves 5-6), calibrée sur les 57 États de l'intersection avec wave-7. RMSE LOO 0.38 (ts) / 0.54 (se). Méthodologiquement plus proche de `observed` que de `imputed_pew`. |
| **`imputed_pew`** | `x_viz` prédit par régression ridge sur (Pew 7 proportions + UNDP HDR + UN voting + V-Dem) → IW. RMSE LOO 0.48 (ts) / 0.62 (se). |
| **`imputed_governance`** | `x_score` prédit par régression ridge sur (WGI + FSI + UNDP HDR + UN voting + V-Dem) → 6 dimensions Hofstede. RMSE LOO par dimension publié. |
| **`centroid_prior`** | `x_viz = μ_viz(civ)` et/ou `x_score = μ_score(civ)` quand aucune observation n'est disponible ; la covariance du centroïde est reportée comme ellipse d'incertitude. |
| **`low_evidence`** | Drapeau booléen ; `True` dès qu'au moins une des deux coordonnées est imputée ou prior. |
| **`prior_variance_inflation`** | Terme `diag(σ_prior²)` ajouté à `M(s)` pour les États dont `x_score_provenance != observed`, propageant l'incertitude d'imputation. |

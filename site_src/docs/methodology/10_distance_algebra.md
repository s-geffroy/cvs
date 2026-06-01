# 10 — Algèbre des distances civilisationnelles

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.**

## 1. Besoin

Comparer rigoureusement deux États (ou un État et une civilisation, ou deux civilisations) dans un cadre cohérent et **multi-métrique**, parce qu'aucune distance unique ne capture toutes les facettes d'une affinité civilisationnelle :

- distance **visuelle** dans le plan IW,
- distance **psycho-sociale** dans Hofstede,
- distance **d'identité** sur le simplexe d'affinité,
- distance **de structure interne** entre seconds moments `M(s)` (cf. [doc 09](09_civilizational_second_moment.md)).

## 2. Définitions formelles

Soit deux États `s` et `t`, leurs coordonnées `(xₛ^viz, xₛ^score, wₛ, M_s)` et `(xₜ^viz, xₜ^score, wₜ, M_t)`.

### 2.1 Distance visuelle dans `B_viz`

```
d_viz(s, t) = ||xₛ^viz − xₜ^viz||₂
```

Euclidienne dans le plan Inglehart-Welzel. **Distance primaire de visualisation.**

### 2.2 Distance Euclidienne dans `B_score`

```
d_score^E(s, t) = ||xₛ^score − xₜ^score||₂
```

Baseline scoring. Suppose des unités comparables (Hofstede 0-100 par axe).

### 2.3 Mahalanobis dans `B_score` — deux versions

La v3.0 publie **deux** versions de la distance de Mahalanobis (cf. [doc 11 §D14](11_critiques_and_responses.md)) :

#### 2.3.1 Inter-civilisationnelle (centroïdes) — `d_score_mahalanobis_centroids`

```
d_score^M_centroids(s, t) = √( (xₛ − xₜ)ᵀ · Σ_centroids⁻¹ · (xₛ − xₜ) )
```

où `Σ_centroids` est la covariance pondérée des 11 centroïdes civilisationnels dans `B_score` (avec régularisation ridge λ=1.0). Cette version mesure les écarts à l'aune de la **dispersion inter-civilisationnelle**.

**Limite** : estimée sur 11 observations en ℝ⁶ + ridge. Statistiquement **peu robuste**. Conservée pour comparabilité v2.0.

#### 2.3.2 Intra-civilisationnelle (variance interne) — `d_score_mahalanobis_intra` ⭐ **nouveauté v3.0**

```
d_score^M_intra(s, t) = √( (xₛ − xₜ)ᵀ · Σ_intra⁻¹ · (xₛ − xₜ) )
```

où `Σ_intra` est la **covariance intra-civilisationnelle pondérée**, calculée comme :

```
Σ_intra[k, k] = ⟨σᵢ^score[k]²⟩ᵢ                  # moyenne des variances par-axe au sein des civilisations
Σ_intra[k, l] = 0 pour k ≠ l                       # diagonale par approximation
Σ_intra ← Σ_intra + ridge · I                      # régularisation
```

Cette version pondère les axes Hofstede par leur **variance intra-civilisationnelle moyenne** : un axe avec une grande dispersion *à l'intérieur* des civilisations (par exemple MAS — culturalement bruité) pèse moins dans la distance qu'un axe avec une faible dispersion (par exemple LTO, plus discriminant).

**C'est la version recommandée par défaut**, utilisée par `d_hyb`.

### 2.4 Distance cosinus sur les vecteurs d'affinité

```
d_w^cos(s, t) = 1 − (wₛ · wₜ) / (||wₛ||₂ · ||wₜ||₂)
```

**Distance d'identité civilisationnelle**. ⚠️ **Ce n'est pas une vraie distance** (ne vérifie pas l'inégalité triangulaire) — étiquetée `dissimilarity` dans le code.

### 2.5 Divergence de Jensen-Shannon

```
M     = (wₛ + wₜ) / 2
JSD   = (1/2) · KL(wₛ || M) + (1/2) · KL(wₜ || M)
d_w^JS(s, t) = √JSD
```

`d_w^JS` est une **vraie distance** (la racine carrée de la divergence JS satisfait l'inégalité triangulaire). **Distance d'information** sur les distributions d'affinité.

### 2.6 Distance de Wasserstein-2 sur le simplexe

Sur le simplexe Δ¹⁰ des 11 civilisations, avec matrice de coûts au sol :

```
D_ij = ||μᵢ^score − μⱼ^score||₂
```

la distance de Wasserstein-2 est :

```
d_w^W(s, t) = √( min_π Σ_{i,j} π_ij · D_ij²   s.t.  Σ_j π_ij = wₛ[i],  Σ_i π_ij = wₜ[j] )
```

**Distance géométriquement consistante** : deux États proches de civilisations adjacentes ont une `d_w^W` plus faible que de civilisations éloignées.

**Implémentation** : algorithme de Sinkhorn (régularisation entropique, ε=0.05) en NumPy pur — voir `packages/civvec_core/algebra/transport.py`. **Pas de dépendance POT.**

#### Circularité partielle assumée

`d_w^W` utilise des **affinités `w`** dérivées des **centroïdes `μ`**, et un **coût au sol** lui-même dérivé des mêmes centroïdes. Cette circularité est **explicitement reconnue** (cf. [doc 11 §D16](11_critiques_and_responses.md)) : la métrique est fiable **pour comparer deux États relativement**, mais ne donne pas une mesure absolue interprétable hors de ce contexte.

Travail futur : explorer un coût au sol indépendant (par exemple distances Pew religieuses inter-civilisations).

### 2.7 Distance de Frobenius sur les seconds moments

```
d_M_F(s, t) = ||M(s) − M(t)||_F = √( Σ_{i,j} (M_s[i,j] − M_t[i,j])² )
```

**Distance de structure interne** : deux États avec des seconds moments similaires (mêmes directions principales, magnitudes comparables) sont proches.

Renommée v3.0 depuis `d_T_frobenius` (anciennement « Frobenius sur les tenseurs de tension »).

### 2.8 Distance hybride

#### Définition formelle v3.0

Chaque composante est **normalisée par sa médiane panel** avant la combinaison convexe :

```
d̃ = d / median(d_panel_off_diagonal_upper_triangle)

d_hyb(s, t) = α · d̃_score^M_intra(s, t)  +  β · d̃_w^W(s, t)  +  γ · d̃_M_F(s, t)
```

avec `α + β + γ = 1`.

**Justification de la normalisation** : sans elle, les trois composantes opèrent sur des échelles différentes (Mahalanobis ~ 0.5-3, Wasserstein ~ 20-100 sur Hofstede 0-100, Frobenius ~ 1000-10000). La médiane panel ramène chaque composante à un panel relatif où 1.0 = médiane, ce qui rend les poids `(α, β, γ)` interprétables comme **importances relatives**, pas comme arbitrages d'unités.

#### Poids par défaut

V3.0 : `α = 0.4`, `β = 0.4`, `γ = 0.2`.

Ce choix privilégie la position Hofstede et l'affinité tout en intégrant l'information structurelle. La sensibilité à ce choix est mesurée dans [doc 13](13_sensitivity_analysis.md) — typiquement, le clustering est robuste pour `(α, β, γ)` proches de l'uniforme (0.33, 0.33, 0.33) mais sensible aux coins.

Poids modifiables interactivement via la page Streamlit `9_Distance_Algebra.py`.

## 3. Propriétés (à garantir par tests)

| Distance | Non-négativité | Symétrie | Identité d(s,s)=0 | Triangle |
|---|---|---|---|---|
| `d_viz` | ✓ | ✓ | ✓ | ✓ |
| `d_score^E` | ✓ | ✓ | ✓ | ✓ |
| `d_score^M_centroids` | ✓ | ✓ | ✓ | ✓ |
| `d_score^M_intra` | ✓ | ✓ | ✓ | ✓ |
| `d_w^cos` | ✓ | ✓ | ✓ | ✗ |
| `d_w^JS` | ✓ | ✓ | ✓ | ✓ |
| `d_w^W` | ✓ | ✓ | ✓ | ✓ |
| `d_M_F` | ✓ | ✓ | ✓ | ✓ |
| `d_hyb` | ✓ | ✓ | ✓ | ✓ (par combinaison convexe) |

Tests dans `tests/test_distance_algebra.py`.

## 4. Cas d'usage

| Question | Distance recommandée |
|---|---|
| Quels États sont visuellement proches ? | `d_viz` |
| Quels États ont des dimensions Hofstede similaires (robuste) ? | `d_score^M_intra` |
| Quels États ont des dimensions Hofstede similaires (centroid-aware) ? | `d_score^M_centroids` |
| Quels États ont la même identité civilisationnelle ? | `d_w^cos` ou `d_w^JS` |
| Quels États ont des affinités géométriquement cohérentes ? | `d_w^W` |
| Quels États ont la même structure de second moment ? | `d_M_F` |
| Quels États sont globalement les plus proches ? | `d_hyb` |
| Clustering hiérarchique des États | `d_hyb` (linkage Ward) |

## 5. Schéma JSON

Cf. `schemas/distance_matrix.schema.json`. La matrice publiée porte toutes les métriques :

```json
{
  "_meta": {
    "schema": "distance_matrix.schema.json",
    "n_states": 60,
    "hybrid_weights": { "alpha": 0.4, "beta": 0.4, "gamma": 0.2 },
    "hybrid_components_normalised_by": "panel_median",
    "hybrid_components": [
      "d_score_mahalanobis_intra",
      "d_w_wasserstein",
      "d_M_frobenius"
    ],
    "panel_medians": { ... },
    "affinity_beta": 0.05
  },
  "iso3_order": ["ARG", "AUS", ...],
  "matrices": {
    "d_viz": [...],
    "d_score_euclidean": [...],
    "d_score_mahalanobis_centroids": [...],
    "d_score_mahalanobis_intra": [...],
    "d_w_cosine": [...],
    "d_w_js": [...],
    "d_w_wasserstein": [...],
    "d_M_frobenius": [...],
    "d_hybrid": [...]
  }
}
```

## 6. Limites

1. **Sensibilité aux centroïdes** : `d_score^M_centroids`, `d_score^M_intra`, `d_w^W`, `d_M_F` dépendent toutes des `μᵢ^score`. Sensibilité quantifiée dans [doc 13](13_sensitivity_analysis.md).
2. **Wasserstein coûteux** : O(n²) par paire d'États. Précalcul matrices NxN persistées en JSON pour panels stables. Le build site précalcule la matrice panel complète.
3. **Hybride éditorial** : les poids `(α, β, γ) = (0.4, 0.4, 0.2)` sont un choix de design **assumé** et **soumis à relecture**. La sensibilité publiée permet d'observer leur impact.
4. **Pas de distance temporelle** : V1 ne modélise pas la dérive culturelle (waves WVS successives). Phase ultérieure.
5. **Circularité de `d_w^W`** : voir §2.6.

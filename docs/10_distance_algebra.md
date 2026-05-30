# 10 — Algèbre des distances civilisationnelles

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.**

## 1. Besoin

Comparer rigoureusement deux États (ou un État et une civilisation, ou deux civilisations) dans un cadre cohérent et **multi-métrique**, parce qu'aucune distance unique ne capture toutes les facettes d'une affinité civilisationnelle :

- distance **visuelle** dans le plan IW,
- distance **psycho-sociale** dans Hofstede,
- distance **d'identité** sur le simplexe d'affinité,
- distance **de structure interne** entre tenseurs de tension.

## 2. Définitions formelles

Soit deux États `s` et `t`, leurs coordonnées `(x_s^viz, x_s^score, w_s, T_s)` et `(x_t^viz, x_t^score, w_t, T_t)`.

### 2.1 Distance visuelle dans `B_viz`

```
d_viz(s, t) = ||x_s^viz − x_t^viz||₂
```

Euclidienne dans le plan Inglehart-Welzel. **Distance primaire de visualisation.**

### 2.2 Distance Euclidienne dans `B_score`

```
d_score^E(s, t) = ||x_s^score − x_t^score||₂
```

Baseline scoring. Suppose des unités comparables (Hofstede 0-100 par axe).

### 2.3 Distance de Mahalanobis dans `B_score`

```
d_score^M(s, t) = sqrt( (x_s − x_t)^T · Σ^{-1} · (x_s − x_t) )
```

où `Σ` est la matrice de covariance pondérée sur les 11 civilisations dans `B_score`. **Scoring robuste** : pondère implicitement les axes selon leur variance inter-civilisationnelle.

### 2.4 Distance cosinus sur les vecteurs d'affinité

```
d_w^cos(s, t) = 1 − (w_s · w_t) / (||w_s||₂ · ||w_t||₂)
```

**Distance d'identité civilisationnelle**. ⚠️ **Ce n'est pas une vraie distance** (ne vérifie pas l'inégalité triangulaire) — étiquetée `dissimilarity` dans le code.

### 2.5 Divergence de Jensen-Shannon

```
M     = (w_s + w_t) / 2
JSD   = (1/2) · KL(w_s || M) + (1/2) · KL(w_t || M)
d_w^JS(s, t) = sqrt(JSD)
```

`d_w^JS` est une **vraie distance** (la racine carrée de la divergence JS satisfait l'inégalité triangulaire). **Distance d'information** sur les distributions d'affinité.

### 2.6 Distance de Wasserstein-2 sur le simplexe

Sur le simplexe Δ¹⁰ des 11 civilisations, avec matrice de coûts au sol :

```
D_ij = ||μ_i^score − μ_j^score||₂
```

la distance de Wasserstein-2 est :

```
d_w^W(s, t) = sqrt( min_π Σ_{i,j} π_ij · D_ij²   s.t.  Σ_j π_ij = w_s[i],  Σ_i π_ij = w_t[j] )
```

**Distance géométriquement consistante** : deux États proches d'civilisations adjacentes ont une `d_w^W` plus faible que d'civilisations éloignées.

**Implémentation** : algorithme de Sinkhorn (régularisation entropique, λ=0.01) en NumPy pur — voir `packages/civvec_core/algebra/transport.py`. **Pas de dépendance POT.**

### 2.7 Distance de Frobenius sur les tenseurs de tension

```
d_T(s, t) = ||T(s) − T(t)||_F = sqrt( Σ_{i,j} (T_s[i,j] − T_t[i,j])² )
```

**Distance de structure interne** : deux États avec des fractures civilisationnelles similaires (même orientation, même magnitude) sont proches.

### 2.8 Distance hybride

```
d_hyb(s, t) = α · d_score^M(s, t) + β · d_w^W(s, t) + γ · d_T(s, t)
```

avec normalisation préalable de chaque composante par sa médiane sur le panel d'États publiés, puis `α + β + γ = 1`.

**Poids par défaut V1** : `α = 0.4`, `β = 0.4`, `γ = 0.2`.

Ce choix privilégie la position Hofstede et l'affinité tout en intégrant l'information structurelle. Modifiable interactivement via la page Streamlit `9_Distance_Algebra.py`.

## 3. Propriétés (à garantir par tests)

| Distance | Non-négativité | Symétrie | Identité d(s,s)=0 | Triangle |
|---|---|---|---|---|
| `d_viz` | ✓ | ✓ | ✓ | ✓ |
| `d_score^E` | ✓ | ✓ | ✓ | ✓ |
| `d_score^M` | ✓ | ✓ | ✓ | ✓ |
| `d_w^cos` | ✓ | ✓ | ✓ | ✗ |
| `d_w^JS` | ✓ | ✓ | ✓ | ✓ |
| `d_w^W` | ✓ | ✓ | ✓ | ✓ |
| `d_T` | ✓ | ✓ | ✓ | ✓ |
| `d_hyb` | ✓ | ✓ | ✓ | ✓ (par combinaison convexe) |

Tests dans `tests/test_distance_algebra.py`.

## 4. Cas d'usage

| Question | Distance recommandée |
|---|---|
| Quels États sont visuellement proches ? | `d_viz` |
| Quels États ont des dimensions Hofstede similaires ? | `d_score^M` |
| Quels États ont la même identité civilisationnelle ? | `d_w^cos` ou `d_w^JS` |
| Quels États ont des affinités géométriquement cohérentes ? | `d_w^W` |
| Quels États ont la même structure de fracture interne ? | `d_T` |
| Quels États sont globalement les plus proches ? | `d_hyb` |
| Clustering hiérarchique des États | `d_hyb` (linkage Ward) |

## 5. Schéma JSON

Cf. `schemas/distance_matrix.schema.json`. Une matrice publiée porte :

```json
{
  "metric": "d_hybrid",
  "labels": ["USA", "FRA", "JPN", ...],
  "matrix": [[0, ...], ...],
  "hybrid_weights": { "alpha": 0.4, "beta": 0.4, "gamma": 0.2 }
}
```

## 6. Limites

1. **Sensibilité aux centroïdes** : `d_score^M`, `d_w^W`, `d_T` dépendent toutes des `μ_i^score`.
2. **Wasserstein coûteux** : O(n²) par paire d'États. Précalcul matrices NxN persistées en JSON pour panels stables.
3. **Hybride arbitraire** : les poids `(α, β, γ) = (0.4, 0.4, 0.2)` sont un choix éditorial à documenter et soumettre à relecture.
4. **Pas de distance temporelle** : V1 ne modélise pas la dérive culturelle (waves WVS successives). Phase ultérieure.

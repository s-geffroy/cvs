# 09 — Mécanique tensorielle des tensions internes d'un État

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.**

## 1. Motivation

Un État qui agrège plusieurs composantes civilisationnelles porte une **tension interne** mesurable. La métaphore opératoire vient de la **mécanique des milieux continus** :

- Un État *monoculturel* est analogue à un matériau **isotrope sans contrainte** : `T = 0`.
- Un État à *fracture civilisationnelle* (Liban, Bosnie, Belgique, Ukraine, Inde, Nigeria) est analogue à un matériau **sous contrainte anisotrope** : `T ≠ 0`, eigenvalues élevées, anisotropie marquée.

Cette analogie n'est **pas une physique** — c'est une grille de lecture opérationnelle, à valider empiriquement sur les cas connus.

## 2. Formulation mathématique

Pour chaque État `s` avec :

- vecteur d'affinité `w_s ∈ Δ¹⁰` (poids sur les 11 macro-civilisations, simplexe),
- coordonnée `x_s ∈ B_score = ℝ⁶` (vecteur Hofstede 6D),
- centroïdes `μ_i^score ∈ ℝ⁶` des civilisations `i = 1..11`,

on définit le **tenseur de tension civilisationnelle** :

```
T(s) = Σ_i w_s[i] · (μ_i^score − x_s) ⊗ (μ_i^score − x_s)
```

où `u ⊗ v = u·v^T` est l'**outer product**. Le résultat est une matrice `6×6` :

- **symétrique** : `T = T^T`,
- **positive semi-définie** : pour tout vecteur `u`, `u^T T u = Σ_i w_s[i] · ((μ_i - x_s) · u)² ≥ 0`.

### 2.1 Invariants scalaires

| Invariant | Formule | Interprétation |
|---|---|---|
| `I1` | `tr(T)` | **Tension totale** (somme des variances pondérées) |
| `I2` | `tr(T²) − tr(T)²/n` | **Tension déviatorique** (analogue von Mises) |
| `det` | `det(T)` | **Rigidité civilisationnelle** |

### 2.2 Décomposition propre

```
T(s) = Σ_k λ_k · e_k ⊗ e_k   avec λ_1 ≥ ... ≥ λ_6 ≥ 0
```

- `λ_k` = **tensions principales** (variances projetées sur les directions propres).
- `e_k` = **directions principales de tension** dans `B_score` — axes Hofstede combinés où la fracture est maximale.

### 2.3 Index d'anisotropie

```
A(s) = (λ_1 − λ_6) / λ_1   ∈ [0, 1]
```

- `A ≈ 0` : tensions **isotropes** — État équilibré, fractures réparties uniformément.
- `A ≈ 1` : tension **concentrée sur un axe** — État avec une fracture nette dans une direction Hofstede combinée.
- Convention : si `λ_1 < ε`, alors `A := 0` (État monocivilisationnel).

## 3. Propriétés et cas limites

### 3.1 État monocivilisationnel

Si `w_s[i₀] = 1` pour un unique `i₀`, et `x_s = μ_{i₀}^score`, alors `T(s) = 0`.

→ Aucune tension interne. Eigenvalues toutes nulles. `A := 0` par convention.

### 3.2 État équilibré entre 2 civilisations distantes

Si `w_s[i] = w_s[j] = 0.5` et `x_s = (μ_i + μ_j) / 2` :

```
T(s) = 0.5 · (μ_i - x_s)(μ_i - x_s)^T + 0.5 · (μ_j - x_s)(μ_j - x_s)^T
     = 0.5 · 2 · ((μ_i - μ_j)/2)((μ_i - μ_j)/2)^T
     = (1/4) · (μ_i - μ_j)(μ_i - μ_j)^T
```

→ `λ_1 = ||μ_i - μ_j||² / 4`, `λ_2 = ... = λ_6 = 0` → `A = 1`.

Cas extrême : fracture parfaite alignée sur la direction `μ_i - μ_j`.

### 3.3 État au centre du simplexe

Si `w_s[i] = 1/11` pour tout `i` et `x_s = (1/11) Σ_i μ_i` (barycentre global) :

```
T(s) = (1/11) Σ_i (μ_i - x_s)(μ_i - x_s)^T
```

→ Matrice de covariance des 11 centroïdes — tension répartie, anisotropie modérée.

## 4. Schéma JSON

Cf. `schemas/state_tension.schema.json`. Champs publiés par État :

```json
{
  "iso3": "FRA",
  "T": [[6x6 matrix]],
  "eigenvalues": [λ_1, ..., λ_6],
  "eigenvectors": [[e_1], ..., [e_6]],
  "invariants": { "I1": ..., "I2": ..., "det": ... },
  "anisotropy": 0.42,
  "quality_flags": { "monocivilizational": false, "low_evidence": false }
}
```

## 5. Tests

`tests/test_tensor_mechanics.py` couvre :

- `test_tensor_is_symmetric` : `||T - T^T||_F < ε`.
- `test_tensor_is_psd` : eigenvalues ≥ −ε.
- `test_invariants_non_negative` : `I1 ≥ 0`, `det ≥ 0`.
- `test_monocivilizational_state_has_zero_tension` : si `w_s` one-hot et `x_s = μ_{argmax(w_s)}`, `T = 0`.
- `test_anisotropy_in_unit_interval` : `A ∈ [0, 1]`.
- `test_principal_directions_are_orthonormal` : `e_k · e_l = δ_kl`.

## 6. Interprétation appliquée — exemples illustratifs

| État | Profil attendu | `I1` | Anisotropie | Interprétation |
|---|---|---|---|---|
| JPN | Quasi monocivilisationnel (Japanese) | bas | basse | État cohérent |
| FRA | Western dominant + influences ibères/méditerranéennes | moyen | modérée | Identité affirmée mais avec sous-courants |
| TUR | Western / Islamic / Sinic-Orthodox marginal | élevé | élevée | Fracture documentée (UE vs Moyen-Orient) |
| IND | Hindic dominant + Sinic/Islamic minoritaires | élevé | modérée | Vaste héritage multi-civilisationnel |
| LBN | Western / Islamic / Orthodox imbriqués | très élevé | très élevée | Tension multi-confessionnelle structurelle |

Ces lectures sont à confronter aux données réelles via la page Streamlit `8_State_Tensions.py`.

## 7. Limites et précautions

1. **Pas de causalité** : le tenseur mesure une **structure géométrique**, pas une dynamique de conflit. Il ne prédit ni instabilité politique ni guerre civile.
2. **Sensibilité aux centroïdes** : `T(s)` dépend des `μ_i^score`. Une modification d'États archétypes modifie l'image tensionnelle.
3. **Métrique Euclidienne** : l'outer product utilise la distance Euclidienne dans `B_score`, qui suppose des unités comparables (Hofstede 0-100 par axe — vérifié).
4. **Affinité dérivée** : `w_s` est issu d'une softmax inverse-distance, donc déjà fonction de `x_s`. Le tenseur est cohérent mais redondant ; lire les invariants plus que la matrice brute.

# Égypte (`EGY`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Égypte ·
**ISO3** : `EGY` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = observed` ·
`x_score = observed` · centroïde de repli : `islamic`.



## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.550, -1.200]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `70.0` | `e_PDI` |
| Individualism (IDV) | `25.0` | `e_IDV` |
| Masculinity (MAS) | `45.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `80.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `7.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `4.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.3318` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1555` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0912` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0818` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0777` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0722` |

| [African](../taxonomy/civilizations/african.md) | `0.0721` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0496` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0320` |

| [Western](../taxonomy/civilizations/western.md) | `0.0237` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0123` |




## Second moment civilisationnel `M(EGY)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3833.05` | Magnitude totale du second moment |
| `I2` (von Mises) | `3246.53` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `3.76e+13` | Déterminant |
| `A` (anisotropie) | `0.991` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `923.69` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `2909.36` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `0.00` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[3045.7, 334.13, 267.78, 114.3, 43.16, 27.97]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`EGY.geojson`](../assets/data/states/EGY.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`EGY.profile.json`)](../assets/data/states/EGY.profile.json)

- [Géométrie (`EGY.geojson`)](../assets/data/states/EGY.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

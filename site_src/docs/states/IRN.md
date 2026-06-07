# Iran (`IRN`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Iran ·
**ISO3** : `IRN` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = observed` ·
`x_score = observed` · centroïde de repli : `islamic`.



## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.100, -0.400]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `58.0` | `e_PDI` |
| Individualism (IDV) | `41.0` | `e_IDV` |
| Masculinity (MAS) | `43.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `59.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `14.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `40.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.2054` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1612` |

| [African](../taxonomy/civilizations/african.md) | `0.1516` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1172` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0937` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0845` |

| [Western](../taxonomy/civilizations/western.md) | `0.0694` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0491` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0308` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0288` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0083` |




## Second moment civilisationnel `M(IRN)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `2070.07` | Magnitude totale du second moment |
| `I2` (von Mises) | `1183.28` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `1.35e+13` | Déterminant |
| `A` (anisotropie) | `0.983` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1030.43` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `1039.64` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `0.00` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[1162.59, 445.16, 287.07, 116.34, 38.67, 20.23]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`IRN.geojson`](../assets/data/states/IRN.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`IRN.profile.json`)](../assets/data/states/IRN.profile.json)

- [Géométrie (`IRN.geojson`)](../assets/data/states/IRN.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

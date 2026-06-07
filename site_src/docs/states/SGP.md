# Singapour (`SGP`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Singapour ·
**ISO3** : `SGP` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = observed` ·
`x_score = observed` · centroïde de repli : `sinic`.



## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.300, -0.400]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `74.0` | `e_PDI` |
| Individualism (IDV) | `20.0` | `e_IDV` |
| Masculinity (MAS) | `48.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `8.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `72.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `46.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.4704` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1431` |

| [African](../taxonomy/civilizations/african.md) | `0.0798` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0763` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0568` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0507` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0439` |

| [Western](../taxonomy/civilizations/western.md) | `0.0286` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0201` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0191` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0113` |




## Second moment civilisationnel `M(SGP)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `2872.63` | Magnitude totale du second moment |
| `I2` (von Mises) | `2332.91` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `8.91e+12` | Déterminant |
| `A` (anisotropie) | `0.992` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1056.03` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `1816.60` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `0.00` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[2203.61, 305.99, 201.83, 108.86, 35.3, 17.03]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`SGP.geojson`](../assets/data/states/SGP.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`SGP.profile.json`)](../assets/data/states/SGP.profile.json)

- [Géométrie (`SGP.geojson`)](../assets/data/states/SGP.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

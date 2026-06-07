# Thaïlande (`THA`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Thaïlande ·
**ISO3** : `THA` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = observed` ·
`x_score = observed` · centroïde de repli : `buddhist`.



## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.200, 0.200]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `64.0` | `e_PDI` |
| Individualism (IDV) | `20.0` | `e_IDV` |
| Masculinity (MAS) | `34.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `64.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `32.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `45.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.2239` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1842` |

| [African](../taxonomy/civilizations/african.md) | `0.1275` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1079` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.1037` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0841` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0505` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0427` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0415` |

| [Western](../taxonomy/civilizations/western.md) | `0.0270` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0070` |




## Second moment civilisationnel `M(THA)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1407.36` | Magnitude totale du second moment |
| `I2` (von Mises) | `560.02` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `9.17e+12` | Déterminant |
| `A` (anisotropie) | `0.969` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `894.62` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `512.73` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `0.00` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[561.46, 366.15, 264.43, 104.02, 94.06, 17.24]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`THA.geojson`](../assets/data/states/THA.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`THA.profile.json`)](../assets/data/states/THA.profile.json)

- [Géométrie (`THA.geojson`)](../assets/data/states/THA.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

# Venezuela (`VEN`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Venezuela ·
**ISO3** : `VEN` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = observed` ·
`x_score = observed` · centroïde de repli : `latin_american`.



## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.100, 0.700]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0484, 0.0000],
   [0.0000, 0.0484]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `81.0` | `e_PDI` |
| Individualism (IDV) | `12.0` | `e_IDV` |
| Masculinity (MAS) | `73.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `76.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `16.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `100.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.3324` |

| [African](../taxonomy/civilizations/african.md) | `0.2091` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1198` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0984` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0753` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0665` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0226` |

| [Western](../taxonomy/civilizations/western.md) | `0.0221` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0194` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0190` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0153` |




## Second moment civilisationnel `M(VEN)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3999.78` | Magnitude totale du second moment |
| `I2` (von Mises) | `3643.42` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `6.23e+12` | Déterminant |
| `A` (anisotropie) | `0.997` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `849.04` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `3150.74` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `0.00` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[3373.12, 319.35, 155.77, 99.44, 43.54, 8.57]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`VEN.geojson`](../assets/data/states/VEN.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`VEN.profile.json`)](../assets/data/states/VEN.profile.json)

- [Géométrie (`VEN.geojson`)](../assets/data/states/VEN.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

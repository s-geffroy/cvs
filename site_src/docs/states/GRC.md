# Grèce (`GRC`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Grèce ·
**ISO3** : `GRC` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = observed` ·
`x_score = observed` · centroïde de repli : `orthodox`.



## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.100, 0.050]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `60.0` | `e_PDI` |
| Individualism (IDV) | `35.0` | `e_IDV` |
| Masculinity (MAS) | `57.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `112.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `45.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `50.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.2070` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1493` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1326` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.1312` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1038` |

| [African](../taxonomy/civilizations/african.md) | `0.0733` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0665` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0544` |

| [Western](../taxonomy/civilizations/western.md) | `0.0338` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0291` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0192` |




## Second moment civilisationnel `M(GRC)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `2872.50` | Magnitude totale du second moment |
| `I2` (von Mises) | `1833.34` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `4.64e+13` | Déterminant |
| `A` (anisotropie) | `0.992` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1283.38` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `1589.12` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `0.00` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[1799.08, 452.05, 378.62, 165.85, 62.33, 14.57]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`GRC.geojson`](../assets/data/states/GRC.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`GRC.profile.json`)](../assets/data/states/GRC.profile.json)

- [Géométrie (`GRC.geojson`)](../assets/data/states/GRC.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

# Fidji (`FJI`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Fidji ·
**ISO3** : `FJI` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = observed` ·
`x_score = observed_with_dim_imputation` · centroïde de repli : `oceanian`.



## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.800, 0.400]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0900, 0.0000],
   [0.0000, 0.0900]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `78.0` | `e_PDI` |
| Individualism (IDV) | `14.0` | `e_IDV` |
| Masculinity (MAS) | `46.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `48.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `46.5` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `46.5` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1951` |

| [African](../taxonomy/civilizations/african.md) | `0.1516` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1410` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1225` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.1170` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0845` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0688` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0570` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0364` |

| [Western](../taxonomy/civilizations/western.md) | `0.0175` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0086` |




## Second moment civilisationnel `M(FJI)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1422.11` | Magnitude totale du second moment |
| `I2` (von Mises) | `618.40` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `3.89e+12` | Déterminant |
| `A` (anisotropie) | `0.978` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `985.12` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `436.99` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `0.00` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[604.48, 370.91, 265.56, 130.05, 37.86, 13.25]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`FJI.geojson`](../assets/data/states/FJI.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`FJI.profile.json`)](../assets/data/states/FJI.profile.json)

- [Géométrie (`FJI.geojson`)](../assets/data/states/FJI.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

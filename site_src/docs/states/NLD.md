# Pays-Bas (`NLD`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Pays-Bas ·
**ISO3** : `NLD` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = observed` ·
`x_score = observed` · centroïde de repli : `western`.



## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[1.450, 1.650]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `38.0` | `e_PDI` |
| Individualism (IDV) | `80.0` | `e_IDV` |
| Masculinity (MAS) | `14.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `53.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `67.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `68.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Western](../taxonomy/civilizations/western.md) | `0.4958` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1637` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0566` |

| [African](../taxonomy/civilizations/african.md) | `0.0561` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0414` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0405` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0364` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0339` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0287` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0283` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0185` |




## Second moment civilisationnel `M(NLD)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3893.90` | Magnitude totale du second moment |
| `I2` (von Mises) | `3292.78` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `2.25e+13` | Déterminant |
| `A` (anisotropie) | `0.997` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1245.57` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `2648.32` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `0.00` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[3086.71, 416.39, 180.14, 128.09, 72.06, 10.51]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`NLD.geojson`](../assets/data/states/NLD.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`NLD.profile.json`)](../assets/data/states/NLD.profile.json)

- [Géométrie (`NLD.geojson`)](../assets/data/states/NLD.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

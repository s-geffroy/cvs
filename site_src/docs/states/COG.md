# Congo (`COG`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Congo ·
**ISO3** : `COG` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = imputed_pew` ·
`x_score = imputed_governance` · centroïde de repli : `african`.

> ⚠️ `x_viz` n'est **pas une observation directe** : voir [doc 16](../methodology/16_imputation_cascade.md) pour les implications.


> ⚠️ `x_score` n'est **pas une observation directe** : la variance prior est gonflée dans `M(s)` ci-dessous.


## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.260, -0.235]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.2329, 0.0000],
   [0.0000, 0.4197]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `57.0` | `e_PDI` |
| Individualism (IDV) | `33.8` | `e_IDV` |
| Masculinity (MAS) | `50.4` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `35.8` | `e_UAI` |
| Long-Term Orientation (LTO) | `30.4` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `41.6` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.2119` |

| [African](../taxonomy/civilizations/african.md) | `0.1711` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1452` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1303` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0861` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0806` |

| [Western](../taxonomy/civilizations/western.md) | `0.0608` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0451` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0417` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0185` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0086` |




## Second moment civilisationnel `M(COG)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3979.80` | Magnitude totale du second moment |
| `I2` (von Mises) | `1068.01` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `3.59e+16` | Déterminant |
| `A` (anisotropie) | `0.797` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1054.13` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `742.85` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[1324.9, 844.12, 708.6, 490.11, 342.73, 269.34]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`COG.geojson`](../assets/data/states/COG.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`COG.profile.json`)](../assets/data/states/COG.profile.json)

- [Géométrie (`COG.geojson`)](../assets/data/states/COG.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

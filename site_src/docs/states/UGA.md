# Ouganda (`UGA`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Ouganda ·
**ISO3** : `UGA` ·
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
  `[-1.519, -0.537]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.2329, 0.0000],
   [0.0000, 0.4197]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `57.5` | `e_PDI` |
| Individualism (IDV) | `29.1` | `e_IDV` |
| Masculinity (MAS) | `48.8` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `30.1` | `e_UAI` |
| Long-Term Orientation (LTO) | `29.3` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `38.3` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1819` |

| [African](../taxonomy/civilizations/african.md) | `0.1608` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1600` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1367` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.1036` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0898` |

| [Western](../taxonomy/civilizations/western.md) | `0.0538` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0437` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0424` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0192` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0081` |




## Second moment civilisationnel `M(UGA)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `4380.20` | Magnitude totale du second moment |
| `I2` (von Mises) | `1414.28` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `4.88e+16` | Déterminant |
| `A` (anisotropie) | `0.841` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1071.78` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `1125.60` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[1680.91, 869.28, 705.16, 511.7, 345.3, 267.85]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`UGA.geojson`](../assets/data/states/UGA.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`UGA.profile.json`)](../assets/data/states/UGA.profile.json)

- [Géométrie (`UGA.geojson`)](../assets/data/states/UGA.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

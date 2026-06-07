# Ouzbékistan (`UZB`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Ouzbékistan ·
**ISO3** : `UZB` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = imputed_wvs_items` ·
`x_score = imputed_governance` · centroïde de repli : `islamic`.

> ⚠️ `x_viz` n'est **pas une observation directe** : voir [doc 16](../methodology/16_imputation_cascade.md) pour les implications.


> ⚠️ `x_score` n'est **pas une observation directe** : la variance prior est gonflée dans `M(s)` ci-dessous.


## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.804, 0.388]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.1415, 0.0000],
   [0.0000, 0.2934]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `67.9` | `e_PDI` |
| Individualism (IDV) | `31.2` | `e_IDV` |
| Masculinity (MAS) | `45.1` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `43.3` | `e_UAI` |
| Long-Term Orientation (LTO) | `44.4` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `32.7` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.2040` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1643` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.1267` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1197` |

| [African](../taxonomy/civilizations/african.md) | `0.1121` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1028` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0556` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0353` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0350` |

| [Western](../taxonomy/civilizations/western.md) | `0.0350` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0096` |




## Second moment civilisationnel `M(UZB)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3601.56` | Magnitude totale du second moment |
| `I2` (von Mises) | `820.70` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `2.36e+16` | Déterminant |
| `A` (anisotropie) | `0.774` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1084.44` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `334.31` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[1064.48, 763.51, 688.24, 479.22, 365.66, 240.46]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`UZB.geojson`](../assets/data/states/UZB.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`UZB.profile.json`)](../assets/data/states/UZB.profile.json)

- [Géométrie (`UZB.geojson`)](../assets/data/states/UZB.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

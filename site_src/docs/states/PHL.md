# Philippines (`PHL`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Philippines ·
**ISO3** : `PHL` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = imputed_wvs_items` ·
`x_score = imputed_governance` · centroïde de repli : `latin_american`.

> ⚠️ `x_viz` n'est **pas une observation directe** : voir [doc 16](../methodology/16_imputation_cascade.md) pour les implications.


> ⚠️ `x_score` n'est **pas une observation directe** : la variance prior est gonflée dans `M(s)` ci-dessous.


## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.343, 0.687]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.1415, 0.0000],
   [0.0000, 0.2934]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `63.9` | `e_PDI` |
| Individualism (IDV) | `30.2` | `e_IDV` |
| Masculinity (MAS) | `46.4` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `51.4` | `e_UAI` |
| Long-Term Orientation (LTO) | `38.7` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `47.1` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [African](../taxonomy/civilizations/african.md) | `0.1935` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1518` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1497` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1398` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0923` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0689` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0640` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0638` |

| [Western](../taxonomy/civilizations/western.md) | `0.0397` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0273` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0091` |




## Second moment civilisationnel `M(PHL)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3347.31` | Magnitude totale du second moment |
| `I2` (von Mises) | `648.39` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `1.78e+16` | Déterminant |
| `A` (anisotropie) | `0.702` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1000.45` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `164.04` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[817.89, 798.73, 659.04, 460.62, 367.12, 243.9]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`PHL.geojson`](../assets/data/states/PHL.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`PHL.profile.json`)](../assets/data/states/PHL.profile.json)

- [Géométrie (`PHL.geojson`)](../assets/data/states/PHL.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

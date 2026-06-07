# Papouasie-Nouvelle-Guinée (`PNG`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Papouasie-Nouvelle-Guinée ·
**ISO3** : `PNG` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = imputed_pew` ·
`x_score = imputed_governance` · centroïde de repli : `oceanian`.

> ⚠️ `x_viz` n'est **pas une observation directe** : voir [doc 16](../methodology/16_imputation_cascade.md) pour les implications.


> ⚠️ `x_score` n'est **pas une observation directe** : la variance prior est gonflée dans `M(s)` ci-dessous.


## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.329, -0.098]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.2329, 0.0000],
   [0.0000, 0.4197]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `54.6` | `e_PDI` |
| Individualism (IDV) | `37.2` | `e_IDV` |
| Masculinity (MAS) | `54.2` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `48.9` | `e_UAI` |
| Long-Term Orientation (LTO) | `25.4` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `43.6` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.2241` |

| [African](../taxonomy/civilizations/african.md) | `0.1858` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1495` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1005` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0915` |

| [Western](../taxonomy/civilizations/western.md) | `0.0650` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0643` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0452` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0441` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0198` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0101` |




## Second moment civilisationnel `M(PNG)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3759.27` | Magnitude totale du second moment |
| `I2` (von Mises) | `912.45` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `2.92e+16` | Déterminant |
| `A` (anisotropie) | `0.758` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1017.87` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `558.59` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[1164.41, 768.89, 749.43, 454.08, 341.1, 281.35]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`PNG.geojson`](../assets/data/states/PNG.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`PNG.profile.json`)](../assets/data/states/PNG.profile.json)

- [Géométrie (`PNG.geojson`)](../assets/data/states/PNG.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

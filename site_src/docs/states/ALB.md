# Albanie (`ALB`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Albanie ·
**ISO3** : `ALB` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = imputed_pew` ·
`x_score = imputed_governance` · centroïde de repli : `islamic`.

> ⚠️ `x_viz` n'est **pas une observation directe** : voir [doc 16](../methodology/16_imputation_cascade.md) pour les implications.


> ⚠️ `x_score` n'est **pas une observation directe** : la variance prior est gonflée dans `M(s)` ci-dessous.


## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.076, 0.115]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.2329, 0.0000],
   [0.0000, 0.4197]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `62.2` | `e_PDI` |
| Individualism (IDV) | `42.6` | `e_IDV` |
| Masculinity (MAS) | `48.6` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `74.3` | `e_UAI` |
| Long-Term Orientation (LTO) | `52.9` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `42.7` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1526` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1407` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1102` |

| [African](../taxonomy/civilizations/african.md) | `0.1046` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0979` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0877` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0844` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0805` |

| [Western](../taxonomy/civilizations/western.md) | `0.0597` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0497` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0319` |




## Second moment civilisationnel `M(ALB)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3756.69` | Magnitude totale du second moment |
| `I2` (von Mises) | `754.09` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `3.24e+16` | Déterminant |
| `A` (anisotropie) | `0.760` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1254.96` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `318.92` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[971.97, 827.76, 720.32, 612.6, 390.93, 233.11]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`ALB.geojson`](../assets/data/states/ALB.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`ALB.profile.json`)](../assets/data/states/ALB.profile.json)

- [Géométrie (`ALB.geojson`)](../assets/data/states/ALB.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

# Tchéquie (`CZE`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Tchéquie ·
**ISO3** : `CZE` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = imputed_wvs_items` ·
`x_score = imputed_governance` · centroïde de repli : `western`.

> ⚠️ `x_viz` n'est **pas une observation directe** : voir [doc 16](../methodology/16_imputation_cascade.md) pour les implications.


> ⚠️ `x_score` n'est **pas une observation directe** : la variance prior est gonflée dans `M(s)` ci-dessous.


## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[1.171, 0.766]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.1415, 0.0000],
   [0.0000, 0.2934]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `61.4` | `e_PDI` |
| Individualism (IDV) | `50.6` | `e_IDV` |
| Masculinity (MAS) | `48.5` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `90.4` | `e_UAI` |
| Long-Term Orientation (LTO) | `49.9` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `56.5` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.1602` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1272` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1093` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1054` |

| [African](../taxonomy/civilizations/african.md) | `0.1046` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0989` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0898` |

| [Western](../taxonomy/civilizations/western.md) | `0.0836` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0482` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0459` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0270` |




## Second moment civilisationnel `M(CZE)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `4451.67` | Magnitude totale du second moment |
| `I2` (von Mises) | `1198.61` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `6.17e+16` | Déterminant |
| `A` (anisotropie) | `0.848` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1358.63` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `910.23` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[1459.85, 933.81, 824.95, 596.6, 414.41, 222.05]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`CZE.geojson`](../assets/data/states/CZE.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`CZE.profile.json`)](../assets/data/states/CZE.profile.json)

- [Géométrie (`CZE.geojson`)](../assets/data/states/CZE.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

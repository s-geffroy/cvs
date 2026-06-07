# Chypre (`CYP`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Chypre ·
**ISO3** : `CYP` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = imputed_wvs_items` ·
`x_score = imputed_governance` · centroïde de repli : `orthodox`.

> ⚠️ `x_viz` n'est **pas une observation directe** : voir [doc 16](../methodology/16_imputation_cascade.md) pour les implications.


> ⚠️ `x_score` n'est **pas une observation directe** : la variance prior est gonflée dans `M(s)` ci-dessous.


## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.457, 0.278]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.1415, 0.0000],
   [0.0000, 0.2934]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `66.1` | `e_PDI` |
| Individualism (IDV) | `43.7` | `e_IDV` |
| Masculinity (MAS) | `50.4` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `81.9` | `e_UAI` |
| Long-Term Orientation (LTO) | `43.8` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `56.5` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.1717` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1478` |

| [African](../taxonomy/civilizations/african.md) | `0.1346` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1149` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1079` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1067` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0610` |

| [Western](../taxonomy/civilizations/western.md) | `0.0551` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0481` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0264` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0257` |




## Second moment civilisationnel `M(CYP)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3731.17` | Magnitude totale du second moment |
| `I2` (von Mises) | `774.10` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `2.94e+16` | Déterminant |
| `A` (anisotropie) | `0.768` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1141.97` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `406.39` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[954.82, 837.1, 758.99, 585.52, 373.49, 221.25]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`CYP.geojson`](../assets/data/states/CYP.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`CYP.profile.json`)](../assets/data/states/CYP.profile.json)

- [Géométrie (`CYP.geojson`)](../assets/data/states/CYP.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

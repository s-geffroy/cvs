# Honduras (`HND`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Honduras ·
**ISO3** : `HND` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = imputed_pew` ·
`x_score = imputed_governance` · centroïde de repli : `latin_american`.

> ⚠️ `x_viz` n'est **pas une observation directe** : voir [doc 16](../methodology/16_imputation_cascade.md) pour les implications.


> ⚠️ `x_score` n'est **pas une observation directe** : la variance prior est gonflée dans `M(s)` ci-dessous.


## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.055, -0.194]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.2329, 0.0000],
   [0.0000, 0.4197]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `65.6` | `e_PDI` |
| Individualism (IDV) | `27.9` | `e_IDV` |
| Masculinity (MAS) | `49.4` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `52.2` | `e_UAI` |
| Long-Term Orientation (LTO) | `33.4` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `44.6` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [African](../taxonomy/civilizations/african.md) | `0.1980` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1853` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1455` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1258` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0888` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0679` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0675` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0548` |

| [Western](../taxonomy/civilizations/western.md) | `0.0321` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0260` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0084` |




## Second moment civilisationnel `M(HND)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3341.45` | Magnitude totale du second moment |
| `I2` (von Mises) | `674.85` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `1.68e+16` | Déterminant |
| `A` (anisotropie) | `0.710` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `946.26` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `212.38` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[835.73, 775.69, 699.92, 446.34, 341.15, 242.62]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`HND.geojson`](../assets/data/states/HND.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`HND.profile.json`)](../assets/data/states/HND.profile.json)

- [Géométrie (`HND.geojson`)](../assets/data/states/HND.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

# Équateur (`ECU`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Équateur ·
**ISO3** : `ECU` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = observed` ·
`x_score = observed_with_dim_imputation` · centroïde de repli : `indigenous`.



## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.050, 0.300]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0484, 0.0000],
   [0.0000, 0.0484]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `78.0` | `e_PDI` |
| Individualism (IDV) | `8.0` | `e_IDV` |
| Masculinity (MAS) | `63.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `67.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `54.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `54.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.2691` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1807` |

| [African](../taxonomy/civilizations/african.md) | `0.1278` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1011` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0887` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0648` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0463` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0462` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0424` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0209` |

| [Western](../taxonomy/civilizations/western.md) | `0.0120` |




## Second moment civilisationnel `M(ECU)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1435.56` | Magnitude totale du second moment |
| `I2` (von Mises) | `633.35` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `4.39e+12` | Déterminant |
| `A` (anisotropie) | `0.985` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `931.63` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `503.93` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `0.00` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[645.03, 326.08, 258.29, 132.64, 64.01, 9.51]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`ECU.geojson`](../assets/data/states/ECU.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`ECU.profile.json`)](../assets/data/states/ECU.profile.json)

- [Géométrie (`ECU.geojson`)](../assets/data/states/ECU.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

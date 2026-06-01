# État `ETH` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `ETH` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.100, -0.650]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0484, 0.0000],
   [0.0000, 0.0484]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `70.0` | `e_PDI` |
| Individualism (IDV) | `20.0` | `e_IDV` |
| Masculinity (MAS) | `65.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `55.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `52.5` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `52.5` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [African](../taxonomy/civilizations/african.md) | `0.2007` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1412` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1288` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1113` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0985` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0935` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0779` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0696` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0328` |

| [Western](../taxonomy/civilizations/western.md) | `0.0230` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0227` |




## Second moment civilisationnel `M(ETH)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1434.78` | Magnitude totale du second moment |
| `I2` (von Mises) | `524.66` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `9.73e+12` | Déterminant |
| `A` (anisotropie) | `0.972` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1073.55` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `361.22` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[515.72, 365.76, 314.37, 148.58, 75.77, 14.57]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`ETH.geojson`](../assets/data/states/ETH.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`ETH.profile.json`)](../assets/data/states/ETH.profile.json)

- [Géométrie (`ETH.geojson`)](../assets/data/states/ETH.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

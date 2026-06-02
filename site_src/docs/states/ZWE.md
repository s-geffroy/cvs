# Zimbabwe (`ZWE`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Zimbabwe ·
**ISO3** : `ZWE` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.150, -0.400]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0625, 0.0000],
   [0.0000, 0.0625]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `75.0` | `e_PDI` |
| Individualism (IDV) | `25.0` | `e_IDV` |
| Masculinity (MAS) | `60.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `55.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `53.8` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `53.8` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [African](../taxonomy/civilizations/african.md) | `0.2007` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1504` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1235` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1091` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0943` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0914` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0849` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0670` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0354` |

| [Western](../taxonomy/civilizations/western.md) | `0.0242` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0191` |




## Second moment civilisationnel `M(ZWE)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1302.57` | Magnitude totale du second moment |
| `I2` (von Mises) | `469.89` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `7.00e+12` | Déterminant |
| `A` (anisotropie) | `0.962` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1059.01` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `243.56` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[456.92, 347.19, 278.2, 136.06, 66.73, 17.48]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`ZWE.geojson`](../assets/data/states/ZWE.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`ZWE.profile.json`)](../assets/data/states/ZWE.profile.json)

- [Géométrie (`ZWE.geojson`)](../assets/data/states/ZWE.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

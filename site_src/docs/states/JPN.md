# État `JPN` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `JPN` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[1.950, 0.450]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `54.0` | `e_PDI` |
| Individualism (IDV) | `46.0` | `e_IDV` |
| Masculinity (MAS) | `95.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `92.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `88.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `42.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.8414` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0228` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0209` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0157` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0155` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0152` |

| [African](../taxonomy/civilizations/african.md) | `0.0148` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0147` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0147` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0128` |

| [Western](../taxonomy/civilizations/western.md) | `0.0115` |




## Second moment civilisationnel `M(JPN)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `993.15` | Magnitude totale du second moment |
| `I2` (von Mises) | `842.59` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `3.95e+09` | Déterminant |
| `A` (anisotropie) | `0.998` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `868.97` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `124.18` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[789.73, 96.56, 59.44, 31.06, 14.42, 1.94]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`JPN.geojson`](../assets/data/states/JPN.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`JPN.profile.json`)](../assets/data/states/JPN.profile.json)

- [Géométrie (`JPN.geojson`)](../assets/data/states/JPN.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

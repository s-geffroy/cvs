# Roumanie (`ROU`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Roumanie ·
**ISO3** : `ROU` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.350, -0.400]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `90.0` | `e_PDI` |
| Individualism (IDV) | `30.0` | `e_IDV` |
| Masculinity (MAS) | `42.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `90.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `52.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `20.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.3754` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1548` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1466` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1029` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0527` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0461` |

| [African](../taxonomy/civilizations/african.md) | `0.0382` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0317` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0221` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0179` |

| [Western](../taxonomy/civilizations/western.md) | `0.0116` |




## Second moment civilisationnel `M(ROU)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1643.28` | Magnitude totale du second moment |
| `I2` (von Mises) | `1066.55` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `2.64e+12` | Déterminant |
| `A` (anisotropie) | `0.989` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1020.49` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `622.79` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[1048.78, 232.84, 207.16, 93.51, 49.79, 11.21]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`ROU.geojson`](../assets/data/states/ROU.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`ROU.profile.json`)](../assets/data/states/ROU.profile.json)

- [Géométrie (`ROU.geojson`)](../assets/data/states/ROU.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

# État `MAR` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `MAR` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.150, -0.950]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `70.0` | `e_PDI` |
| Individualism (IDV) | `46.0` | `e_IDV` |
| Masculinity (MAS) | `53.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `68.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `14.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `25.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.3047` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1238` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1139` |

| [African](../taxonomy/civilizations/african.md) | `0.1084` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0882` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0772` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0499` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0476` |

| [Western](../taxonomy/civilizations/western.md) | `0.0449` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0289` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0124` |




## Second moment civilisationnel `M(MAR)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `2316.97` | Magnitude totale du second moment |
| `I2` (von Mises) | `1472.03` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `1.55e+13` | Déterminant |
| `A` (anisotropie) | `0.989` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `987.32` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `1329.65` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[1442.19, 395.67, 290.74, 126.16, 46.2, 16.02]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`MAR.geojson`](../assets/data/states/MAR.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`MAR.profile.json`)](../assets/data/states/MAR.profile.json)

- [Géométrie (`MAR.geojson`)](../assets/data/states/MAR.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

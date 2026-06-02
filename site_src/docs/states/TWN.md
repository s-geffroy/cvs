# TWN (`TWN`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : _(non répertorié ONU)_ ·
**ISO3** : `TWN` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.850, 0.850]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `58.0` | `e_PDI` |
| Individualism (IDV) | `17.0` | `e_IDV` |
| Masculinity (MAS) | `45.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `69.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `93.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `49.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.1817` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1737` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.1200` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1136` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0754` |

| [African](../taxonomy/civilizations/african.md) | `0.0665` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0642` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0623` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0595` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0498` |

| [Western](../taxonomy/civilizations/western.md) | `0.0334` |




## Second moment civilisationnel `M(TWN)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3306.70` | Magnitude totale du second moment |
| `I2` (von Mises) | `2041.12` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `1.17e+14` | Déterminant |
| `A` (anisotropie) | `0.996` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1492.09` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `1814.61` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[2030.83, 509.69, 348.94, 276.88, 131.45, 8.91]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`TWN.geojson`](../assets/data/states/TWN.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`TWN.profile.json`)](../assets/data/states/TWN.profile.json)

- [Géométrie (`TWN.geojson`)](../assets/data/states/TWN.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

# France (`FRA`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : France ·
**ISO3** : `FRA` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[1.200, 1.450]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `68.0` | `e_PDI` |
| Individualism (IDV) | `71.0` | `e_IDV` |
| Masculinity (MAS) | `43.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `86.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `63.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `48.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Western](../taxonomy/civilizations/western.md) | `0.1507` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.1332` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1068` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0983` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0894` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0885` |

| [African](../taxonomy/civilizations/african.md) | `0.0777` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0773` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0711` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0675` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0395` |




## Second moment civilisationnel `M(FRA)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3400.25` | Magnitude totale du second moment |
| `I2` (von Mises) | `2029.52` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `3.36e+14` | Déterminant |
| `A` (anisotropie) | `0.978` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1654.82` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `1745.44` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[1991.29, 735.99, 307.84, 254.77, 66.02, 44.33]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`FRA.geojson`](../assets/data/states/FRA.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`FRA.profile.json`)](../assets/data/states/FRA.profile.json)

- [Géométrie (`FRA.geojson`)](../assets/data/states/FRA.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

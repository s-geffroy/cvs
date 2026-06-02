# Malaisie (`MYS`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Malaisie ·
**ISO3** : `MYS` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.950, -0.200]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `100.0` | `e_PDI` |
| Individualism (IDV) | `26.0` | `e_IDV` |
| Masculinity (MAS) | `50.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `36.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `41.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `57.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [African](../taxonomy/civilizations/african.md) | `0.2056` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1434` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1305` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1215` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.1048` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0882` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0810` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0624` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0306` |

| [Western](../taxonomy/civilizations/western.md) | `0.0234` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0086` |




## Second moment civilisationnel `M(MYS)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `2531.42` | Magnitude totale du second moment |
| `I2` (von Mises) | `1622.40` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `4.54e+13` | Déterminant |
| `A` (anisotropie) | `0.977` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1022.44` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `1508.98` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[1592.12, 411.59, 311.78, 134.01, 45.48, 36.44]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`MYS.geojson`](../assets/data/states/MYS.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`MYS.profile.json`)](../assets/data/states/MYS.profile.json)

- [Géométrie (`MYS.geojson`)](../assets/data/states/MYS.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

# Mexique (`MEX`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Mexique ·
**ISO3** : `MEX` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.800, 0.700]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `81.0` | `e_PDI` |
| Individualism (IDV) | `30.0` | `e_IDV` |
| Masculinity (MAS) | `69.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `82.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `24.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `97.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.3527` |

| [African](../taxonomy/civilizations/african.md) | `0.1953` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1049` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0922` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0817` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0619` |

| [Western](../taxonomy/civilizations/western.md) | `0.0301` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0236` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0220` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0188` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0166` |




## Second moment civilisationnel `M(MEX)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3184.76` | Magnitude totale du second moment |
| `I2` (von Mises) | `2680.83` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `1.48e+13` | Déterminant |
| `A` (anisotropie) | `0.991` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `895.55` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `2289.21` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[2515.54, 343.71, 134.98, 120.94, 47.61, 21.97]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`MEX.geojson`](../assets/data/states/MEX.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`MEX.profile.json`)](../assets/data/states/MEX.profile.json)

- [Géométrie (`MEX.geojson`)](../assets/data/states/MEX.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

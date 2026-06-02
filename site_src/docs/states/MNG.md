# Mongolie (`MNG`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Mongolie ·
**ISO3** : `MNG` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.200, -0.650]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `93.0` | `e_PDI` |
| Individualism (IDV) | `21.0` | `e_IDV` |
| Masculinity (MAS) | `48.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `92.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `44.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `37.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.2250` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1846` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.1755` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1528` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0938` |

| [African](../taxonomy/civilizations/african.md) | `0.0580` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0360` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0249` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0241` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0155` |

| [Western](../taxonomy/civilizations/western.md) | `0.0098` |




## Second moment civilisationnel `M(MNG)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1558.60` | Magnitude totale du second moment |
| `I2` (von Mises) | `911.07` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `5.36e+12` | Déterminant |
| `A` (anisotropie) | `0.979` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `896.34` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `662.26` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[908.71, 296.97, 174.07, 100.82, 58.78, 19.24]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`MNG.geojson`](../assets/data/states/MNG.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`MNG.profile.json`)](../assets/data/states/MNG.profile.json)

- [Géométrie (`MNG.geojson`)](../assets/data/states/MNG.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

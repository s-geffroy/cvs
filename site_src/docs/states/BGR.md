# Bulgarie (`BGR`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Bulgarie ·
**ISO3** : `BGR` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.250, -0.950]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `70.0` | `e_PDI` |
| Individualism (IDV) | `30.0` | `e_IDV` |
| Masculinity (MAS) | `40.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `85.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `69.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `16.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.4020` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1187` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1072` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0955` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0646` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0596` |

| [African](../taxonomy/civilizations/african.md) | `0.0349` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0345` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0341` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0301` |

| [Western](../taxonomy/civilizations/western.md) | `0.0189` |




## Second moment civilisationnel `M(BGR)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1946.96` | Magnitude totale du second moment |
| `I2` (von Mises) | `1177.49` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `3.07e+13` | Déterminant |
| `A` (anisotropie) | `0.958` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1197.28` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `749.69` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[1173.09, 354.42, 180.83, 119.9, 69.97, 48.74]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`BGR.geojson`](../assets/data/states/BGR.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`BGR.profile.json`)](../assets/data/states/BGR.profile.json)

- [Géométrie (`BGR.geojson`)](../assets/data/states/BGR.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

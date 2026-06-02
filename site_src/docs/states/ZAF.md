# Afrique du Sud (`ZAF`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Afrique du Sud ·
**ISO3** : `ZAF` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.600, 0.000]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `49.0` | `e_PDI` |
| Individualism (IDV) | `65.0` | `e_IDV` |
| Masculinity (MAS) | `63.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `49.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `34.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `63.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.3302` |

| [Western](../taxonomy/civilizations/western.md) | `0.2524` |

| [African](../taxonomy/civilizations/african.md) | `0.1270` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0698` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0511` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0490` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0398` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0271` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0240` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0174` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0124` |




## Second moment civilisationnel `M(ZAF)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1795.90` | Magnitude totale du second moment |
| `I2` (von Mises) | `1176.86` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `5.11e+12` | Déterminant |
| `A` (anisotropie) | `0.990` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1064.43` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `731.47` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[1159.41, 256.05, 176.6, 121.05, 71.52, 11.26]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`ZAF.geojson`](../assets/data/states/ZAF.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`ZAF.profile.json`)](../assets/data/states/ZAF.profile.json)

- [Géométrie (`ZAF.geojson`)](../assets/data/states/ZAF.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

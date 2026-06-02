# Bolivie (`BOL`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Bolivie ·
**ISO3** : `BOL` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.100, 0.050]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0484, 0.0000],
   [0.0000, 0.0484]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `78.0` | `e_PDI` |
| Individualism (IDV) | `10.0` | `e_IDV` |
| Masculinity (MAS) | `42.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `87.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `54.2` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `54.2` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.3843` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1920` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.1073` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0854` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0744` |

| [African](../taxonomy/civilizations/african.md) | `0.0594` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0270` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0269` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0206` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0130` |

| [Western](../taxonomy/civilizations/western.md) | `0.0096` |




## Second moment civilisationnel `M(BOL)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1130.52` | Magnitude totale du second moment |
| `I2` (von Mises) | `632.73` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `4.19e+11` | Déterminant |
| `A` (anisotropie) | `0.990` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `756.44` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `374.09` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[628.15, 250.26, 108.83, 95.19, 41.97, 6.13]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`BOL.geojson`](../assets/data/states/BOL.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`BOL.profile.json`)](../assets/data/states/BOL.profile.json)

- [Géométrie (`BOL.geojson`)](../assets/data/states/BOL.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

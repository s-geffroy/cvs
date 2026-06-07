# Indonésie (`IDN`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Indonésie ·
**ISO3** : `IDN` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = observed` ·
`x_score = observed` · centroïde de repli : `islamic`.



## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.100, -0.300]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `78.0` | `e_PDI` |
| Individualism (IDV) | `14.0` | `e_IDV` |
| Masculinity (MAS) | `46.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `48.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `62.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `38.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.2490` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1540` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1186` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1114` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1051` |

| [African](../taxonomy/civilizations/african.md) | `0.0886` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0555` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0524` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0361` |

| [Western](../taxonomy/civilizations/western.md) | `0.0162` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0131` |




## Second moment civilisationnel `M(IDN)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1574.68` | Magnitude totale du second moment |
| `I2` (von Mises) | `836.40` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `3.69e+12` | Déterminant |
| `A` (anisotropie) | `0.985` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1137.60` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `437.08` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `0.00` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[821.03, 393.47, 182.65, 125.02, 40.04, 12.48]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`IDN.geojson`](../assets/data/states/IDN.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`IDN.profile.json`)](../assets/data/states/IDN.profile.json)

- [Géométrie (`IDN.geojson`)](../assets/data/states/IDN.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

# Pologne (`POL`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Pologne ·
**ISO3** : `POL` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = imputed_wvs_items` ·
`x_score = imputed_governance` · centroïde de repli : `western`.

> ⚠️ `x_viz` n'est **pas une observation directe** : voir [doc 16](../methodology/16_imputation_cascade.md) pour les implications.


> ⚠️ `x_score` n'est **pas une observation directe** : la variance prior est gonflée dans `M(s)` ci-dessous.


## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.476, 0.077]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.1415, 0.0000],
   [0.0000, 0.2934]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `61.2` | `e_PDI` |
| Individualism (IDV) | `48.0` | `e_IDV` |
| Masculinity (MAS) | `50.9` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `85.4` | `e_UAI` |
| Long-Term Orientation (LTO) | `49.9` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `59.7` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.1631` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1248` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1235` |

| [African](../taxonomy/civilizations/african.md) | `0.1215` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1056` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0938` |

| [Western](../taxonomy/civilizations/western.md) | `0.0808` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0692` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0478` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0415` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0285` |




## Second moment civilisationnel `M(POL)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `4189.59` | Magnitude totale du second moment |
| `I2` (von Mises) | `1034.09` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `4.81e+16` | Déterminant |
| `A` (anisotropie) | `0.825` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1307.69` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `699.08` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[1266.23, 905.33, 825.78, 567.46, 402.63, 222.16]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`POL.geojson`](../assets/data/states/POL.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`POL.profile.json`)](../assets/data/states/POL.profile.json)

- [Géométrie (`POL.geojson`)](../assets/data/states/POL.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

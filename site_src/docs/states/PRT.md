# Portugal (`PRT`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Portugal ·
**ISO3** : `PRT` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = imputed_pew` ·
`x_score = imputed_governance` · centroïde de repli : `western`.

> ⚠️ `x_viz` n'est **pas une observation directe** : voir [doc 16](../methodology/16_imputation_cascade.md) pour les implications.


> ⚠️ `x_score` n'est **pas une observation directe** : la variance prior est gonflée dans `M(s)` ci-dessous.


## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.095, 0.706]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.2329, 0.0000],
   [0.0000, 0.4197]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `62.7` | `e_PDI` |
| Individualism (IDV) | `47.4` | `e_IDV` |
| Masculinity (MAS) | `48.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `83.8` | `e_UAI` |
| Long-Term Orientation (LTO) | `49.6` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `49.4` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1439` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.1235` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1218` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1085` |

| [African](../taxonomy/civilizations/african.md) | `0.1058` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1025` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0927` |

| [Western](../taxonomy/civilizations/western.md) | `0.0713` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0606` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0367` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0327` |




## Second moment civilisationnel `M(PRT)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `4044.83` | Magnitude totale du second moment |
| `I2` (von Mises) | `897.61` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `4.37e+16` | Déterminant |
| `A` (anisotropie) | `0.799` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1294.35` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `567.66` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[1111.06, 898.19, 793.87, 618.65, 399.97, 223.08]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`PRT.geojson`](../assets/data/states/PRT.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`PRT.profile.json`)](../assets/data/states/PRT.profile.json)

- [Géométrie (`PRT.geojson`)](../assets/data/states/PRT.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

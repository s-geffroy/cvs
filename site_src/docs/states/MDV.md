# Maldives (`MDV`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Maldives ·
**ISO3** : `MDV` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = imputed_pew` ·
`x_score = imputed_governance` · centroïde de repli : `islamic`.

> ⚠️ `x_viz` n'est **pas une observation directe** : voir [doc 16](../methodology/16_imputation_cascade.md) pour les implications.


> ⚠️ `x_score` n'est **pas une observation directe** : la variance prior est gonflée dans `M(s)` ci-dessous.


## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.260, -0.769]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.2329, 0.0000],
   [0.0000, 0.4197]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `83.6` | `e_PDI` |
| Individualism (IDV) | `28.6` | `e_IDV` |
| Masculinity (MAS) | `46.8` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `60.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `42.6` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `21.1` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.2845` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1707` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1448` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0808` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0733` |

| [African](../taxonomy/civilizations/african.md) | `0.0702` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0693` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0419` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0374` |

| [Western](../taxonomy/civilizations/western.md) | `0.0164` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0107` |




## Second moment civilisationnel `M(MDV)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3587.87` | Magnitude totale du second moment |
| `I2` (von Mises) | `905.47` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `1.98e+16` | Déterminant |
| `A` (anisotropie) | `0.795` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `945.65` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `459.40` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[1108.63, 768.8, 731.23, 413.33, 338.99, 226.89]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`MDV.geojson`](../assets/data/states/MDV.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`MDV.profile.json`)](../assets/data/states/MDV.profile.json)

- [Géométrie (`MDV.geojson`)](../assets/data/states/MDV.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

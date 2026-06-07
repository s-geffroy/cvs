# Géorgie (`GEO`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Géorgie ·
**ISO3** : `GEO` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

**Provenance des coordonnées** (cascade [doc 16](../methodology/16_imputation_cascade.md)) :
`x_viz = imputed_wvs_items` ·
`x_score = imputed_governance` · centroïde de repli : `orthodox`.

> ⚠️ `x_viz` n'est **pas une observation directe** : voir [doc 16](../methodology/16_imputation_cascade.md) pour les implications.


> ⚠️ `x_score` n'est **pas une observation directe** : la variance prior est gonflée dans `M(s)` ci-dessous.


## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.252, -0.997]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.1415, 0.0000],
   [0.0000, 0.2934]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `64.3` | `e_PDI` |
| Individualism (IDV) | `43.4` | `e_IDV` |
| Masculinity (MAS) | `51.6` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `65.9` | `e_UAI` |
| Long-Term Orientation (LTO) | `47.9` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `44.6` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1471` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1400` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1371` |

| [African](../taxonomy/civilizations/african.md) | `0.1360` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1038` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0764` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0721` |

| [Western](../taxonomy/civilizations/western.md) | `0.0611` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0527` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0511` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0226` |




## Second moment civilisationnel `M(GEO)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `3516.23` | Magnitude totale du second moment |
| `I2` (von Mises) | `678.92` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `2.28e+16` | Déterminant |
| `A` (anisotropie) | `0.728` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais + inflation prior

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1173.58` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `159.84` | Écart de l'État à son barycentre d'affinité |
| Inflation prior `diag(σ_prior²)` | `2182.82` | Variance d'imputation propagée (≠ 0 si `x_score` non observé) |

### Valeurs propres (descendantes)

`[843.2, 830.64, 665.8, 579.55, 367.79, 229.26]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`GEO.geojson`](../assets/data/states/GEO.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`GEO.profile.json`)](../assets/data/states/GEO.profile.json)

- [Géométrie (`GEO.geojson`)](../assets/data/states/GEO.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

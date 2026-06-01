# État `UKR` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `UKR` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.200, -0.850]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `92.0` | `e_PDI` |
| Individualism (IDV) | `25.0` | `e_IDV` |
| Masculinity (MAS) | `27.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `95.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `86.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `18.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.5452` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1001` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0948` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0623` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0495` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0406` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0282` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0281` |

| [African](../taxonomy/civilizations/african.md) | `0.0237` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0166` |

| [Western](../taxonomy/civilizations/western.md) | `0.0109` |




## Second moment civilisationnel `M(UKR)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `2666.73` | Magnitude totale du second moment |
| `I2` (von Mises) | `2238.26` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `3.16e+12` | Déterminant |
| `A` (anisotropie) | `0.996` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `1011.20` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `1655.53` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[2104.79, 231.19, 160.49, 116.46, 46.3, 7.5]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`UKR.geojson`](../assets/data/states/UKR.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`UKR.profile.json`)](../assets/data/states/UKR.profile.json)

- [Géométrie (`UKR.geojson`)](../assets/data/states/UKR.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

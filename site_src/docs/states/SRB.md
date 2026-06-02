# Serbie (`SRB`) — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**Nom (FR)** : Serbie ·
**ISO3** : `SRB` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.150, -0.650]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `86.0` | `e_PDI` |
| Individualism (IDV) | `25.0` | `e_IDV` |
| Masculinity (MAS) | `43.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `92.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `52.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `28.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.3253` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1798` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1383` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1362` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0587` |

| [African](../taxonomy/civilizations/african.md) | `0.0418` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0399` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0286` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0227` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0178` |

| [Western](../taxonomy/civilizations/western.md) | `0.0109` |




## Second moment civilisationnel `M(SRB)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1421.31` | Magnitude totale du second moment |
| `I2` (von Mises) | `885.04` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `1.21e+12` | Déterminant |
| `A` (anisotropie) | `0.991` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `989.43` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `431.88` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[875.84, 236.04, 155.66, 96.92, 48.92, 7.94]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`SRB.geojson`](../assets/data/states/SRB.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`SRB.profile.json`)](../assets/data/states/SRB.profile.json)

- [Géométrie (`SRB.geojson`)](../assets/data/states/SRB.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

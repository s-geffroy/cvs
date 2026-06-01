# État `ZMB` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `ZMB` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.200, -0.300]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0625, 0.0000],
   [0.0000, 0.0625]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `75.0` | `e_PDI` |
| Individualism (IDV) | `30.0` | `e_IDV` |
| Masculinity (MAS) | `60.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `55.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `55.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `55.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [African](../taxonomy/civilizations/african.md) | `0.2053` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1380` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1099` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1047` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1032` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0941` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0918` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0663` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0358` |

| [Western](../taxonomy/civilizations/western.md) | `0.0297` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0213` |




## Tenseur de tension civilisationnelle `T(ZMB)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `1348.22` | Tension totale |
| `I2` (déviatorique) | `149287.68` | Asymétrie |
| `det(T)` | `1.33e+13` | Rigidité |
| `A` (anisotropie) | `0.942` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[474.12, 351.54, 276.11, 147.47, 71.71, 27.27]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`ZMB.geojson`](../assets/data/states/ZMB.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`ZMB.profile.json`)](../assets/data/states/ZMB.profile.json)

- [Géométrie (`ZMB.geojson`)](../assets/data/states/ZMB.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

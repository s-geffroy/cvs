# État `GTM` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `GTM` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.250, 0.300]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0484, 0.0000],
   [0.0000, 0.0484]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `95.0` | `e_PDI` |
| Individualism (IDV) | `6.0` | `e_IDV` |
| Masculinity (MAS) | `37.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `101.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `59.8` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `59.8` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.3249` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1733` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.1539` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.1266` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0701` |

| [African](../taxonomy/civilizations/african.md) | `0.0545` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0267` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0225` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0204` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0179` |

| [Western](../taxonomy/civilizations/western.md) | `0.0091` |




## Tenseur de tension civilisationnelle `T(GTM)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `2473.09` | Tension totale |
| `I2` (déviatorique) | `2498029.92` | Asymétrie |
| `det(T)` | `6.51e+12` | Rigidité |
| `A` (anisotropie) | `0.990` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[1835.58, 345.07, 118.65, 112.58, 43.53, 17.68]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`GTM.geojson`](../assets/data/states/GTM.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`GTM.profile.json`)](../assets/data/states/GTM.profile.json)

- [Géométrie (`GTM.geojson`)](../assets/data/states/GTM.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

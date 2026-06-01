# État `JOR` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `JOR` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.300, -1.050]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `70.0` | `e_PDI` |
| Individualism (IDV) | `30.0` | `e_IDV` |
| Masculinity (MAS) | `45.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `65.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `16.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `43.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.2526` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1641` |

| [African](../taxonomy/civilizations/african.md) | `0.1546` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.1196` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0879` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0687` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0588` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0317` |

| [Western](../taxonomy/civilizations/western.md) | `0.0292` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0259` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0068` |




## Tenseur de tension civilisationnelle `T(JOR)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `1514.06` | Tension totale |
| `I2` (déviatorique) | `389476.64` | Asymétrie |
| `det(T)` | `3.19e+12` | Rigidité |
| `A` (anisotropie) | `0.981` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[751.75, 346.83, 276.98, 89.28, 35.15, 14.07]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`JOR.geojson`](../assets/data/states/JOR.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`JOR.profile.json`)](../assets/data/states/JOR.profile.json)

- [Géométrie (`JOR.geojson`)](../assets/data/states/JOR.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

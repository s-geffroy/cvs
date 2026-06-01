# État `PER` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `PER` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.850, 0.400]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `64.0` | `e_PDI` |
| Individualism (IDV) | `16.0` | `e_IDV` |
| Masculinity (MAS) | `42.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `87.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `25.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `46.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.2103` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.2046` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1657` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1426` |

| [African](../taxonomy/civilizations/african.md) | `0.0932` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0572` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0507` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0274` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0200` |

| [Western](../taxonomy/civilizations/western.md) | `0.0184` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0100` |




## Tenseur de tension civilisationnelle `T(PER)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `1602.53` | Tension totale |
| `I2` (déviatorique) | `539437.27` | Asymétrie |
| `det(T)` | `9.45e+12` | Rigidité |
| `A` (anisotropie) | `0.964` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[902.83, 307.16, 211.77, 97.89, 50.01, 32.88]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`PER.geojson`](../assets/data/states/PER.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`PER.profile.json`)](../assets/data/states/PER.profile.json)

- [Géométrie (`PER.geojson`)](../assets/data/states/PER.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

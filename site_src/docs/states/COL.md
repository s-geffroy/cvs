# État `COL` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `COL` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.900, 1.100]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `67.0` | `e_PDI` |
| Individualism (IDV) | `13.0` | `e_IDV` |
| Masculinity (MAS) | `64.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `80.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `13.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `83.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.3846` |

| [African](../taxonomy/civilizations/african.md) | `0.1782` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1055` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0997` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0741` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0722` |

| [Western](../taxonomy/civilizations/western.md) | `0.0210` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0193` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0185` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0153` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0113` |




## Tenseur de tension civilisationnelle `T(COL)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `2471.07` | Tension totale |
| `I2` (déviatorique) | `2796828.79` | Asymétrie |
| `det(T)` | `2.58e+12` | Rigidité |
| `A` (anisotropie) | `0.994` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[1924.73, 296.04, 122.1, 74.02, 42.34, 11.85]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`COL.geojson`](../assets/data/states/COL.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`COL.profile.json`)](../assets/data/states/COL.profile.json)

- [Géométrie (`COL.geojson`)](../assets/data/states/COL.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

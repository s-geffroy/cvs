# État `TWN` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `TWN` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.850, 0.850]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `58.0` | `e_PDI` |
| Individualism (IDV) | `17.0` | `e_IDV` |
| Masculinity (MAS) | `45.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `69.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `93.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `49.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.1817` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1737` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.1200` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1136` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0754` |

| [African](../taxonomy/civilizations/african.md) | `0.0665` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0642` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0623` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0595` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0498` |

| [Western](../taxonomy/civilizations/western.md) | `0.0334` |




## Tenseur de tension civilisationnelle `T(TWN)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `3306.70` | Tension totale |
| `I2` (déviatorique) | `2777443.41` | Asymétrie |
| `det(T)` | `1.17e+14` | Rigidité |
| `A` (anisotropie) | `0.996` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[2030.83, 509.69, 348.94, 276.88, 131.45, 8.91]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`TWN.geojson`](../assets/data/states/TWN.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`TWN.profile.json`)](../assets/data/states/TWN.profile.json)

- [Géométrie (`TWN.geojson`)](../assets/data/states/TWN.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

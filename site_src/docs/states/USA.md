# État `USA` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `USA` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.100, 1.550]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `40.0` | `e_PDI` |
| Individualism (IDV) | `91.0` | `e_IDV` |
| Masculinity (MAS) | `62.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `46.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `26.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `68.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Western](../taxonomy/civilizations/western.md) | `0.4725` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.2207` |

| [African](../taxonomy/civilizations/african.md) | `0.0809` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0599` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0388` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0371` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0270` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0193` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0177` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0157` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0103` |




## Tenseur de tension civilisationnelle `T(USA)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `3231.62` | Tension totale |
| `I2` (déviatorique) | `5230409.31` | Asymétrie |
| `det(T)` | `6.63e+12` | Rigidité |
| `A` (anisotropie) | `0.997` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[2617.84, 280.89, 151.1, 109.57, 63.66, 8.56]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`USA.geojson`](../assets/data/states/USA.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`USA.profile.json`)](../assets/data/states/USA.profile.json)

- [Géométrie (`USA.geojson`)](../assets/data/states/USA.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

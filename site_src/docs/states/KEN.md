# État `KEN` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `KEN` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.550, -0.650]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0484, 0.0000],
   [0.0000, 0.0484]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `70.0` | `e_PDI` |
| Individualism (IDV) | `25.0` | `e_IDV` |
| Masculinity (MAS) | `60.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `50.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `51.2` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `51.2` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [African](../taxonomy/civilizations/african.md) | `0.2093` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1306` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1122` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1118` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.1091` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0987` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0963` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0579` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0292` |

| [Western](../taxonomy/civilizations/western.md) | `0.0278` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0171` |




## Tenseur de tension civilisationnelle `T(KEN)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `1303.19` | Tension totale |
| `I2` (déviatorique) | `168850.06` | Asymétrie |
| `det(T)` | `5.07e+12` | Rigidité |
| `A` (anisotropie) | `0.972` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[497.64, 346.36, 251.53, 129.06, 64.57, 14.04]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`KEN.geojson`](../assets/data/states/KEN.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`KEN.profile.json`)](../assets/data/states/KEN.profile.json)

- [Géométrie (`KEN.geojson`)](../assets/data/states/KEN.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

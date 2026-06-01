# État `CHL` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `CHL` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.200, 0.850]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `63.0` | `e_PDI` |
| Individualism (IDV) | `23.0` | `e_IDV` |
| Masculinity (MAS) | `28.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `86.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `31.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `68.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.3098` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1588` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1377` |

| [African](../taxonomy/civilizations/african.md) | `0.1080` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0868` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0716` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0458` |

| [Western](../taxonomy/civilizations/western.md) | `0.0316` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0221` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0189` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0088` |




## Tenseur de tension civilisationnelle `T(CHL)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `1914.80` | Tension totale |
| `I2` (déviatorique) | `1004624.76` | Asymétrie |
| `det(T)` | `4.78e+12` | Rigidité |
| `A` (anisotropie) | `0.993` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[1201.82, 347.8, 190.61, 93.31, 72.37, 8.88]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`CHL.geojson`](../assets/data/states/CHL.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`CHL.profile.json`)](../assets/data/states/CHL.profile.json)

- [Géométrie (`CHL.geojson`)](../assets/data/states/CHL.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

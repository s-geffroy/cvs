# État `RUS` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `RUS` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.050, -1.050]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `93.0` | `e_PDI` |
| Individualism (IDV) | `39.0` | `e_IDV` |
| Masculinity (MAS) | `36.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `95.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `81.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `20.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.5527` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0880` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0818` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0659` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0486` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0410` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0355` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0288` |

| [African](../taxonomy/civilizations/african.md) | `0.0255` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0187` |

| [Western](../taxonomy/civilizations/western.md) | `0.0137` |




## Tenseur de tension civilisationnelle `T(RUS)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `2286.43` | Tension totale |
| `I2` (déviatorique) | `2098858.12` | Asymétrie |
| `det(T)` | `9.83e+12` | Rigidité |
| `A` (anisotropie) | `0.983` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[1692.73, 255.62, 167.31, 87.37, 55.3, 28.11]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`RUS.geojson`](../assets/data/states/RUS.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`RUS.profile.json`)](../assets/data/states/RUS.profile.json)

- [Géométrie (`RUS.geojson`)](../assets/data/states/RUS.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

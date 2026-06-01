# État `MMR` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `MMR` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.500, -0.050]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0484, 0.0000],
   [0.0000, 0.0484]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `80.0` | `e_PDI` |
| Individualism (IDV) | `20.0` | `e_IDV` |
| Masculinity (MAS) | `50.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `60.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `52.5` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `52.5` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.2217` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1732` |

| [African](../taxonomy/civilizations/african.md) | `0.1465` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1161` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0740` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0724` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0613` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0601` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0455` |

| [Western](../taxonomy/civilizations/western.md) | `0.0169` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0124` |




## Tenseur de tension civilisationnelle `T(MMR)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `1126.28` | Tension totale |
| `I2` (déviatorique) | `115092.43` | Asymétrie |
| `det(T)` | `3.37e+12` | Rigidité |
| `A` (anisotropie) | `0.930` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[376.16, 340.2, 234.04, 111.0, 38.69, 26.19]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`MMR.geojson`](../assets/data/states/MMR.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`MMR.profile.json`)](../assets/data/states/MMR.profile.json)

- [Géométrie (`MMR.geojson`)](../assets/data/states/MMR.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

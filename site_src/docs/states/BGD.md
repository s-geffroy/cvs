# État `BGD` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `BGD` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.050, -0.650]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `80.0` | `e_PDI` |
| Individualism (IDV) | `20.0` | `e_IDV` |
| Masculinity (MAS) | `55.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `60.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `47.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `20.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.2545` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1699` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1304` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0933` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0920` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0806` |

| [African](../taxonomy/civilizations/african.md) | `0.0724` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0403` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0376` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0151` |

| [Western](../taxonomy/civilizations/western.md) | `0.0138` |




## Tenseur de tension civilisationnelle `T(BGD)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `1546.76` | Tension totale |
| `I2` (déviatorique) | `357257.73` | Asymétrie |
| `det(T)` | `9.76e+12` | Rigidité |
| `A` (anisotropie) | `0.974` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[734.44, 390.88, 202.03, 136.2, 63.85, 19.36]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`BGD.geojson`](../assets/data/states/BGD.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`BGD.profile.json`)](../assets/data/states/BGD.profile.json)

- [Géométrie (`BGD.geojson`)](../assets/data/states/BGD.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

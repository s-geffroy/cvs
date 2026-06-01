# État `ARG` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `ARG` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.600, 0.650]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `49.0` | `e_PDI` |
| Individualism (IDV) | `46.0` | `e_IDV` |
| Masculinity (MAS) | `56.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `86.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `20.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `62.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.2485` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1516` |

| [African](../taxonomy/civilizations/african.md) | `0.1436` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1026` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0943` |

| [Western](../taxonomy/civilizations/western.md) | `0.0882` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0664` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0352` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0313` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0219` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0163` |




## Tenseur de tension civilisationnelle `T(ARG)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `2438.90` | Tension totale |
| `I2` (déviatorique) | `1602390.23` | Asymétrie |
| `det(T)` | `2.09e+13` | Rigidité |
| `A` (anisotropie) | `0.989` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[1499.44, 534.83, 199.4, 121.71, 67.68, 15.83]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`ARG.geojson`](../assets/data/states/ARG.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`ARG.profile.json`)](../assets/data/states/ARG.profile.json)

- [Géométrie (`ARG.geojson`)](../assets/data/states/ARG.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

# État `CHN` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `CHN` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.750, -0.950]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `80.0` | `e_PDI` |
| Individualism (IDV) | `20.0` | `e_IDV` |
| Masculinity (MAS) | `66.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `30.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `87.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `24.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.4950` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1541` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0562` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0552` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0505` |

| [African](../taxonomy/civilizations/african.md) | `0.0474` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0410` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0384` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0313` |

| [Western](../taxonomy/civilizations/western.md) | `0.0160` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0148` |




## Tenseur de tension civilisationnelle `T(CHN)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `2579.19` | Tension totale |
| `I2` (déviatorique) | `2644721.99` | Asymétrie |
| `det(T)` | `9.34e+12` | Rigidité |
| `A` (anisotropie) | `0.995` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[1902.65, 273.96, 184.89, 138.92, 68.6, 10.17]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`CHN.geojson`](../assets/data/states/CHN.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`CHN.profile.json`)](../assets/data/states/CHN.profile.json)

- [Géométrie (`CHN.geojson`)](../assets/data/states/CHN.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

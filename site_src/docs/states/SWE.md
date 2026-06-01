# État `SWE` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `SWE` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[1.780, 2.350]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `31.0` | `e_PDI` |
| Individualism (IDV) | `71.0` | `e_IDV` |
| Masculinity (MAS) | `5.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `29.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `53.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `78.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Western](../taxonomy/civilizations/western.md) | `0.4331` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.2180` |

| [African](../taxonomy/civilizations/african.md) | `0.0735` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0582` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0505` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0403` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0381` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0347` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0265` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0174` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0098` |




## Tenseur de tension civilisationnelle `T(SWE)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `5156.10` | Tension totale |
| `I2` (déviatorique) | `14943858.17` | Asymétrie |
| `det(T)` | `1.96e+13` | Rigidité |
| `A` (anisotropie) | `0.998` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[4376.82, 404.21, 198.29, 109.49, 58.59, 8.7]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`SWE.geojson`](../assets/data/states/SWE.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`SWE.profile.json`)](../assets/data/states/SWE.profile.json)

- [Géométrie (`SWE.geojson`)](../assets/data/states/SWE.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

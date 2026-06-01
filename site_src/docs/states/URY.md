# État `URY` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `URY` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.050, 1.100]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `61.0` | `e_PDI` |
| Individualism (IDV) | `36.0` | `e_IDV` |
| Masculinity (MAS) | `38.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `99.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `26.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `53.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.2787` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1519` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1261` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1095` |

| [African](../taxonomy/civilizations/african.md) | `0.0901` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0742` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0691` |

| [Western](../taxonomy/civilizations/western.md) | `0.0405` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0284` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0160` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0156` |




## Tenseur de tension civilisationnelle `T(URY)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `2255.91` | Tension totale |
| `I2` (déviatorique) | `1355811.74` | Asymétrie |
| `det(T)` | `1.24e+13` | Rigidité |
| `A` (anisotropie) | `0.990` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[1398.25, 386.32, 285.01, 127.21, 45.07, 14.04]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`URY.geojson`](../assets/data/states/URY.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`URY.profile.json`)](../assets/data/states/URY.profile.json)

- [Géométrie (`URY.geojson`)](../assets/data/states/URY.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

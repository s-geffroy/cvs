# État `VNM` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `VNM` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.050, -0.200]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `70.0` | `e_PDI` |
| Individualism (IDV) | `20.0` | `e_IDV` |
| Masculinity (MAS) | `40.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `30.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `57.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `35.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.3428` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1578` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0942` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0923` |

| [African](../taxonomy/civilizations/african.md) | `0.0867` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0770` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0576` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0311` |

| [Western](../taxonomy/civilizations/western.md) | `0.0261` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0256` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0088` |




## Tenseur de tension civilisationnelle `T(VNM)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `1832.14` | Tension totale |
| `I2` (déviatorique) | `782952.04` | Asymétrie |
| `det(T)` | `7.84e+12` | Rigidité |
| `A` (anisotropie) | `0.989` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[1084.58, 286.9, 239.49, 151.54, 57.57, 12.06]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`VNM.geojson`](../assets/data/states/VNM.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`VNM.profile.json`)](../assets/data/states/VNM.profile.json)

- [Géométrie (`VNM.geojson`)](../assets/data/states/VNM.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

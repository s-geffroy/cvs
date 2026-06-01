# État `ESP` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `ESP` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.650, 0.950]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `57.0` | `e_PDI` |
| Individualism (IDV) | `51.0` | `e_IDV` |
| Masculinity (MAS) | `42.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `86.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `48.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `44.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1337` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1268` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1138` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.1101` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.1086` |

| [Western](../taxonomy/civilizations/western.md) | `0.0967` |

| [African](../taxonomy/civilizations/african.md) | `0.0896` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0881` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0644` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0359` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0325` |




## Tenseur de tension civilisationnelle `T(ESP)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `2246.28` | Tension totale |
| `I2` (déviatorique) | `810275.84` | Asymétrie |
| `det(T)` | `3.27e+13` | Rigidité |
| `A` (anisotropie) | `0.987` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[1072.38, 606.51, 314.45, 173.13, 65.75, 14.06]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`ESP.geojson`](../assets/data/states/ESP.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`ESP.profile.json`)](../assets/data/states/ESP.profile.json)

- [Géométrie (`ESP.geojson`)](../assets/data/states/ESP.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

# État `AUS` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `AUS` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.500, 1.650]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `38.0` | `e_PDI` |
| Individualism (IDV) | `90.0` | `e_IDV` |
| Masculinity (MAS) | `61.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `51.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `21.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `71.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Western](../taxonomy/civilizations/western.md) | `0.4595` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.2242` |

| [African](../taxonomy/civilizations/african.md) | `0.0859` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0528` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0473` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0391` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0289` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0175` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0172` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0169` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0107` |




## Tenseur de tension civilisationnelle `T(AUS)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `3465.04` | Tension totale |
| `I2` (déviatorique) | `6122759.48` | Asymétrie |
| `det(T)` | `7.17e+12` | Rigidité |
| `A` (anisotropie) | `0.997` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[2825.53, 327.6, 128.54, 109.72, 65.23, 8.42]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`AUS.geojson`](../assets/data/states/AUS.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`AUS.profile.json`)](../assets/data/states/AUS.profile.json)

- [Géométrie (`AUS.geojson`)](../assets/data/states/AUS.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

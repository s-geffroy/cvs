# État `FJI` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `FJI` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.800, 0.400]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0900, 0.0000],
   [0.0000, 0.0900]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `78.0` | `e_PDI` |
| Individualism (IDV) | `14.0` | `e_IDV` |
| Masculinity (MAS) | `46.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `48.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `46.5` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `46.5` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1951` |

| [African](../taxonomy/civilizations/african.md) | `0.1516` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1410` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1225` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.1170` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0845` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0688` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0570` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0364` |

| [Western](../taxonomy/civilizations/western.md) | `0.0175` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0086` |




## Tenseur de tension civilisationnelle `T(FJI)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `1422.11` | Tension totale |
| `I2` (déviatorique) | `254946.48` | Asymétrie |
| `det(T)` | `3.89e+12` | Rigidité |
| `A` (anisotropie) | `0.978` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[604.48, 370.91, 265.56, 130.05, 37.86, 13.25]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`FJI.geojson`](../assets/data/states/FJI.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`FJI.profile.json`)](../assets/data/states/FJI.profile.json)

- [Géométrie (`FJI.geojson`)](../assets/data/states/FJI.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

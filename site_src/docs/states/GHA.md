# État `GHA` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `GHA` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.450, 0.200]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0484, 0.0000],
   [0.0000, 0.0484]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `80.0` | `e_PDI` |
| Individualism (IDV) | `15.0` | `e_IDV` |
| Masculinity (MAS) | `40.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `65.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `4.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `72.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.2601` |

| [African](../taxonomy/civilizations/african.md) | `0.1981` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1461` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1177` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0976` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0780` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0310` |

| [Western](../taxonomy/civilizations/western.md) | `0.0229` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0225` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0210` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0051` |




## Tenseur de tension civilisationnelle `T(GHA)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `2731.77` | Tension totale |
| `I2` (déviatorique) | `3204824.13` | Asymétrie |
| `det(T)` | `3.58e+12` | Rigidité |
| `A` (anisotropie) | `0.996` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[2071.45, 322.73, 214.3, 79.22, 35.05, 9.01]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`GHA.geojson`](../assets/data/states/GHA.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`GHA.profile.json`)](../assets/data/states/GHA.profile.json)

- [Géométrie (`GHA.geojson`)](../assets/data/states/GHA.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

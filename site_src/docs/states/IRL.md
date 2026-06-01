# État `IRL` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `IRL` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.100, 1.100]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `28.0` | `e_PDI` |
| Individualism (IDV) | `70.0` | `e_IDV` |
| Masculinity (MAS) | `68.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `35.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `24.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `65.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Western](../taxonomy/civilizations/western.md) | `0.3360` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.3077` |

| [African](../taxonomy/civilizations/african.md) | `0.1048` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0650` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0428` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0404` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0302` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0286` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0184` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0173` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0088` |




## Tenseur de tension civilisationnelle `T(IRL)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `3313.82` | Tension totale |
| `I2` (déviatorique) | `5218307.18` | Asymétrie |
| `det(T)` | `1.24e+13` | Rigidité |
| `A` (anisotropie) | `0.995` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[2624.25, 341.91, 179.08, 96.22, 58.62, 13.73]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`IRL.geojson`](../assets/data/states/IRL.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`IRL.profile.json`)](../assets/data/states/IRL.profile.json)

- [Géométrie (`IRL.geojson`)](../assets/data/states/IRL.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

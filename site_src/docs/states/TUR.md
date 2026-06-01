# État `TUR` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `TUR` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-0.850, -0.650]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `66.0` | `e_PDI` |
| Individualism (IDV) | `37.0` | `e_IDV` |
| Masculinity (MAS) | `45.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `85.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `46.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `49.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1881` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.1451` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1335` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1333` |

| [African](../taxonomy/civilizations/african.md) | `0.0990` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0924` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0755` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0444` |

| [Western](../taxonomy/civilizations/western.md) | `0.0380` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0281` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0226` |




## Tenseur de tension civilisationnelle `T(TUR)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `1439.98` | Tension totale |
| `I2` (déviatorique) | `212408.08` | Asymétrie |
| `det(T)` | `5.42e+12` | Rigidité |
| `A` (anisotropie) | `0.979` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[524.32, 409.15, 309.23, 129.21, 56.96, 11.11]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`TUR.geojson`](../assets/data/states/TUR.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`TUR.profile.json`)](../assets/data/states/TUR.profile.json)

- [Géométrie (`TUR.geojson`)](../assets/data/states/TUR.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

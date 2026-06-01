# État `NZL` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `NZL` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.650, 1.850]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `22.0` | `e_PDI` |
| Individualism (IDV) | `79.0` | `e_IDV` |
| Masculinity (MAS) | `58.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `49.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `33.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `75.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Western](../taxonomy/civilizations/western.md) | `0.5031` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.2349` |

| [African](../taxonomy/civilizations/african.md) | `0.0708` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0388` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0382` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0285` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0239` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0186` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0183` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0161` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0088` |




## Tenseur de tension civilisationnelle `T(NZL)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `2888.53` | Tension totale |
| `I2` (déviatorique) | `4365734.14` | Asymétrie |
| `det(T)` | `1.83e+12` | Rigidité |
| `A` (anisotropie) | `0.996` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[2380.49, 257.29, 114.71, 95.86, 31.57, 8.62]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`NZL.geojson`](../assets/data/states/NZL.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`NZL.profile.json`)](../assets/data/states/NZL.profile.json)

- [Géométrie (`NZL.geojson`)](../assets/data/states/NZL.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

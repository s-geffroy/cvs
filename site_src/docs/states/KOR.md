# État `KOR` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `KOR` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[1.650, 0.550]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `60.0` | `e_PDI` |
| Individualism (IDV) | `18.0` | `e_IDV` |
| Masculinity (MAS) | `39.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `85.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `100.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `29.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.2771` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1450` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.1231` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1032` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0941` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0640` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0538` |

| [African](../taxonomy/civilizations/african.md) | `0.0392` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0382` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0377` |

| [Western](../taxonomy/civilizations/western.md) | `0.0247` |




## Tenseur de tension civilisationnelle `T(KOR)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `3965.59` | Tension totale |
| `I2` (déviatorique) | `5347852.30` | Asymétrie |
| `det(T)` | `1.87e+14` | Rigidité |
| `A` (anisotropie) | `0.995` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[2742.74, 493.54, 374.76, 214.38, 126.6, 13.57]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`KOR.geojson`](../assets/data/states/KOR.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`KOR.profile.json`)](../assets/data/states/KOR.profile.json)

- [Géométrie (`KOR.geojson`)](../assets/data/states/KOR.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

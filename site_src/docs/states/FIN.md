# État `FIN` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `FIN` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.900, 1.500]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `33.0` | `e_PDI` |
| Individualism (IDV) | `63.0` | `e_IDV` |
| Masculinity (MAS) | `26.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `59.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `38.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `57.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Western](../taxonomy/civilizations/western.md) | `0.4314` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.2191` |

| [African](../taxonomy/civilizations/african.md) | `0.0702` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0497` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0493` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0476` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0468` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0275` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0263` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0211` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0112` |




## Tenseur de tension civilisationnelle `T(FIN)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `2244.02` | Tension totale |
| `I2` (déviatorique) | `1784984.35` | Asymétrie |
| `det(T)` | `6.58e+12` | Rigidité |
| `A` (anisotropie) | `0.991` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[1570.45, 344.88, 156.85, 108.89, 48.17, 14.78]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`FIN.geojson`](../assets/data/states/FIN.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`FIN.profile.json`)](../assets/data/states/FIN.profile.json)

- [Géométrie (`FIN.geojson`)](../assets/data/states/FIN.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

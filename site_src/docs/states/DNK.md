# État `DNK` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `DNK` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[1.500, 2.200]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `18.0` | `e_PDI` |
| Individualism (IDV) | `74.0` | `e_IDV` |
| Masculinity (MAS) | `16.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `23.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `35.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `70.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Western](../taxonomy/civilizations/western.md) | `0.4748` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.2324` |

| [African](../taxonomy/civilizations/african.md) | `0.0676` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0550` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0371` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0334` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0317` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0307` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0180` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0112` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0081` |




## Tenseur de tension civilisationnelle `T(DNK)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `4811.90` | Tension totale |
| `I2` (déviatorique) | `14036104.40` | Asymétrie |
| `det(T)` | `5.62e+12` | Rigidité |
| `A` (anisotropie) | `0.998` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[4215.12, 304.71, 167.45, 68.7, 48.0, 7.92]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`DNK.geojson`](../assets/data/states/DNK.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`DNK.profile.json`)](../assets/data/states/DNK.profile.json)

- [Géométrie (`DNK.geojson`)](../assets/data/states/DNK.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

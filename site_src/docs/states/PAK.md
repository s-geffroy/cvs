# État `PAK` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `PAK` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[-1.300, -0.950]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0400, 0.0000],
   [0.0000, 0.0400]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `55.0` | `e_PDI` |
| Individualism (IDV) | `14.0` | `e_IDV` |
| Masculinity (MAS) | `50.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `70.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `50.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `0.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.2099` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.1423` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.1401` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1096` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.1043` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0941` |

| [African](../taxonomy/civilizations/african.md) | `0.0555` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0491` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0407` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0313` |

| [Western](../taxonomy/civilizations/western.md) | `0.0229` |




## Tenseur de tension civilisationnelle `T(PAK)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `3387.58` | Tension totale |
| `I2` (déviatorique) | `3676879.94` | Asymétrie |
| `det(T)` | `4.33e+14` | Rigidité |
| `A` (anisotropie) | `0.973` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[2294.86, 444.3, 262.85, 177.73, 145.36, 62.48]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`PAK.geojson`](../assets/data/states/PAK.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`PAK.profile.json`)](../assets/data/states/PAK.profile.json)

- [Géométrie (`PAK.geojson`)](../assets/data/states/PAK.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

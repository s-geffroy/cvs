# État `UKR` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `UKR` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.200, -0.850]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `92.0` | `e_PDI` |
| Individualism (IDV) | `25.0` | `e_IDV` |
| Masculinity (MAS) | `27.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `95.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `86.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `18.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.5452` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1001` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0948` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0623` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0495` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0406` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0282` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0281` |

| [African](../taxonomy/civilizations/african.md) | `0.0237` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0166` |

| [Western](../taxonomy/civilizations/western.md) | `0.0109` |




## Tenseur de tension civilisationnelle `T(UKR)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `2666.73` | Tension totale |
| `I2` (déviatorique) | `3339869.24` | Asymétrie |
| `det(T)` | `3.16e+12` | Rigidité |
| `A` (anisotropie) | `0.996` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[2104.79, 231.19, 160.49, 116.46, 46.3, 7.5]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`UKR.geojson`](../assets/data/states/UKR.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`UKR.profile.json`)](../assets/data/states/UKR.profile.json)

- [Géométrie (`UKR.geojson`)](../assets/data/states/UKR.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

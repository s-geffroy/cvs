# État `ITA` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `ITA` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.400, 0.850]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0225, 0.0000],
   [0.0000, 0.0225]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `50.0` | `e_PDI` |
| Individualism (IDV) | `76.0` | `e_IDV` |
| Masculinity (MAS) | `70.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `75.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `61.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `30.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Western](../taxonomy/civilizations/western.md) | `0.1796` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.1587` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1350` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.1212` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0830` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0678` |

| [African](../taxonomy/civilizations/african.md) | `0.0664` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0585` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0477` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0421` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0400` |




## Tenseur de tension civilisationnelle `T(ITA)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `3764.79` | Tension totale |
| `I2` (déviatorique) | `3852376.22` | Asymétrie |
| `det(T)` | `1.47e+14` | Rigidité |
| `A` (anisotropie) | `0.995` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[2337.08, 762.25, 335.03, 224.59, 94.19, 11.65]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`ITA.geojson`](../assets/data/states/ITA.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`ITA.profile.json`)](../assets/data/states/ITA.profile.json)

- [Géométrie (`ITA.geojson`)](../assets/data/states/ITA.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

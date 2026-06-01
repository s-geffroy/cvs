# État `SGP` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `SGP` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : (simplification 110m — territoire non rendu)

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- **`x_viz`** (Traditional ↔ Secular-Rational, Survival ↔ Self-Expression) =
  `[0.300, -0.400]`

- **Ellipse 80 %** (`Σ_viz`) — covariance =
  ```
  [[0.0324, 0.0000],
   [0.0000, 0.0324]]
  ```




### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `74.0` | `e_PDI` |
| Individualism (IDV) | `20.0` | `e_IDV` |
| Masculinity (MAS) | `48.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `8.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `72.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `46.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.4704` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.1431` |

| [African](../taxonomy/civilizations/african.md) | `0.0798` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0763` |

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.0568` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.0507` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.0439` |

| [Western](../taxonomy/civilizations/western.md) | `0.0286` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0201` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.0191` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0113` |




## Tenseur de tension civilisationnelle `T(SGP)`

`T(s) ∈ ℝ^{6×6}` symétrique semi-défini positif, analogue au tenseur des contraintes
en mécanique des milieux continus. Cf. [Méthodologie 09](../methodology/09_civilizational_mechanics.md).

### Invariants scalaires

| Invariant | Valeur | Interprétation |
|---|---|---|
| `I1 = tr(T)` | `2872.63` | Tension totale |
| `I2` (déviatorique) | `3628320.97` | Asymétrie |
| `det(T)` | `8.91e+12` | Rigidité |
| `A` (anisotropie) | `0.992` | (λ₁−λ₆)/λ₁ |

### Tensions principales (eigenvalues triées)

`[2203.61, 305.99, 201.83, 108.86, 35.3, 17.03]`




## Téléchargements

- [Profil JSON brut (`SGP.profile.json`)](../assets/data/states/SGP.profile.json)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

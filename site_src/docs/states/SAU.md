# État `SAU` — profil civilisationnel

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

**ISO3** : `SAU` ·
**Couverture B_vec** : B_viz + B_score (complet) ·
**Données géométriques** : Natural Earth 110m

## Coordonnées B_vec

### `B_viz = ℝ²` — Inglehart-Welzel


- *Coordonnées Inglehart-Welzel manquantes pour cet État.*



### `B_score = ℝ⁶` — Hofstede

| Dimension | Score | Notation |
|---|---|---|
| Power Distance (PDI) | `95.0` | `e_PDI` |
| Individualism (IDV) | `25.0` | `e_IDV` |
| Masculinity (MAS) | `60.0` | `e_MAS` |
| Uncertainty Avoidance (UAI) | `80.0` | `e_UAI` |
| Long-Term Orientation (LTO) | `36.0` | `e_LTO` |
| Indulgence vs Restraint (IVR) | `52.0` | `e_IVR` |



## Vecteur d'affinité civilisationnelle

Distribution dérivée par softmax inverse-distance dans `B_score` (β = 0.05).
Somme = 1, w ≥ 0.

| Civilisation | Affinité |
|---|---|

| [Buddhist](../taxonomy/civilizations/buddhist.md) | `0.2111` |

| [Indigenous](../taxonomy/civilizations/indigenous.md) | `0.1637` |

| [Islamic](../taxonomy/civilizations/islamic.md) | `0.1556` |

| [Latin American](../taxonomy/civilizations/latin_american.md) | `0.1487` |

| [African](../taxonomy/civilizations/african.md) | `0.1234` |

| [Orthodox](../taxonomy/civilizations/orthodox.md) | `0.0620` |

| [Hindic](../taxonomy/civilizations/hindic.md) | `0.0433` |

| [Oceanian](../taxonomy/civilizations/oceanian.md) | `0.0387` |

| [Sinic](../taxonomy/civilizations/sinic.md) | `0.0259` |

| [Japanese](../taxonomy/civilizations/japanese.md) | `0.0149` |

| [Western](../taxonomy/civilizations/western.md) | `0.0128` |




## Second moment civilisationnel `M(SAU)`

`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ) + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

Cf. [Méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

### Invariants scalaires

| Invariant | Valeur | Définition |
|---|---|---|
| `I1 = tr(M)` | `1557.97` | Magnitude totale du second moment |
| `I2` (von Mises) | `768.38` | √(3/2 · s:s) avec `s = M − tr(M)/6 · I` |
| `det(M)` | `1.52e+13` | Déterminant |
| `A` (anisotropie) | `0.967` | (λ₁−λ₆)/λ₁ |

### Décomposition M = Cov_w + biais

| Composante | tr(.) | Interprétation |
|---|---|---|
| Dispersion intra (Cov_w) | `865.43` | Étalement pondéré des centroïdes autour de μ̄ |
| Biais (μ̄ − xₛ)(μ̄ − xₛ)ᵀ | `692.55` | Écart de l'État à son barycentre d'affinité |

### Valeurs propres (descendantes)

`[795.73, 296.88, 234.84, 111.48, 92.47, 26.57]`



## Géométrie

- **Source** : Natural Earth 110m (`ne_110m_admin_0_countries`), domaine public.
- **Téléchargement** : [`SAU.geojson`](../assets/data/states/SAU.geojson)
- **Provenance** : `geometry_source = "Natural Earth"` · `contains_gadm_geometry = false`.


## Téléchargements

- [Profil JSON brut (`SAU.profile.json`)](../assets/data/states/SAU.profile.json)

- [Géométrie (`SAU.geojson`)](../assets/data/states/SAU.geojson)


---

[Retour à la liste des États](../index.md) ·
[Carte interactive](../map/index.md) ·
[Base vectorielle B_vec](../basis/index.md) ·
[Algèbre des distances](../distances/index.md)

# Taxonomie hyper-détaillée — `macro_civilizations.v2`

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

!!! info "Statut : en relecture (Phase 1b)"
    Cette taxonomie est publiée dès maintenant pour permettre la relecture par des tiers
    avant la stabilisation des États en Phase 2. Toute remarque est bienvenue via
    [issue GitHub](https://github.com/s-geffroy/cvs/issues).

Version actuelle : **`2.0.0-state-first-adm1-ready-two-bases`** — 11 civilisations.

## Index des civilisations

| ID | Label | Quadrant IW | Couverture archétypes | Extension Huntington |
|---|---|---|---|---|

| [`western`](civilizations/western.md) | Western | `TS+ / SE+` | complète | — |

| [`orthodox`](civilizations/orthodox.md) | Orthodox | `TS≈0 / SE-` | complète | — |

| [`islamic`](civilizations/islamic.md) | Islamic | `TS- / SE-` | complète | — |

| [`sinic`](civilizations/sinic.md) | Sinic | `TS+ / SE-` | complète | — |

| [`hindic`](civilizations/hindic.md) | Hindic | `TS- / SE-` | ⚠️ faible | — |

| [`japanese`](civilizations/japanese.md) | Japanese | `TS++ / SE≈0` | ⚠️ faible | — |

| [`buddhist`](civilizations/buddhist.md) | Buddhist | `TS≈0 / SE≈0` | complète | ✓ |

| [`latin_american`](civilizations/latin_american.md) | Latin American | `TS- / SE+` | complète | — |

| [`african`](civilizations/african.md) | African | `TS-- / SE-` | complète | — |

| [`indigenous`](civilizations/indigenous.md) | Indigenous | `TS-- / SE-` | ⚠️ faible | ✓ |

| [`oceanian`](civilizations/oceanian.md) | Oceanian | `TS+ / SE+` | ⚠️ faible | ✓ |


## Politique

| Clé | Valeur |
|---|---|

| `raw_vector_is_source_of_truth` | `True` |

| `normalized_vector_visualization_only` | `True` |

| `adm1_subdivision_required_later` | `True` |

| `two_bases_coupled` | `True` |


## Couplage B_doc ↔ B_vec

Chaque civilisation porte simultanément :

- **`citation_ids[]`** vers `bibliography[]` racine (B_doc),
- **`mu_viz`** dans `B_viz = ℝ²` (Inglehart-Welzel),
- **`mu_score`** dans `B_score = ℝ⁶` (Hofstede 6D).

Aucune coordonnée n'est orpheline ; aucune citation n'est orpheline.
Tests d'invariants : `tests/test_bases_coupling.py`.

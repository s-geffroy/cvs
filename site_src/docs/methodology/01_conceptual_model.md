# 01 — Modèle conceptuel

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md`](07_ethics_publication_policy.md).

## 1. Deux formes du vecteur civilisationnel

Le projet distingue deux formes pour les artefacts internes :

- **Vecteur brut** : source de vérité analytique. Conserve les magnitudes, l'incertitude, les composantes non-normalisées.
- **Vecteur normalisé** : dérivé du vecteur brut, utilisé uniquement pour visualisation et comparaison sur le simplexe `Δ¹⁰`.

L'opération de normalisation utilise un softmax inverse-distance (cf. [doc 08 §4.2](08_civilizational_basis.md)).

## 2. Couches civilisationnelles

Le modèle articule trois **couches** :

```
[
  "macro_civilization_vector_raw",     # 11 macro-civilisations (Huntington + extensions)
  "subcivilization_vector_raw",        # sous-clusters (e.g. anglo-saxon, protestant_europe)
  "interface_zone_vector_raw"          # États à l'interface entre civilisations
]
```

En V1, seul le **macro_civilization_vector** est activement publié sous forme normalisée (`wₛ ∈ Δ¹⁰`). Les sous-clusters et zones d'interface sont **structurellement définis** dans `taxonomies/macro_civilizations.v2.json` (champs `sub_clusters[]`, `ambiguous_cases[]`) mais ne portent pas de coordonnées calculées propres.

## 3. Interprétation à l'échelle État

À l'échelle d'un État souverain, certaines couches ne sont **estimables qu'approximativement** :

- Les sous-clusters demanderaient des données régionales sub-nationales (ADM1).
- Les zones d'interface supposent une modélisation des frontières civilisationnelles, non implémentée.

La sortie publique d'un État porte donc :

- Vecteur `wₛ` (macro), dérivé.
- Coordonnées `xₛ^viz`, `xₛ^score`.
- Second moment `M(s)`.
- Intervalles de confiance (`Σₛ^viz` pour B_viz, drapeau `imputed` pour B_score).
- Evidence trace (`source_refs[]`).
- Comparabilité (drapeaux `coverage`, `low_evidence`).

## 4. Anticipation ADM1

Aucune sortie ADM1 active. L'architecture conserve :

- Schémas `adm1_profile.v2.schema.json`.
- Hook CLI `civvec score --unit-type adm1` qui retourne `prepared_not_active`.
- Géométries geoBoundaries ADM1 versionnées (non publiées).

Cf. [doc 04](04_adm1_preparation_policy.md).

## 5. Articulation B_doc ↔ B_vec

Le modèle conceptuel repose sur **deux bases interdépendantes** au premier rang :

- **B_doc** (documentaire) : citations académiques, taxonomie sourcée.
- **B_vec** (vectorielle) : `B_viz = ℝ²` (Inglehart-Welzel) ⊕ `B_score = ℝ⁶` (Hofstede).

Chaque coordonnée `μᵢ`, `xₛ` dans `B_vec` est **sourcée** par des `citation_ids[]` vers `B_doc`. Inversement, chaque entrée de `B_doc` portant une civilisation a ses coordonnées `μᵢ` calculées et **stockées** dans la taxonomie. Cf. [doc 08](08_civilizational_basis.md) pour la formalisation et `tests/test_bases_coupling.py` pour les invariants vérifiés.

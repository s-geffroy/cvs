# Guide de relecture — Phase 1b

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées.
    Il ne doit pas être utilisé pour classer des individus réels.

Ce site est publié **délibérément tôt** pour permettre la relecture par des tiers
avant la stabilisation des États (Phase 2). Vos remarques sont les bienvenues.

## Ouvrir une issue

[github.com/s-geffroy/cvs/issues](https://github.com/s-geffroy/cvs/issues)

Conventions de titre :

- `[taxo]` pour une remarque sur la taxonomie hyper-détaillée (`macro_civilizations.v2.json`).
- `[doc]` pour une remarque sur la méthodologie (`docs/00..10_*.md`).
- `[biblio]` pour une citation manquante ou erronée.
- `[base]` pour une remarque sur `B_viz` ou `B_score`.
- `[éthique]` pour une remarque sur la politique de publication.

## Points d'attention prioritaires (Phase 1b)

1. **Taxonomie `macro_civilizations.v2.json`** :
    - Les **rôles** `core | periphery | ambiguous | interface` sont-ils défendables ?
    - Manque-t-il des **cas ambigus** documentés (Turquie, Russie, Israël, Mexique, Belgique, Pays-Bas, Sri Lanka, Corée du Sud) ?
    - Les **sous-clusters** capturent-ils les distinctions internes utiles (ex : Anglo vs Europe protestante vs Europe catholique chez Western) ?
2. **Extensions à Huntington** (`buddhist`, `indigenous`, `oceanian`) :
    - Sont-elles **suffisamment sourcées** ?
    - Le drapeau `low_archetype_coverage` est-il correctement positionné ?
3. **Bibliographie** :
    - Citations orphelines détectées par `tests/test_documentary_basis.py::test_all_citation_ids_resolve_to_bibliography`.
    - Manque-t-il une référence importante (Inglehart 2018, Welzel 2013, Norris-Inglehart 2019…) ?
4. **Choix B_vec** :
    - Le couplage `B_viz` (Inglehart-Welzel 2D) + `B_score` (Hofstede 6D) est-il défendable ?
    - Le calcul d'affinité par **softmax inverse-distance** dans `B_score` produit-il des résultats cohérents avec la classification Huntington ?
5. **Mécanique tensorielle** (`docs/09_civilizational_mechanics.md`) :
    - L'analogie avec le tenseur des contraintes en milieux continus tient-elle ?
    - Les invariants `I1`, `I2`, `det` sont-ils correctement définis ?
6. **Algèbre des distances** (`docs/10_distance_algebra.md`) :
    - Les **poids par défaut** `α=0.4, β=0.4, γ=0.2` de `d_hyb` sont-ils raisonnables ?
    - La distance **Wasserstein-2** est-elle correctement implémentée (Sinkhorn, λ=0.05) ?

## Workflow PR

1. Fork → branche feature → PR vers `main`.
2. La CI exécute `pytest` + `mkdocs build --strict` en container.
3. Préviewer local : `docker compose build civvec_site && docker compose run --rm civvec_site && docker run --rm -p 8080:80 -v "$PWD/dist:/usr/share/nginx/html:ro" nginx:alpine`.

## Non couvert en Phase 1b

- Pages États (FRA, …) → Phase 2.
- Carte interactive MapLibre → Phase 2.
- Page B_vec interactive (scatter + radars) → Phase 2.

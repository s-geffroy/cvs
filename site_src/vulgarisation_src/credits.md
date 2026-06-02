---
title: Crédits et sources
---

## Qui ?

cvs est un projet **open source** dirigé par **s-geffroy** (auteur principal). Le projet accueille les contributions externes via [GitHub](https://github.com/s-geffroy/cvs/issues).

## Quoi ?

cvs (*Civilizational Vector State*) est un pipeline Python bayésien produisant un **vecteur d'affiliation civilisationnelle** par État souverain. Il publie :

- Un **site MkDocs** complet avec méthodologie, taxonomie, fiches États, carte interactive, base vectorielle, seconds moments, distances.
- Un **mini-site de vulgarisation** (cette section).
- Un ensemble de **fichiers JSON** machine-lisibles (sous `assets/data/`).
- Des **schémas JSON v3** (sous `assets/schemas/`).
- Un **CLI Python** (`civvec …`) pour reconstruire localement.

## Licences

| Élément | Licence |
|---|---|
| **Code source** | MIT |
| **Documentation et site** | MIT (incluant cette section) |
| **WVS** (données) | CC-BY |
| **Hofstede** (données) | Usage scientifique autorisé |
| **Inglehart-Welzel** (données) | Reprise des publications WVS |
| **Natural Earth** (géométries) | Domaine public |
| **geoBoundaries** (géométries) | CC-BY 4.0 |
| **GADM** (géométries) | **Non utilisé** — restriction de redistribution |

Voir le fichier `data_sources/SOURCES.md` du dépôt pour la traçabilité complète.

## Comment citer cvs ?

```bibtex
@misc{cvs2026,
  author       = {Geffroy, S.},
  title        = {Civilizational Vector State: A Bayesian Pipeline for
                  State-Level Civilizational Affiliation Vectors},
  year         = {2026},
  version      = {3.0.0a1},
  url          = {https://github.com/s-geffroy/cvs},
  note         = {Published under MIT License. Accessed via
                  \url{https://s-geffroy.github.io/cvs/}}
}
```

Pour citer une **page spécifique** (méthodologie 09, par exemple), citer l'URL pleine : `https://s-geffroy.github.io/cvs/methodology/09_civilizational_second_moment/`.

## Remerciements

Le projet repose sur les **travaux de toute une communauté académique**, qu'il agrège :

- **Ronald Inglehart** (1934-2021) et **Christian Welzel**, pour le *World Values Survey* et la carte 2D des valeurs.
- **Geert Hofstede** (1928-2020) et **Michael Minkov**, pour les 6 dimensions culturelles.
- **Samuel Huntington** (1927-2008), pour la taxonomie de départ — **utilisée comme prior**, critiquée et complétée.
- L'équipe **Natural Earth** (Tom Patterson, Nathaniel Kelso) pour les géométries en domaine public.
- L'équipe **geoBoundaries** (William & Mary) pour les géométries CC-BY 4.0.

## Et les critiques académiques ?

cvs **inclut** dans sa documentation officielle 27 critiques anticipées — y compris celles qu'il **n'a pas su corriger**. Voir [Controverses académiques](niveau-3-etudiant-shs/controverses-academiques.html) (vulgarisation) et [doc 11](../methodology/11_critiques_and_responses/) (site principal).

## Contact

- **Issues** (bug, critique, suggestion) : <https://github.com/s-geffroy/cvs/issues>
- **Pull Requests** : <https://github.com/s-geffroy/cvs/pulls>
- **Pas d'email public** ; tous les échanges passent par GitHub pour la traçabilité.

## Version de cette page

Cette section de vulgarisation accompagne cvs **v3.0.0a1** (publication 2026). Les chiffres cités (proximités, distances) sont **stables** sur cette version mais peuvent évoluer aux versions suivantes.

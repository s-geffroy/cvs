---
title: Les 3 distances en une image
---

cvs publie **plusieurs façons** de mesurer la distance entre deux pays. Voici les 3 plus utiles, **sans formules**, avec une image mentale pour chacune.

## Distance 1 — `d_viz` : la distance sur la carte 2D

> 🗺️ Image mentale : **deux épingles sur la carte d'Inglehart-Welzel** (le plan « tradition ↔ rationalité » × « survie ↔ expression de soi »). On mesure la distance à la règle.

- Simple, lisible, visuelle.
- Bonne pour les graphiques grand public.
- Limite : 2 dimensions seulement, ça écrase de l'information.

## Distance 2 — `d_score^M` : la distance dans les 6 dimensions de Hofstede

> 📏 Image mentale : **deux profils de personnalité** (l'un de la France, l'autre du Japon), chacun décrit par 6 traits (hiérarchie, individualisme, masculinité, incertitude, long terme, indulgence). On compare les profils en tenant compte du fait que certaines dimensions sont plus discriminantes que d'autres.

- Plus riche que `d_viz`.
- Tient compte du fait que tous les pays ne s'écartent pas de la même façon dans toutes les dimensions.
- Limite : nécessite que les 6 chiffres existent (manquants pour certains pays).

## Distance 3 — `d_hyb` : la distance hybride (la « meilleure »)

> 🧪 Image mentale : **un mélange savant** des deux précédentes + une troisième composante (qui compare aussi les **tensions internes** du pays — voir page suivante). C'est la distance recommandée pour la plupart des usages.

- C'est la distance « par défaut » publiée par cvs.
- Plus stable que les distances simples.
- Limite : son interprétation est moins intuitive.

## En une image

```
[d_viz]      ←  carte 2D, visuel, grand public
[d_score^M]  ←  6 dimensions Hofstede, plus précis
[d_hyb]      ←  mélange équilibré, par défaut
```

## Le piège du « tableau de comparaison »

> ❌ « La France est plus proche de la Suède que de l'Italie selon cvs : 0.24 vs 0.31. »

Ce genre de phrase est techniquement vrai mais **trompeur** parce que :

1. Le lecteur ne sait pas quelle distance on utilise.
2. La différence entre 0.24 et 0.31 peut être **dans le bruit** (intervalle de confiance non publié).
3. Une autre distance pourrait donner l'**ordre inverse**.

Bonne pratique : citer la **distance utilisée**, et préciser que le **classement entre voisins proches** est instable.

## Et les autres distances ?

cvs publie aussi des distances plus exotiques (cosine, Jensen-Shannon, Wasserstein, Frobenius). Elles servent surtout à la recherche — pour le grand public, **`d_viz` ou `d_hyb` suffisent**.

Pour les détails complets : [doc 10 — Algèbre des distances](../../methodology/10_distance_algebra/) du site principal.

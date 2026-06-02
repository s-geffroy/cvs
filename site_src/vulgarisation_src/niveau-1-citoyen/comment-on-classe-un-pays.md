---
title: Comment on « classe » un pays ?
---

## Une métaphore : la playlist Spotify

Quand Spotify vous classe dans « auditeur de pop indie + rap français + un peu de jazz », il ne vous met **pas dans une boîte**. Il dit : « voilà à quoi vous ressemblez, en pourcentage ».

cvs fait exactement pareil avec les pays. Au lieu de dire « la France est occidentale, point », il dit :

| Famille | % de proximité |
|---|---|
| Occidentale | 71 % |
| Latino-américaine | 11 % |
| Orthodoxe | 7 % |
| Autres | 11 % |

(Les chiffres exacts viennent du fichier `state_coordinates.json` du projet ; ils peuvent varier avec les versions.)

## D'où viennent les chiffres ?

Trois sources, **toutes publiques** :

1. **WVS** — la *World Values Survey*, une grande enquête mondiale qui pose à des dizaines de milliers de personnes des questions du type : « Faites-vous confiance à vos voisins ? », « Pour vous, la religion est-elle importante ? ».
2. **Hofstede** — six grandes dimensions qui décrivent les cultures (hiérarchique vs égalitaire, individualiste vs collectiviste, etc.). Ces six chiffres ont été calculés à partir d'employés d'IBM dans les années 70, puis affinés depuis.
3. **Inglehart-Welzel** — une carte en 2D qui place les pays sur deux axes : *tradition ↔ rationalité* et *survie ↔ expression de soi*.

cvs **mélange** ces sources et calcule, pour chaque pays, sa **distance** à chacune des familles civilisationnelles. Plus la distance est petite, plus le % de proximité est grand.

## Les ingrédients en images

> 🥦 WVS = ce que les gens **disent** dans une enquête.
>
> 📏 Hofstede = six chiffres qui résument la **culture professionnelle**.
>
> 🗺️ Inglehart-Welzel = une **carte 2D** des grandes valeurs.

Mélangez les trois → un vecteur de proximité par pays.

## Ce qu'on **ne** fait **pas**

- On ne va **pas** chercher la religion officielle d'un pays.
- On ne va **pas** chercher sa langue.
- On ne va **pas** chercher son histoire coloniale.
- On ne va **pas** chercher son PIB.

Tout repose sur **ce que les habitants ont déclaré** dans des enquêtes, et sur quelques chiffres culturels agrégés.

## En une ligne

> Classer un pays = mesurer sa **distance** à chaque famille, et dire « voilà à quoi tu ressembles, en pourcentage ».

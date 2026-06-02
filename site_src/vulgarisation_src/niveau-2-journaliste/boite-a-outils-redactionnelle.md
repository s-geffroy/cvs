---
title: Boîte à outils rédactionnelle
---

Une **antisèche** pour rédiger juste, et un set d'**équivalences** pour traduire le jargon technique en français de salle de rédaction.

## Formulations à préférer / à éviter

| ✅ À préférer | ❌ À éviter |
|---|---|
| « Le profil **agrégé** du pays X » | « Le pays X » (tout court) |
| « D'après les données **publiques agrégées** par cvs » | « Selon cvs » (trop court, perd la provenance) |
| « Une proximité d'environ 70 % à la famille **dite** occidentale » | « 70 % occidental » |
| « cvs **regroupe** les pays par famille civilisationnelle » | « cvs **classe** les pays » |
| « Les **moyennes déclarées** dans WVS » | « Les opinions des X-ais » |
| « Une **distance statistique** entre deux profils nationaux » | « L'écart culturel entre deux peuples » |
| « Ce projet **ne mesure pas** d'individus » | (omettre la précaution) |

## Glossaire de la salle de rédaction

| Terme technique cvs | Traduction simple |
|---|---|
| `B_doc` | Les sources livresques de départ (Huntington, IW, Hofstede) |
| `B_vec` | La représentation numérique des pays |
| `B_viz` | La carte 2D (Inglehart-Welzel) |
| `B_score` | Les six dimensions de Hofstede |
| Vecteur d'affiliation | Le **profil en pourcentages** d'un pays |
| Centroïde | Le **point moyen** d'une famille civilisationnelle |
| Distance hybride `d_hyb` | La distance par défaut, **recommandée** |
| `M(s)`, « second moment » | Les **tensions internes** d'un pays (dispersion autour de sa moyenne) |
| Wasserstein-2 | Une distance « transport optimal » — savante mais robuste |
| Mahalanobis | Une distance qui **tient compte** du fait que toutes les dimensions n'ont pas le même poids |

## Templates de phrase prêts à reprendre

### Introduction d'un article

> « Une équipe propose une nouvelle façon de visualiser les proximités culturelles entre pays. Baptisé *Civilizational Vector State*, ce projet open source agrège trois sources publiques (l'enquête WVS, les six dimensions de Hofstede, la carte d'Inglehart-Welzel) pour calculer, pour chaque État souverain couvert, un **vecteur de proximité** à une dizaine de grandes familles civilisationnelles. Les auteurs préviennent que cet outil **ne doit pas servir à classer des individus** : il s'agit d'agrégats statistiques au niveau de l'État. »

### Citation d'un chiffre précis

> « Le profil agrégé de la France apparaît, dans cvs, dominé par la famille dite **occidentale** (≈70 %), avec une teinte **latine** secondaire (≈10 %). À titre de comparaison, le profil agrégé de la Suède est davantage tiré vers les valeurs dites **post-matérialistes** sur la carte d'Inglehart-Welzel. »

### Conclusion ou encadré « méthode »

> « cvs est un **instantané** : ses données proviennent principalement de la 7ᵉ vague de WVS (2017-2022). Le projet, publié sous licence MIT, met à disposition l'ensemble de sa **méthodologie**, ses **schémas JSON** et ses 27 **critiques académiques anticipées**. »

## Trois choses à toujours préciser

1. **La date des données** (vague WVS), pas la date de l'article.
2. **La nature agrégée** (par État, jamais par individu).
3. **L'avertissement éthique** (« ne doit pas être utilisé pour classer des individus réels »).

## Les liens à mettre dans votre article

- Site principal : <https://s-geffroy.github.io/cvs/>
- Fiche pays d'exemple (France) : <https://s-geffroy.github.io/cvs/states/FRA/>
- Carte interactive : <https://s-geffroy.github.io/cvs/map/>
- Éthique : <https://s-geffroy.github.io/cvs/ethics/>
- Code source : <https://github.com/s-geffroy/cvs>

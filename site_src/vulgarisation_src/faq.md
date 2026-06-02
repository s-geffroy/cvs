---
title: Questions fréquentes
---

## 1. cvs, c'est de l'astrologie pour les nations ?

Non. cvs **ne prédit pas** l'avenir et **ne juge pas** les pays. Il décrit **où ils se situent**, statistiquement, à partir d'**enquêtes publiques**. C'est de la statistique descriptive — pas de la divination.

## 2. Pourquoi pas la Russie dans la famille « occidentale » ?

Parce que les chiffres de WVS et de Hofstede placent la Russie **plus près du cluster orthodoxe** (Bulgarie, Serbie, Grèce, Ukraine, Roumanie) que du cluster occidental. C'est une **mesure empirique**, pas un jugement politique.

## 3. Vous êtes pro-Huntington ?

Non. cvs **utilise** la taxonomie de Huntington comme **carte de départ** parce qu'elle est familière et bibliographiquement référencée — pas parce qu'on croit à la thèse du « choc des civilisations ». Voir [Huntington en 2 pages](niveau-3-etudiant-shs/huntington-en-2-pages.html).

## 4. Où sont vos données ?

Toutes les données sources sont publiques :
- **WVS** : <https://www.worldvaluessurvey.org/>
- **Hofstede** : dossier `data_sources/hofstede/` du code source.
- **Inglehart-Welzel** : dossier `data_sources/iw/` du code source.
- **Natural Earth** (géométries) : <https://www.naturalearthdata.com/>

cvs **republit** ces données dans son propre dépôt avec leurs **licences** (cf. [Crédits](credits.html)).

## 5. Pourquoi pas mon pays ?

Si votre pays n'apparaît pas, c'est probablement parce que la **vague 7 de WVS** ne l'a pas couvert. cvs ne **fabrique pas** de données : il **utilise** ce qui existe. ~130 États sont **non couverts**.

## 6. Vous calculez chaque année ?

Non. cvs est **statique** : il reflète la dernière vague de données. La prochaine vague WVS (8ᵉ) sortira progressivement et cvs sera mis à jour quand elle sera complète.

## 7. Peut-on utiliser cvs pour faire de la politique migratoire / RH / cybersécurité ?

**Non.** L'avertissement éthique est explicite : *« Ces profils ne doivent jamais être utilisés pour classer des individus réels. »* cvs travaille au niveau **agrégé d'États**. L'utiliser pour décider du sort d'**une** personne est un **mésusage** explicitement rejeté.

## 8. La France à 71 % « occidentale », ça veut dire que 29 % des Français ne sont pas occidentaux ?

Non. **Aucun individu** n'est concerné par cette mesure. « 71 % » est la **proximité du profil agrégé français** au profil agrégé de la famille occidentale. Ce **n'est pas** un pourcentage d'individus.

## 9. cvs est-il open source ?

Oui, sous **licence MIT**. Le code, la documentation, les schémas JSON et les données curées sont sur <https://github.com/s-geffroy/cvs>.

## 10. Comment citer cvs dans un article académique ?

Voir [Crédits et sources](credits.html) pour la citation au format BibTeX.

## 11. cvs est-il « vrai » ?

cvs est **reproductible** : tout le pipeline est en open source, toutes les données sources sont publiques. Quelqu'un peut **vérifier** chaque chiffre. Ça ne veut pas dire que cvs est « vrai » — toute mesure de SHS est une **simplification**.

## 12. Vous prévoyez d'aller plus loin que les États ?

cvs **prépare** une couche **ADM1** (régions administratives infranationales — départements en France, États aux US, gouvernorats en Égypte…) mais ne l'a **pas activée en V1** pour des raisons de licence (GADM, non utilisable) et de qualité. Voir [Politique ADM1 préparée](../adm1_policy/) sur le site principal.

## 13. Comment proposer une correction ?

Ouvrez une **issue** sur GitHub : <https://github.com/s-geffroy/cvs/issues>. Si vous identifiez :
- Une **donnée fausse** dans une source publique.
- Une **erreur de méthodologie**.
- Une **critique académique** non listée dans [doc 11](../methodology/11_critiques_and_responses/).

Toutes les remarques sont les bienvenues. Le projet est en relecture publique permanente.

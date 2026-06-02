---
title: Hofstede en 2 pages
---

## L'idée principale

Geert **Hofstede** (1928-2020), psychologue social néerlandais, dirige un service de recherche RH chez **IBM** dans les années 1970. Il analyse les questionnaires de salariés d'IBM dans une cinquantaine de pays et identifie **6 grandes dimensions** sur lesquelles les cultures nationales se distinguent.

| Dimension | Question simple |
|---|---|
| **PDI** — *Power Distance Index* | À quel point l'inégalité hiérarchique est-elle acceptée ? |
| **IDV** — *Individualism vs Collectivism* | Le « je » prime-t-il sur le « nous » ? |
| **MAS** — *Masculinity vs Femininity* | La société valorise-t-elle compétition/réussite ou soin/coopération ? |
| **UAI** — *Uncertainty Avoidance Index* | Tolère-t-on l'incertitude ou la fuit-on ? |
| **LTO** — *Long-Term Orientation* | Préfère-t-on tradition + court terme ou pragmatisme + long terme ? |
| **IVR** — *Indulgence vs Restraint* | La société autorise-t-elle la gratification ou la réprime-t-elle ? |

À l'origine il y avait 4 dimensions ; LTO et IVR ont été ajoutées dans les années 90 et 2000 grâce à des collaborations (Bond, Minkov).

## Pourquoi c'est utile pour cvs

- **Six chiffres par pays** → cvs construit `B_score = ℝ⁶`, un espace de dimension 6 dans lequel chaque pays est un point.
- Données **largement publiées**, faciles à intégrer, **interprétables**.
- Permet de calculer des **distances Mahalanobis** entre pays (qui tiennent compte du fait que toutes les dimensions n'ont pas la même variance).

## Critiques principales

| Critique | Auteur clé |
|---|---|
| **Échantillon biaisé** : ne s'appuie que sur des employés IBM (cadres et techniciens) — pas représentatif de la population générale | McSweeney (2002) |
| **Stabilité postulée** : Hofstede présente les dimensions comme stables sur des décennies, c'est empiriquement discutable | Ailon (2008) |
| **Orthogonalité postulée** : les 6 dimensions sont présentées comme indépendantes, mais les corrélations empiriques sont fortes | Minkov & Hofstede (2014) — autocritique partielle |
| **Effet « culture nationale »** : Hofstede confond la culture nationale avec la culture d'une entreprise multinationale particulière (IBM) | McSweeney (2002) |
| **Échelle simplifiée** : 6 chiffres pour résumer la culture d'un pays, c'est réducteur | Baskerville (2003) |

Voir [doc 08 §3.2](../../methodology/08_civilizational_basis/) du site principal — qui étiquette explicitement l'orthogonalité comme **« postulée non vérifiée empiriquement »**.

## Comment cvs traite ces critiques

- **Échantillon biaisé** : cvs **complète** Hofstede avec WVS (échantillon population générale) et avec Inglehart-Welzel — donc le biais IBM est noyé dans des sources plus larges.
- **Orthogonalité** : cvs utilise des **distances Mahalanobis intra-civilisationnelles** qui tiennent compte de la covariance réelle entre dimensions (pas une orthogonalité postulée).
- **Stabilité** : cvs publie une **date de capture** explicite et prévoit des **réplications** futures sur les vagues WVS suivantes.
- **Échelle simplifiée** : cvs ajoute la couche `M(s)` (second moment) qui mesure la **dispersion** autour de la moyenne — autrement dit, la simplification à 6 chiffres est **accompagnée** d'une mesure de la perte d'information.

## L'attitude de cvs envers Hofstede

> cvs **utilise** Hofstede comme une **commodité métrique** (6 axes interprétables), pas comme une vérité culturelle absolue. Les axes sont utiles parce qu'ils sont **partagés** par d'autres travaux académiques — pas parce qu'on croit qu'ils épuisent ce qu'est une culture.

## Pour aller plus loin

- Hofstede, *Cultures and Organizations: Software of the Mind*, 2010 (3ᵉ éd.).
- McSweeney, *Hofstede's Model of National Cultural Differences and their Consequences: A Triumph of Faith — a Failure of Analysis*, 2002 (la critique de référence).
- Site principal cvs : [doc 08 — Base civilisationnelle](../../methodology/08_civilizational_basis/).

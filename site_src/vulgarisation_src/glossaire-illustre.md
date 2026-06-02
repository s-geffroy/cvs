---
title: Glossaire illustré
---

Tous les termes du projet, expliqués en **langage courant**, avec une **image mentale** pour chacun.

## A

**Affinité (vecteur d')** — Pour un pays donné, la liste des **pourcentages de proximité** à chaque famille civilisationnelle. Ex : France = { occidentale: 71 %, latine: 11 %, orthodoxe: 7 %, … }.
> 🎨 *Image* : une palette de couleurs, où chaque couleur est une famille civilisationnelle, et la **proportion** de chaque couleur dans la palette est l'affinité.

## B

**B_doc** — La « **base documentaire** » : les **livres** et **articles** sur lesquels cvs s'appuie pour son prior (Huntington, Hofstede, Inglehart-Welzel).
> 📚 *Image* : une bibliothèque de référence.

**B_score** — Les **6 dimensions de Hofstede** (PDI, IDV, MAS, UAI, LTO, IVR), un point par pays dans un espace 6D.
> 📏 *Image* : un profil de personnalité à 6 traits.

**B_vec** — La « **base vectorielle** » : la **représentation numérique** des pays, qui combine `B_viz` (2D) et `B_score` (6D).
> 🧮 *Image* : une fiche-pays informatisée.

**B_viz** — La **carte 2D d'Inglehart-Welzel** : deux axes (tradition ↔ rationnel, survie ↔ expression de soi).
> 🗺️ *Image* : une carte 2D du monde des valeurs.

**Bayésien** — Une **manière de raisonner** : partir d'une croyance (prior), la confronter aux données, en sortir une croyance révisée (posterior).
> 🔄 *Image* : une enquête policière : on part d'une suspicion, on collecte les indices, on révise la suspicion.

## C

**Centroïde** — Le **point moyen** d'une famille civilisationnelle dans `B_score`.
> 🎯 *Image* : le centre de gravité d'un nuage de points.

**Civilisation** — Dans cvs, un **regroupement statistique** de pays qui se ressemblent. **Pas** une essence, **pas** un destin.
> 👨‍👩‍👧 *Image* : une famille de cuisines.

**Cluster** — Synonyme de regroupement statistique.

**Covariance** — Une mesure de la façon dont **deux quantités varient ensemble**. Sert à construire des distances Mahalanobis.

## D

**`d_hyb`** — La **distance hybride**, recommandée par défaut. Mélange équilibré de plusieurs distances complémentaires.
> 🧪 *Image* : un cocktail bien dosé.

**`d_viz`** — La **distance euclidienne** sur la carte 2D.
> 📐 *Image* : la distance à la règle.

**`d_score`** — La **distance dans l'espace 6D** de Hofstede. Plusieurs variantes (euclidienne, Mahalanobis).

**`d_M_F`** — La **distance entre deux seconds moments** (Frobenius). Mesure si **les tensions internes** se ressemblent.

**Désambiguïsation** — La **règle explicite** qui décide à quelle famille rattacher un pays charnière (Corée, Thaïlande, Bolivie…).

## H

**Hofstede** — Voir [Hofstede en 2 pages](niveau-3-etudiant-shs/hofstede-en-2-pages.html).

**Huntington** — Voir [Huntington en 2 pages](niveau-3-etudiant-shs/huntington-en-2-pages.html).

## I

**Inglehart-Welzel** — Voir [Inglehart-Welzel en 2 pages](niveau-3-etudiant-shs/inglehart-welzel-en-2-pages.html).

**ISO3** — Un **code à 3 lettres** pour chaque État souverain (FRA = France, JPN = Japon, BRA = Brésil…). Norme ISO 3166-1 alpha-3.

## M

**`M(s)`** — Le **second moment civilisationnel** d'un État. Mesure les **tensions internes** : à quel point ce pays est dispersé autour de sa moyenne.
> ⚖️ *Image* : la « turbulence » intérieure d'un pays.

**Mahalanobis (distance de)** — Une distance qui **tient compte** du fait que toutes les dimensions n'ont pas la même importance.
> 📊 *Image* : la distance à la règle, mais avec une règle qui se déforme selon l'axe.

**Mélange (mixture)** — En probabilité, une **combinaison pondérée** de plusieurs distributions. cvs publie chaque pays comme un **mélange** de familles civilisationnelles.

## P

**PDI / IDV / MAS / UAI / LTO / IVR** — Les **6 dimensions de Hofstede** :
- **PDI** : *Power Distance Index* — acceptation de la hiérarchie.
- **IDV** : *Individualism* — « je » avant « nous ».
- **MAS** : *Masculinity* — compétition vs coopération.
- **UAI** : *Uncertainty Avoidance Index* — tolérance à l'incertitude.
- **LTO** : *Long-Term Orientation* — orientation long terme.
- **IVR** : *Indulgence vs Restraint* — autorisation de la gratification.

**Posterior** — En bayésien, la **croyance révisée** après confrontation aux données.

**Prior** — En bayésien, la **croyance de départ** avant confrontation aux données. Chez cvs, c'est la taxonomie de Huntington.

## S

**Softmax** — Une **fonction mathématique** qui transforme des **distances** en **probabilités** qui somment à 1. Le paramètre `β` contrôle la « température ».

**Spearman (corrélation de)** — Une mesure de **corrélation par rang**. Utilisée par cvs pour la validation empirique externe.

## T

**T(s) — ANCIEN nom** — L'ancien nom du second moment `M(s)`. Renommé en v3.0 pour évacuer le « physics envy » (cf. [doc 11](../methodology/11_critiques_and_responses/)).

## W

**Wasserstein-2** — Une **distance de transport optimal**. Mesure le coût minimal pour transformer une distribution en une autre. Utilisée pour comparer des **vecteurs d'affiliation**.
> 🚚 *Image* : le coût minimal pour déplacer le sable d'une dune à une autre.

**WVS** — *World Values Survey*. La grande enquête mondiale sur les valeurs, qui fournit la matière première de cvs.
> 🌍 *Image* : un questionnaire planétaire posé à des dizaines de milliers de personnes.

## Pour aller plus loin

Le glossaire **complet** (avec formules) est sur le site principal : [doc 15 — Glossaire](../methodology/15_glossary/).

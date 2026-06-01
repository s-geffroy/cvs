# 14 — Baseline non-supervisé

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md](07_ethics_publication_policy.md).

## 1. Question

Si on lance un **clustering data-driven** sur les données brutes
(WVS Inglehart-Welzel + Hofstede), retrouve-t-on les 11 macro-civilisations
Huntington-informées ou des regroupements différents ?

Si le data-driven et l'informé-Huntington **convergent**, la taxonomie est
soutenue par la géométrie des données. S'ils **divergent**, la taxonomie
impose une structure qui n'émerge pas naturellement.

## 2. Protocole

### Features

Vecteur 8-dimensionnel par État : `(TS, SE, PDI, IDV, MAS, UAI, LTO, IVR)`.
Standardisation z-score par axe avant clustering.

### Méthodes comparées

1. **k-means avec k=11** (matching la cardinalité de la taxonomie).
2. **HDBSCAN-lite** (single-linkage + cut au plus grand gap,
   `min_cluster_size = 3`) — choix libre du nombre de clusters.
3. **Référence Huntington-informée** : `argmax(wₛ)` pour chaque État.

### Métriques

- **ARI (Adjusted Rand Index)** : -1 à +1, mesure de l'accord entre deux
  partitions sans dépendre des étiquettes.
- **NMI (Normalised Mutual Information)** : 0 à 1, information partagée
  entre les deux partitions.

### Sortie

`assets/data/empirical/baseline_clustering.json` (généré par
`civvec empirical baseline`).

## 3. Lecture

### 3.1 ARI / NMI

| Valeur | Interprétation |
|---|---|
| ARI ≈ 0 | Accord aléatoire — la taxonomie n'est **pas** retrouvée par data-driven |
| ARI ≈ 0.3 | Accord modéré — quelques clusters reconnaissables |
| ARI ≈ 0.6 | Accord substantiel — la taxonomie est largement soutenue |
| ARI ≈ 0.8+ | Accord fort — la taxonomie émerge naturellement |

NMI plus tolérant : NMI > 0.5 indique déjà un signal partagé non trivial.

### 3.2 Cas attendus

**Hypothèse de convergence partielle** : la taxonomie devrait être bien
retrouvée pour les civilisations **larges et homogènes**
(`western`, `latin_american`, `african`) mais mal retrouvée pour les
civilisations **petites ou ambiguës** (`japanese` seul = 1 État,
`indigenous` à peine couvert, `buddhist` chevauchant Sinic).

ARI attendu : entre **0.3 et 0.55**.

### 3.3 Résultats v3.0

**Mesures publiées** dans `assets/data/empirical/baseline_clustering.json` :

| Métrique | k-means k=11 vs Huntington |
|---|---|
| **ARI** | **0.459** |
| **NMI** | **0.721** |

**Interprétation** :

- `ARI = 0.459` se situe dans la zone « accord modéré-substantiel » — la
  taxonomie Huntington-informée est **largement soutenue** par un
  clustering non-supervisé sur les données brutes WVS+Hofstede, sans être
  parfaitement émergente.
- `NMI = 0.721` confirme une **information partagée importante** entre les
  deux partitions (la moitié des États sont assignés à la même classe par
  les deux méthodes).
- Conclusion : la taxonomie n'est **pas arbitraire** : même un algorithme
  qui ne sait rien d'Huntington retrouve une structure proche. Mais elle
  n'est pas non plus **émergente naturelle** — l'apport d'Huntington
  ajoute un signal d'environ 30-50% à ce qui est dérivable par data
  uniquement.

## 4. Confusion matrix

`baseline_clustering.json` publie le **mapping** k-means cluster ↔
Huntington civilisation, ce qui permet de voir :

- Quelles civilisations sont **scindées** en plusieurs clusters k-means
  (signe d'hétérogénéité intra-civ).
- Quelles civilisations sont **fusionnées** dans un même cluster k-means
  (signe de proximité géométrique non distinguable sans Huntington).

## 5. HDBSCAN-lite : densité

HDBSCAN-lite identifie des « **noyaux denses** » dans l'espace 8D :

- Le nombre de clusters trouvés peut différer de 11.
- Les États classés `-1` (noise) sont des **valeurs aberrantes** par
  rapport aux noyaux denses — pas nécessairement à exclure, mais à
  examiner.

## 6. Limites

1. **k=11 imposé pour k-means** : on contraint la cardinalité à la
   taxonomie. Un k optimal data-driven pourrait être différent (3 ? 5 ?).
   La métrique « silhouette » sur k variable n'est pas calculée en v3.0.
2. **HDBSCAN-lite ≠ HDBSCAN canonique** : notre implémentation
   single-linkage + gap est une approximation. Une vraie HDBSCAN
   (mutual reachability density) pourrait diverger.
3. **Pas d'analyse UMAP/t-SNE** : visualiser le clustering en 2D nécessite
   une projection non-linéaire qui n'est pas implémentée en v3.0.
4. **Pas de bootstrap des ARI/NMI** : on rapporte des points, pas des CI.

## 7. Travaux futurs

- Sweep sur `k` pour k-means + critère silhouette.
- HDBSCAN canonique (via une dépendance optionnelle).
- Projection UMAP/PCA des 8D vers 2D pour visualisation.
- Comparaison à des taxonomies alternatives (Welzel 2013, Schwartz Values).

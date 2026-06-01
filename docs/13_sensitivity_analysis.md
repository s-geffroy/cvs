# 13 — Analyse de sensibilité

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md](07_ethics_publication_policy.md).

## 1. Sensibilité aux États archétypes (leave-one-out)

### Protocole

Pour chaque civilisation `c_i` et chaque État archétype `s ∈ member_states(c_i)` :

1. Recalculer `μᵢ^viz` et `μᵢ^score` **sans** `s` (mais avec tous les
   autres archétypes core/periphery avec leurs poids habituels).
2. Mesurer la **distance Euclidienne** entre le centroïde original et le
   centroïde recalculé, séparément dans `B_viz` (ℝ²) et `B_score` (ℝ⁶).

### Sortie

`assets/data/empirical/sensitivity_leave_one_out.json` (généré par
`civvec empirical sensitivity`) liste, pour chaque civilisation,
l'archétype dont le retrait produit le plus grand décalage. C'est
l'**État archétype le plus influent** pour cette civilisation — un proxy
de fragilité du centroïde.

### Lecture

- **Décalages typiques < 5 unités Hofstede** : centroïde robuste (la
  civilisation est bien soutenue par un panel diversifié d'archétypes).
- **Décalages > 15 unités** : centroïde **fragile** — la civilisation
  repose sur un petit nombre d'États archétypes. Drapeau de prudence
  pour l'interprétation des résultats.
- **Décalages > 30 unités** : centroïde **non fiable** — révision de la
  liste d'archétypes recommandée.

### Cas attendus

- `western`, `latin_american`, `african` : décalages modérés (large panel).
- `japanese`, `indigenous`, `oceanian` : décalages élevés (couverture
  limitée — flag `low_archetype_coverage`).

## 2. Sensibilité au paramètre `β` du softmax

### Protocole

Pour chaque `β ∈ {0.01, 0.025, 0.05, 0.1, 0.2}` :

1. Recalculer `wₛ` pour tous les États avec coordonnées Hofstede.
2. Mesurer l'**entropie moyenne** de `wₛ` sur le panel.
3. Mesurer le **maximum** moyen de `wₛ` (concentration).
4. Mesurer la **fraction d'États dont la civilisation argmax change** vs
   le β par défaut (0.05).

### Sortie

`assets/data/empirical/sensitivity_beta_sweep.json`.

### Lecture

- **β faible (0.01)** : `wₛ` plus **uniforme** (entropie élevée), affinité
  plus partagée. Bon pour mettre en évidence des États multi-civilisationnels.
- **β élevé (0.2)** : `wₛ` plus **concentré** (entropie basse), affinité
  pointue. Bon pour identifier les États mono-civilisationnels.
- **β par défaut (0.05)** : compromis éditorial.

### Critère de robustesse

Si la **fraction argmax inchangée** entre `β = 0.025` et `β = 0.1` est
supérieure à 80%, le scoring est robuste à ce paramètre dans cette plage.
En dessous, le scoring devient sensible et il faut justifier le choix.

## 3. Sensibilité aux poids hybrides `(α, β, γ)`

### Protocole

Sur une grille simplexe (pas 0.1, `α + β + γ = 1`, `α, β, γ ≥ 0`) :

1. Recalculer la matrice de distances `d_hyb` panel × panel.
2. Calculer le **coefficient de corrélation de rangs de Spearman** entre
   `d_hyb` (poids courants) et `d_hyb` (poids par défaut `0.4, 0.4, 0.2`).
3. Identifier les zones du simplexe où `ρ > 0.95` (équivalence pratique)
   et celles où `ρ < 0.7` (divergence sensible).

### Sortie

`assets/data/empirical/sensitivity_hybrid_weights.json` — pour chaque
point du simplexe, `(α, β, γ)` + `spearman_rho_vs_default`.

### Lecture

- Une vaste zone du simplexe avec `ρ > 0.95` indique que le clustering
  est **robuste** au choix de poids — les utilisateurs peuvent prendre des
  poids différents sans changer drastiquement les voisinages.
- Une zone restreinte indique un scoring **sensible** au choix éditorial.
  C'est un signal de prudence interprétative.

### Hypothèse

Le scoring devrait être robuste pour `(α, β, γ)` proches de l'uniforme
(0.33, 0.33, 0.33), mais sensible aux **coins** (γ=1 = Frobenius seul).

## 4. Sensibilité aux poids `role` (core/periphery/ambiguous)

### Protocole

Le poids `periphery=0.5` du calcul des centroïdes (cf. [doc 08 §4.1](08_civilizational_basis.md)) est éditorial. Cette sensibilité balaye `periphery_weight ∈ {0.0, 0.25, 0.5, 0.75, 1.0}` en gardant `core=1.0, ambiguous=0.0`, et mesure le déplacement Euclidien de chaque centroïde `μᵢ^score` par rapport au défaut.

### Sortie

`assets/data/empirical/sensitivity_role_weights.json`. Pour chaque civilisation et chaque valeur de `periphery_weight`, le déplacement du centroïde par rapport au défaut.

### Lecture

- `max_displacement < 3` unités Hofstede : pondération `0.5` **robuste**.
- `max_displacement > 10` : sensibilité réelle pour certaines civilisations, à examiner.

## 5. Corrélation cross-base `d_viz` ↔ `d_score_euclidean`

### Protocole

Pour toutes les paires d'États avec coordonnées IW + Hofstede complètes, calculer `d_viz(s, t)` et `d_score_euclidean(s, t)` et reporter le coefficient de Spearman.

### Sortie

`assets/data/empirical/sensitivity_cross_base_correlation.json` — un seul scalaire `spearman_rho`.

### Lecture

- `ρ > 0.7` : les deux bases sont **largement redondantes** — IW et Hofstede capturent un signal majoritairement partagé.
- `ρ ∈ [0.4, 0.7]` : **complémentaires** — chaque base apporte de l'information distincte.
- `ρ < 0.4` : **divergence forte** — la critique « mélange pommes/oranges » (cf. [doc 11 §B5](11_critiques_and_responses.md)) prend de l'ampleur.

## 6. Plausibilité des cas connus (confrontation des prédictions doc 09)

[Doc 09 §6](09_civilizational_second_moment.md) énonçait des prédictions pour JPN, FRA, TUR, IND, LBN. Confrontation aux mesures publiées dans `state_moments.json` :

| État | `I1_trace` mesuré | Anisotropie `A(s)` | Prédiction doc 09 | Verdict |
|---|---|---|---|---|
| JPN | ~993 | 0.998 | "basse anisotropie" (État cohérent) | **VIOLÉE** : A très élevée |
| FRA | ~3400 | 0.978 | "modérée" | **VIOLÉE** : A très élevée |
| TUR | ~1440 | 0.979 | "élevée" | Cohérent en A, faible en I1 |
| IND | ~1051 | 0.982 | "modérée" | **VIOLÉE** en A, cohérent en I1 |
| LBN | — | — | non couvert (LBN absent du panel) | — |

### Finding empirique : `A(s)` n'est PAS discriminante

La mesure révèle que **tous les États publiés ont une anisotropie A > 0.97**. Cause mathématique : `M(s)` est une somme pondérée de 11 outer-products (`(μᵢ − xₛ)(μᵢ − xₛ)ᵀ`), chacun de rang 1. Pour la plupart des États, la dispersion des centroïdes dans `B_score` a **une direction dominante** (capturée par le premier axe principal), ce qui fait `λ₁ ≫ λ₆` partout — donc `A ≈ 1` partout.

**Conclusion** : `A(s)` ne discrimine pas entre États « cohérents » et « fracturés ». Le bon indicateur est `I1 = tr(M)` (magnitude totale), qui varie de ~600 (États proches d'un archétype) à ~3500+ (États comme FRA, fortement écartés de tous les archétypes simultanément).

Cette finding est **publiée en l'état** (pas de réécriture rétroactive des prédictions). Elle suggère que :

1. La métaphore mécanique de « fracture orientée » est trompeuse dans ce contexte (cf. [doc 11 §C13](11_critiques_and_responses.md)).
2. `I1` est la statistique scalaire informative dérivée de `M(s)`.
3. Les **directions** `eₖ` restent potentiellement utiles localement, mais leur interprétation globale comme « directions de fracture » est invalidée.

## 7. Limites et travaux futurs

1. **Pas de propagation d'incertitude WVS** : les CI publiés par WVS ne sont pas propagés dans `M(s)`, `wₛ`, `d_hyb`. Travail futur : bootstrap sur les CI WVS pour estimer l'incertitude finale.
2. **Pas d'analyse de stabilité temporelle** : v3.0 utilise WVS wave 7. Comparaison à waves antérieures non implémentée.

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

## 4. Plausibilité des cas connus (confrontation des prédictions doc 09 §6)

Doc 09 §6 (« Lectures appliquées ») énonçait des prédictions pour JPN,
FRA, TUR, IND, LBN. Cette section publie la **confrontation aux
données calculées**.

| État | `I1_trace` mesuré | Anisotropie mesurée | Prédiction respectée ? |
|---|---|---|---|
| JPN | (cf. `state_moments.json`) | (cf.) | À mesurer |
| FRA | (cf.) | (cf.) | À mesurer |
| TUR | (cf.) | (cf.) | À mesurer |
| IND | (cf.) | (cf.) | À mesurer |
| LBN | (non couvert — LBN absent du panel v3.0) | — | — |

**Note** : LBN (Liban) n'est pas dans le panel actuel par manque de données
Hofstede et WVS suffisamment qualifiées. Sa prédiction de « tension
multi-confessionnelle structurelle » reste à valider quand les données
seront disponibles.

Pour les autres États, l'utilisateur peut consulter
`assets/data/state_moments.json` et vérifier `I1_trace` et `anisotropy`.

## 5. Limites et travaux futurs

1. **Pas de propagation d'incertitude WVS** : les CI publiés par WVS ne
   sont pas propagés dans `M(s)`, `wₛ`, `d_hyb`. Travail futur : bootstrap
   sur les CI WVS pour estimer l'incertitude finale.
2. **Pas de sweep sur les pondérations role** (core=1, periphery=0.5,
   ambiguous=0). Travail futur : sweep également ces poids.
3. **Pas d'analyse de stabilité temporelle** : v3.0 utilise WVS wave 7.
   Comparaison à waves antérieures non implémentée.

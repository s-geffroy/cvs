# Base vectorielle `B_vec` — visualisation interactive

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

`B_vec` se compose de deux sous-espaces complémentaires :

- **`B_viz = ℝ²`** — Inglehart-Welzel Cultural Map.
- **`B_score = ℝ⁶`** — Hofstede.

Voir la [méthodologie 08](../methodology/08_civilizational_basis.md) pour le détail.

## Scatter `B_viz` (Traditional ↔ Secular-Rational × Survival ↔ Self-Expression)

<div id="civvec-basis-scatter" style="width: 100%; height: 540px;"></div>

## Radar `B_score` (6 dimensions Hofstede)

Choisissez une civilisation dans la liste déroulante du graphique.

<div id="civvec-basis-radar" style="width: 100%; height: 480px;"></div>

<noscript>
Les graphiques interactifs nécessitent JavaScript. Les données restent téléchargeables :
[`civilization_centroids.json`](../assets/data/civilization_centroids.json) ·
[`state_coordinates.json`](../assets/data/state_coordinates.json).
</noscript>

## Téléchargements

- [`B_viz.json`](../assets/data/B_viz.json) (2 axes)
- [`B_score.json`](../assets/data/B_score.json) (6 axes)
- [`civilization_centroids.json`](../assets/data/civilization_centroids.json) (11 civilisations)
- [`state_coordinates.json`](../assets/data/state_coordinates.json) (193 États)

## Détails techniques

- **Moteur graphique** : [Plotly.js](https://plotly.com/javascript/) 2.35.2 via CDN pinné.
- **Source ellipses** : `Σ_viz` extraites de `state_coordinates.json` (intervalles WVS wave 7).
- **Calcul des centroïdes** : moyenne pondérée par États archétypes, voir
  [`apps/basis_builder/centroids.py`](https://github.com/s-geffroy/cvs/blob/main/apps/basis_builder/centroids.py).

---

[Liste des États](../states/index.md) ·
[Carte interactive](../map/index.md) ·
[Second moment M(s)](../moments/index.md) ·
[Distances](../distances/index.md)

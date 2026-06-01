# Tensions internes des États — vue d'ensemble

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

Chaque État souverain porte un **tenseur de tension civilisationnelle**
`T(s) ∈ ℝ^{6×6}` semi-défini positif, dont les eigenvalues sont les **tensions
principales** et les vecteurs propres les **directions de fracture
civilisationnelle**. Voir la [méthodologie 09](../methodology/09_civilizational_mechanics.md).

## Classement par anisotropie

`A(s) = (λ₁ − λ₆) / λ₁ ∈ [0,1]` mesure la concentration de la tension sur un axe :

- `A → 0` : tensions isotropes (État équilibré dans `B_score`).
- `A → 1` : fracture nette concentrée sur une combinaison Hofstede.

<div id="civvec-tensions-anisotropy" style="width: 100%; height: 520px;"></div>

## Heatmap interactive de `T(s)`

Sélectionnez un État ci-dessous pour visualiser sa matrice 6×6 de tension :

<div id="civvec-tensions-heatmap" style="width: 100%; height: 540px;"></div>

<noscript>
Les graphiques interactifs nécessitent JavaScript. Données téléchargeables :
[`state_tensors.json`](../assets/data/state_tensors.json).
</noscript>

## Téléchargements

- [`state_tensors.json`](../assets/data/state_tensors.json) (63 États)

## Limites assumées

`T(s)` est une **métaphore opérationnelle**, pas une grandeur physique : elle
quantifie l'écart pondéré aux centroïdes civilisationnels dans `B_score`. Sa
validité empirique reste à éprouver — voir [§09 — Mécanique tensorielle](../methodology/09_civilizational_mechanics.md).

---

[Liste des États](../states/index.md) ·
[Base vectorielle](../basis/index.md) ·
[Distances](../distances/index.md)

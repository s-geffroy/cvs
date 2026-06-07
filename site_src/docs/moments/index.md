# Second moment civilisationnel des États — vue d'ensemble

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

Chaque État souverain porte un **second moment civilisationnel pondéré**
`M(s) ∈ ℝ^{6×6}` symétrique semi-défini positif :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ
     = Cov_w(μ; wₛ)  +  (μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σᵢ wₛ[i]
```

où `μ̄ = Σᵢ wₛ[i] · μᵢ` est le **barycentre pondéré** des centroïdes
civilisationnels sous l'affinité `wₛ`. La décomposition sépare la
**dispersion intra-civilisationnelle** (`Cov_w`) du **biais** de l'État
par rapport à son barycentre d'affinité. Voir la
[méthodologie 09 — Second moment civilisationnel](../methodology/09_civilizational_second_moment.md).

!!! info "Renommage v3.0"
    L'objet historiquement appelé « tenseur de tension `T(s)` » est désormais
    publié sous le nom « second moment civilisationnel `M(s)` » : son contenu
    mathématique est identique, mais la dénomination évacue l'ambiguïté
    avec la mécanique des milieux continus. Voir [doc 11 — Critiques et réponses](../methodology/11_critiques_and_responses.md) §C9–C13.

## Classement par anisotropie

`A(s) = (λ₁ − λ₆) / λ₁ ∈ [0,1]` mesure la concentration du second moment sur un axe :

- `A → 0` : dispersion **isotrope** dans `B_score` (État équilibré).
- `A → 1` : dispersion **concentrée sur un axe** (écart dominant sur une combinaison Hofstede).

<div id="civvec-moments-anisotropy" style="width: 100%; height: 520px;"></div>

## Heatmap interactive de `M(s)`

Sélectionnez un État ci-dessous pour visualiser sa matrice 6×6 :

<div id="civvec-moments-heatmap" style="width: 100%; height: 540px;"></div>

<noscript>
Les graphiques interactifs nécessitent JavaScript. Données téléchargeables :
[`state_moments.json`](../assets/data/state_moments.json).
</noscript>

## Téléchargements

- [`state_moments.json`](../assets/data/state_moments.json) (193 États)

## Limites assumées

`M(s)` est une **construction géométrique**, pas une grandeur physique. Elle
quantifie la dispersion pondérée des centroïdes civilisationnels autour de
`xₛ` — une métaphore opérationnelle, pas une dynamique. Sa validité empirique
est testée dans [doc 13 — Sensitivity analysis](../methodology/13_sensitivity_analysis.md)
(LOO sur archétypes) et discutée dans [doc 11 — Critiques et réponses](../methodology/11_critiques_and_responses.md).

---

[Liste des États](../states/index.md) ·
[Base vectorielle](../basis/index.md) ·
[Distances](../distances/index.md)

# Civilizational Vector State (cvs) <span class="cvs-review-badge">v3.0 — rigueur méthodologique étoffée</span>

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées.
    **Il ne doit pas être utilisé pour classer des individus réels.**

## Pitch

`cvs/` est un pipeline Python bayésien produisant pour chaque **État souverain** un
**vecteur d'affiliation civilisationnelle** à partir de **sources publiques uniquement**
(World Values Survey wave 7, Hofstede 2010, Inglehart-Welzel 2005/2010, Natural Earth,
geoBoundaries — jamais GADM).

Le projet repose sur **deux bases interdépendantes** :

- **B_doc** (documentaire) — Huntington (1996), Inglehart-Welzel (2005, 2010), Hofstede (2010), WVS wave 7.
- **B_vec** (vectorielle) — `B_viz = ℝ²` (Inglehart-Welzel : TS, SE) ⊕ `B_score = ℝ⁶` (Hofstede : PDI, IDV, MAS, UAI, LTO, IVR).

Étendu par :

- **Second moment civilisationnel** `M(s) ∈ ℝ^{6×6}` (PSD), renommé en v3.0 depuis l'ancien « tenseur de tension `T(s)` » pour évacuer le *physics envy* (cf. [doc 11](methodology/11_critiques_and_responses.md)).
- **Algèbre des distances** : `d_viz`, `d_score^M_intra`, `d_w^W` (Wasserstein-2), `d_M_F`, `d_hyb` hybride.
- **Validation empirique** : corrélations `wₛ` ↔ Pew/WGI/FSI ([doc 12](methodology/12_empirical_validation.md)).
- **Analyse de sensibilité** : LOO sur archétypes, sweep β, sweep `(α, β, γ)` ([doc 13](methodology/13_sensitivity_analysis.md)).
- **Baseline non-supervisé** : k-means + HDBSCAN-lite vs taxonomie ([doc 14](methodology/14_baseline_unsupervised.md)).

## Statut de cette publication

**v3.0** : le site couvre la méthodologie complète, la taxonomie hyper-détaillée, les
sources, les schémas, les pages États, la carte interactive, les seconds moments, les
distances, **et** une couche de **validation empirique + sensibilité + baseline** + une
politique éthique étoffée. Cette version répond aux critiques anticipées (cf. [doc 11](methodology/11_critiques_and_responses.md)).

## Navigation

- **Méthodologie** ([index](methodology/index.md)) — `00..15`, dont :
    - [`08_civilizational_basis`](methodology/08_civilizational_basis.md)
    - [`09_civilizational_second_moment`](methodology/09_civilizational_second_moment.md)
    - [`10_distance_algebra`](methodology/10_distance_algebra.md)
    - [`11_critiques_and_responses`](methodology/11_critiques_and_responses.md)
    - [`12_empirical_validation`](methodology/12_empirical_validation.md)
    - [`13_sensitivity_analysis`](methodology/13_sensitivity_analysis.md)
    - [`14_baseline_unsupervised`](methodology/14_baseline_unsupervised.md)
    - [`15_glossary`](methodology/15_glossary.md)
- [États](states/index.md) — fiche pour chaque ISO3 couvert.
- [Carte](map/index.md) — choropleth MapLibre.
- [Base vectorielle](basis/index.md) — Plotly B_viz + B_score.
- [Moments M(s)](moments/index.md).
- [Distances](distances/index.md).
- [Taxonomie](taxonomy/index.md) — 11 civilisations hyper-détaillées avec sous-clusters et controverses.
- [Sources & bibliographie](sources/index.md).
- [Schémas JSON v3](schemas/index.md).
- [Politique ADM1 préparée](adm1_policy.md) — non activée en V1.
- [Éthique de publication](ethics.md).
- [Guide de relecture](review/index.md) — comment ouvrir une issue/PR.

## Liens externes

- Dépôt : [`s-geffroy/cvs`](https://github.com/s-geffroy/cvs)
- Issues : [github.com/s-geffroy/cvs/issues](https://github.com/s-geffroy/cvs/issues)

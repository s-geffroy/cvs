# Civilizational Vector State (cvs) <span class="cvs-review-badge">Phase 1b — en relecture</span>

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

- **Mécanique tensorielle** : tenseur de tension `T(s) ∈ ℝ^{6×6}` analogue au tenseur des contraintes en milieux continus.
- **Algèbre des distances** : `d_viz`, `d_score^M` (Mahalanobis), `d_w^W` (Wasserstein-2), `d_T` (Frobenius), `d_hyb` hybride.

## Statut de cette publication

**Phase 1b** : le site contient pour le moment **la méthodologie complète, la taxonomie
hyper-détaillée, les sources, les schémas et la politique éthique**. Il est publié
**délibérément tôt** pour permettre aux relecteurs externes d'auditer la doc et la taxo
avant la stabilisation des États (Phase 2).

Ne sont **pas encore publiés** : pages États, carte interactive, vue B_vec interactive
(prévus Phase 2).

## Navigation

- [Méthodologie](methodology/index.md) — `00..10`, dont [`08_civilizational_basis`](methodology/08_civilizational_basis.md), [`09_civilizational_mechanics`](methodology/09_civilizational_mechanics.md), [`10_distance_algebra`](methodology/10_distance_algebra.md).
- [Taxonomie](taxonomy/index.md) — 11 civilisations hyper-détaillées avec sous-clusters et controverses.
- [Sources & bibliographie](sources/index.md).
- [Schémas JSON v2](schemas/index.md).
- [Politique ADM1 préparée](adm1_policy.md) — non activée en V1.
- [Éthique de publication](ethics.md).
- [Guide de relecture](review/index.md) — comment ouvrir une issue/PR.

## Liens externes

- Dépôt : [`s-geffroy/cvs`](https://github.com/s-geffroy/cvs)
- Issues : [github.com/s-geffroy/cvs/issues](https://github.com/s-geffroy/cvs/issues)

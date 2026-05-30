# Politique ADM1 — préparée, non active en V1

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées.
    Il ne doit pas être utilisé pour classer des individus réels.

!!! info "Statut"
    ADM1 (sous-divisions administratives de premier ordre : régions, états fédérés, provinces)
    est **architecturalement anticipé** mais **désactivé** en V1.

## Pourquoi anticiper ADM1 sans l'activer

1. **Schémas figés tôt** — un schéma `adm1_profile.v2.schema.json` est versionné dès aujourd'hui
   pour éviter une rupture de contrat lors de l'activation future.
2. **Géométries prêtes** — geoBoundaries ADM1 est versionné dans `data_sources/geoboundaries/adm1/`,
   auditable mais non utilisé par le pipeline de scoring.
3. **CLI signale clairement** — `civvec score --unit-type adm1 ...` retourne `prepared_not_active`
   avec lien vers cette page.
4. **Cohérence B_vec** — le schéma v2 inclut des slots `x_viz` et `x_score` pour que l'activation
   future ne nécessite que la population des coordonnées.

## Pourquoi pas en V1

- Couverture sous-nationale WVS/Hofstede très inégale.
- Risque éthique accru (profilage régional plus susceptible d'être détourné).
- Validation des États souverains à terminer d'abord.

## Critères de levée

ADM1 ne sera activé que lorsque :

- (a) ≥20 États V1 sont stabilisés et publiés,
- (b) une politique de publication ADM1 est validée éthiquement,
- (c) la couverture Hofstede/IW sub-nationale est documentée par juridiction.

## Référence interne

Cf. [`docs/04_adm1_preparation_policy.md`](methodology/04_adm1_preparation_policy.md).

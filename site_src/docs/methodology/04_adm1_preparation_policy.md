# 04 — Politique ADM1 préparée

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md`](07_ethics_publication_policy.md).

## 1. État actuel — ADM1 *prepared, not active*

Les sorties à l'échelle ADM1 (régions sub-nationales) sont **architecturalement préparées** mais **pas activées** dans la v3.0.

Concrètement :

- Schémas définis : `schemas/adm1_profile.v2.schema.json`.
- Géométries versionnées : `data_sources/geoboundaries/adm1/` (à terme).
- Hook CLI : `civvec score --unit-type adm1 <iso3>` retourne `{"error": "prepared_not_active", "see": "docs/04_adm1_preparation_policy.md"}` avec code de sortie 2.
- Notes de migration documentées (cf. §4 ci-dessous).

## 2. Stratégie des sources géométriques

| Source | Rôle | Licence | Statut publication |
|---|---|---|---|
| **geoBoundaries** | Source primaire ADM1 lorsque activée. | CC-BY 4.0. | **Autorisée** en publication. |
| **Natural Earth** | Rendu et fallback léger. | Domaine public. | **Autorisée** en publication. |
| **GADM** | Fallback académique restreint. | Restrictive : usage non-commercial, **pas de redistribution**. | **Interdite** en publication. |

## 3. Politique GADM stricte

**GADM ne doit en aucun cas être publié** par `cvs/` :

- Usage interne **seulement** pour recherche, jamais redistribué.
- Pas de redistribution sous quelque forme (GeoJSON, tile, PMTiles, vector, raster).
- Pas d'usage commercial.
- Toute trace de provenance GADM doit être **trackée** et scannée par `apps/site_builder/guards.py:scan_directory_for_gadm`.
- Test obligatoire : `tests/test_site_build.py:test_no_gadm_geometry_in_published_geojson` doit passer.

Les seules sources autorisées en publication sont **Natural Earth** et **geoBoundaries**. Cf. `apps/site_builder/guards.py:ALLOWED_GEOMETRY_SOURCES`.

## 4. Critères de levée du *prepared_not_active*

L'activation des sorties ADM1 suppose la validation cumulative :

1. **≥ 20 États V1 stabilisés** avec corrélations externes positives (doc 12 ARI > 0.4 ou similaire).
2. **Politique éthique ADM1 validée** par relecture publique sur le canal Issues du dépôt — incluant les risques de profiling régional, de stigmatisation, de récupération politique.
3. **Couverture Hofstede et IW sub-nationale** documentée pour au moins 5 États-pilotes (par exemple INE en Espagne pour les communautés autonomes ; pas de proxy national répété au niveau régional).
4. **Workflow GitHub Actions** étendu pour publier les artefacts ADM1 séparément, avec scan GADM strict.

Aucune de ces conditions n'est remplie en v3.0. L'activation ADM1 reste donc **différée**.

## 5. Architecture restée disponible

Pour faciliter le futur déblocage :

- Le schéma `state_profile.v2.schema.json` accepte un champ optionnel `unit_type ∈ {"state", "adm1"}` (forcé à `"state"` en V1).
- Les pipelines `centroids` et `projector` sont indépendants de `unit_type` — ils traitent des records typés.
- Le CLI accepte `--unit-type adm1` mais court-circuite avec `prepared_not_active`.

## 6. Décisions ouvertes lors de l'activation future

Quand ADM1 sera activé, plusieurs choix de design devront être faits :

- Granularité de la civilisation par ADM1 (héritée de l'État ? recalculée ?).
- Pondération des sources (Hofstede national vs Hofstede sub-national si disponible).
- Politique de fusion vs séparation des ADM1 (e.g. Catalogne séparée de l'Espagne ou non).
- Frontières d'éthique : éviter la stigmatisation de régions particulières.

Ces choix seront documentés dans une révision future de cette politique.

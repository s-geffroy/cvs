# 08 — Base civilisationnelle : synthèse hybride et coordonnées vectorielles

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md](07_ethics_publication_policy.md).

Le projet `cvs/` repose sur **deux bases interdépendantes** qui co-évoluent et se valident mutuellement.

| Base | Nature | Rôle |
|---|---|---|
| **B_doc** (documentaire) | Bibliographie + taxonomie sourcée | Ce sur quoi le modèle s'appuie |
| **B_vec** (vectorielle) | Espace mathématique ℝ² ⊕ ℝ⁶ | Comment le modèle représente |

Aucune des deux n'est dérivée de l'autre. Chaque coordonnée dans `B_vec` porte un `citation_ids[]` pointant vers `B_doc.bibliography`, et chaque entrée de `B_doc` qui décrit une civilisation porte ses coordonnées calculées dans `B_vec` (`mu_viz`, `mu_score`).

## 1. Pourquoi une synthèse hybride Huntington + Inglehart-Welzel + Hofstede + WVS ?

### 1.1 Huntington seul est insuffisant

Huntington (1996) fournit un **vocabulaire civilisationnel** (Western, Orthodox, Islamic, Sinic, Hindic, Japanese, Latin American, African) largement repris dans les sciences sociales, mais :

- **Non opérationnalisé** : aucun ensemble de coordonnées numériques associé aux civilisations.
- **Statique** : ignore l'évolution des valeurs (laïcisation, post-matérialisme).
- **Réductionniste** : critique de Sen (2006) sur la pluralité des identités.

### 1.2 Inglehart-Welzel fournit l'axiomatique empirique

L'analyse factorielle Inglehart-Welzel (2005, 2010) sur 100+ pays / 6 vagues WVS révèle **deux dimensions latentes** qui capturent ~70% de la variance des valeurs culturelles :

- **TS** : Traditional ↔ Secular-Rational (religion, famille, autorité).
- **SE** : Survival ↔ Self-Expression (sécurité matérielle vs autonomie/diversité).

Ces deux axes définissent **`B_viz = ℝ²`** — la base de visualisation primaire.

### 1.3 Hofstede fournit la résolution fine

Les 6 dimensions Hofstede (PDI, IDV, MAS, UAI, LTO, IVR) sont calibrées empiriquement sur des populations de travailleurs IBM (1967-1973, étendues 1990s-2010s) et **postulent** une indépendance dimensionnelle par construction factorielle. **L'orthogonalité empirique n'est pas vérifiée** sur les valeurs contemporaines : MAS et IDV sont notoirement corrélées (cf. McSweeney 2002, Schmitz & Weber 2014), UAI a une faible variance expliquée. La v3.0 étiquette donc l'orthogonalité comme **postulée**, pas **mesurée** (voir [doc 11](11_critiques_and_responses.md) section A2, et la métrique `d_score_mahalanobis_intra` introduite pour pondérer les axes selon leur variance intra-civilisationnelle — cf. [doc 10](10_distance_algebra.md)).

Ces 6 axes définissent **`B_score = ℝ⁶`** — la base de scoring fin.

### 1.4 WVS wave 7 fournit l'actualisation

La vague 7 (2017-2022) du World Values Survey publie les coordonnées IW actuelles pour la majorité des pays, sous licence CC-BY.

## 2. Tableau de correspondance Huntington ↔ Inglehart-Welzel ↔ Hofstede

| Huntington | IW quadrant typique | Hofstede archétypes (PDI/IDV/MAS/UAI/LTO/IVR) |
|---|---|---|
| Western | TS+ / SE+ | USA, GBR, FRA, DEU, NLD, SWE, CAN, AUS |
| Orthodox | TS≈0 / SE− | RUS, UKR, ROU, BGR, GRC, SRB |
| Islamic | TS− / SE− | TUR, IRN, EGY, SAU, IDN, PAK |
| Sinic | TS+ / SE− | CHN, SGP, TWN, VNM (HKG) |
| Hindic | TS− / SE− | IND |
| Japanese | TS++ / SE≈0 | JPN |
| Buddhist (extension) | TS≈0 / SE≈0 | THA, KOR, MMR, MNG |
| Latin American | TS− / SE+ | BRA, MEX, ARG, CHL, COL, PER |
| African | TS−− / SE− | NGA, ZAF, KEN, GHA, ETH |
| Indigenous (extension) | TS−− / SE− | (faible couverture — cf. §3) |
| Oceanian (extension) | TS+ / SE+ | NZL, AUS-partiel, FJI |

## 3. Extensions documentées au-delà de Huntington

### 3.1 Buddhist

Huntington classait la « Buddhist civilization » comme **non clairement délimitée** (notion frontière entre Sinic et Hindic). Ici elle est instanciée pour intégrer THA, KOR (controverse Sinic/Buddhist), MMR, MNG.

- Sources : Reat (1994), Berkwitz (2010) — non engagées formellement, mention bibliographique.

### 3.2 Indigenous

Huntington n'inclut **pas** les peuples autochtones comme civilisation à part entière. L'inclusion ici suit :

- Smith (2012), *Decolonizing Methodologies* — épistémologie indigène.
- UN Permanent Forum on Indigenous Issues — reconnaissance institutionnelle.

**Drapeau** `low_archetype_coverage: true` car (a) aucun État souverain n'est purement indigène, (b) BOL/ECU/PER présentent une stratification où l'identité indigène coexiste avec l'identité latino-américaine.

### 3.3 Oceanian

Hau'ofa (1994) « Our Sea of Islands » articule une identité pacifique distincte de la classification Western (NZL, AUS-partiel).

**Drapeau** `low_archetype_coverage: true` car peu de données Hofstede pour les micro-États du Pacifique.

### 3.4 Règle de désambiguïsation entre civilisations chevauchantes

Pour les États dont l'identité chevauche plusieurs catégories, la v3.0 publie une **règle de priorité explicite** :

| Cas | Décision | Justification |
|---|---|---|
| KOR | `sinic` core, `buddhist` periphery | Influence sinique structurelle (caractères chinois historiques, confucianisme) ; bouddhisme = minorité religieuse mais non structurellement définissante. |
| THA | `buddhist` core, `sinic` periphery | Bouddhisme theravāda = identité dominante ; influences siniques historiques mais non structurelles. |
| MMR | `buddhist` core | Bouddhisme theravāda dominant, identité bouddhiste affirmée. |
| MNG | `buddhist` core, `sinic` periphery | Bouddhisme tibétain dominant ; héritage historique sinique périphérique. |
| BOL | `latin_american` core, `indigenous` periphery | Identité latino-américaine officielle ; stratification indigène significative mais non dominante. |
| ECU | `latin_american` core, `indigenous` periphery | Idem BOL. |
| PER | `latin_american` core, `indigenous` periphery | Idem BOL. |
| NZL | `western` core, `oceanian` periphery | Anglo-saxon dominant ; identité polynésienne secondaire (māori). |
| AUS | `western` core, `oceanian` periphery | Idem NZL. |
| FJI | `oceanian` core | Petit État, identité polynésienne primaire. |
| TUR | `islamic` core, `western` ambiguous | Pays musulman majoritaire mais avec une affiliation européenne contestée — `ambiguous_cases` documenté. |
| RUS | `orthodox` core | Identité orthodoxe russe affirmée ; pas de chevauchement structurel. |
| IRN | `islamic` core (chiite) | Identité chiite spécifique, marquée. |

Pour les cas restant **véritablement ambigus** après application de cette règle, les États sont listés dans `taxonomies/macro_civilizations.v2.json:ambiguous_cases` de la civilisation où ils sont **moins fortement** rattachés — ce qui les laisse présents dans la documentation sans influencer le centroïde.

## 4. Formules de projection (lien vers B_vec)

### 4.1 Centroïdes de civilisation

Pour la civilisation `c_i` avec États-membres `S_i = {s_1, ..., s_n}` et leurs poids `α_j` :

```
μ_i^viz   = (Σ_j α_j · x_j^viz) / (Σ_j α_j)
Σ_i^viz   = (Σ_j α_j · (x_j^viz - μ_i^viz)(x_j^viz - μ_i^viz)^T) / (Σ_j α_j)

μ_i^score = (Σ_j α_j · x_j^score) / (Σ_j α_j)
σ_i^score[k] = sqrt((Σ_j α_j · (x_j^score[k] - μ_i^score[k])²) / (Σ_j α_j))   pour k=1..6
```

Pondération par défaut : `α_j = 1` pour les États core, `α_j = 0.5` pour periphery, `α_j = 0` pour ambiguous (exclus du centroïde mais membres listés).

### 4.2 Vecteur d'affinité civilisationnelle (dérivé)

Pour un État `s` avec `x_s^score ∈ ℝ⁶` :

```
d_i = ||x_s^score - μ_i^score||₂           # Distance Euclidienne aux 11 centroïdes
w_s[i] = exp(-β·d_i) / Σ_j exp(-β·d_j)     # Softmax inverse-distance
```

Paramètre `β = 0.05` par défaut (échelle Hofstede 0-100, distances typiques 30-80). Le vecteur `w_s ∈ Δ¹⁰` est donc **dérivé** de la géométrie, plutôt qu'estimé indépendamment comme dans v1.

## 5. Limites assumées

1. **Hofstede couvre ~100 pays** : ETH, FJI, et plusieurs micro-États manquent ou sont imputés depuis des proxies régionaux. Procédure d'imputation explicite : `np.nanmean` sur les axes disponibles, flag `coverage: imputed` posé sur l'État, propagation jusqu'aux outputs. Drapeau `imputed` dans `state_coordinates.json`.
2. **IW manque pour certains pays africains/asiatiques** : utilisation des waves antérieures (5, 6) si wave 7 manque. Drapeau `iw_coverage` est positionné à `missing` quand aucune wave n'est disponible.
3. **Les axes IW ne sont pas strictement orthogonaux** en wave 7 (corrélation ~0.15) — orthogonalité **postulée par construction factorielle**, non vérifiée empiriquement. La v3.0 corrige l'étiquetage trompeur de la v2.0 (`empirical_orthogonal_by_construction` → `postulated_orthogonal_not_empirically_verified`).
4. **Hofstede et IW datent de différentes vagues** : pas de simultanéité temporelle stricte. Hofstede 2010 (consolidation 2015) vs WVS wave 7 (2017-2022). Limite reconnue, non corrigeable en V1.
5. **Les centroïdes sont sensibles au choix d'États archétypes** — sensibilité quantifiée par leave-one-out dans [doc 13](13_sensitivity_analysis.md). La UI Streamlit permet d'itérer interactivement.
6. **Le poids periphery=0.5 est éditorial** : justification non empirique. Sensibilité à ce choix testée dans [doc 13](13_sensitivity_analysis.md). Valeurs alternatives (0.25, 0.75) discutées.

## 6. Cohérence garantie

Tests automatiques (`tests/test_documentary_basis.py`, `test_vector_basis.py`, `test_bases_coupling.py`) garantissent :

- Toute civilisation a ≥1 citation_id (B_doc).
- Toute citation_id résout vers la bibliographie racine.
- Toute civilisation a ≥3 États archétypes.
- Tout État archétype a des données IW ou Hofstede.
- Tout centroïde est dans le domaine.
- Tout vecteur d'affinité est un simplexe valide.
- **Toute civilisation porte simultanément `citation_ids[]` ET `mu_viz` + `mu_score`** (couplage B_doc ↔ B_vec).

## 7. Versionnement

- `taxonomies/macro_civilizations.v2.json` : version `2.0.0`.
- `packages/civvec_core/basis/B_viz.json` : version `2.0.0`.
- `packages/civvec_core/basis/B_score.json` : version `2.0.0`.
- Toute modification d'un centroïde, d'une bibliographie ou d'un État archétype incrémente la version mineure (`2.x.0`) et est consignée dans `CHANGELOG.md.

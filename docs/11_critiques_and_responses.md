# 11 — Critiques académiques et réponses du projet

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md](07_ethics_publication_policy.md).

Cette page anticipe les **critiques attendues** d'un projet qui hybride
Huntington, Inglehart-Welzel et Hofstede pour produire un scoring
civilisationnel des États souverains. Pour chaque critique, on **cite la
source académique**, on **mesure l'impact** sur le projet, et on **expose
la réponse** (correction faite, limite assumée, ou travail futur).

Structure des sections :

- **A. Critiques sur les sources elles-mêmes** (Huntington, Hofstede, IW, WVS).
- **B. Critiques sur l'opérationnalisation hybride** (mélange, centroïdes, softmax, extensions).
- **C. Critiques mathématiques sur `M(s)`** (formerly `T(s)`).
- **D. Critiques sur l'algèbre des distances** (Mahalanobis, hybride, Wasserstein).
- **E. Critiques épistémologiques et éthiques**.
- **F. Critiques sur la rigueur statistique**.
- **G. Critiques structurelles sur la documentation**.

---

## A. Critiques sur les sources elles-mêmes

### A1. Huntington (1996) reproduit un essentialisme culturel

**Critique** : *Le Clash of Civilizations* a été critiqué pour réductionnisme,
déterminisme culturel, et ignorance de la pluralité interne. Le projet
hérite des 8 macro-civilisations huntingtoniennes en les présentant comme
« vocabulaire » — ce qui est un cheval de Troie pour les présupposés.

**Sources** :

- Sen, A. (2006). *Identity and Violence: The Illusion of Destiny*. W.W. Norton.
- Said, E. (2001). « The Clash of Ignorance ». *The Nation*, 22 oct. 2001.
- Fox, J. (2001). « Civilizational, Religious, and National Explanations
  for Ethnic Rebellion in the Post-Cold War Middle East ». *Jewish Political
  Studies Review*, 13(1-2), 177-204. → **réfute empiriquement les « fault lines »**.
- Berman, P. (2003). *Terror and Liberalism*. W.W. Norton.
- Gurr, T. R. (1994). « Peoples Against States: Ethnopolitical Conflict
  and the Changing World System ». *International Studies Quarterly*, 38(3), 347-377.
  → données qui contredisent la prédominance des conflits inter-civilisationnels.

**Impact** : les 11 catégories `cvs/` sont *informées* par Huntington (8 + 3
extensions). Si Huntington est faux, la taxonomie l'est en partie.

**Réponse du projet** :

1. **Pas de prédiction politique** : `cvs/` ne prédit pas les conflits ; il
   décrit une géométrie culturelle moyenne (cf. `M(s)` §7 limite 1).
2. **Désessentialisation par les extensions** : `indigenous`, `oceanian`,
   `buddhist` ne sont pas chez Huntington — leur inclusion casse le canon
   huntingtonien (cf. [doc 08 §3](08_civilizational_basis.md)).
3. **Sources empiriques séparées** : la géométrie réelle vient
   d'Inglehart-Welzel et Hofstede, pas de Huntington. Huntington fournit
   les **étiquettes**, pas les **coordonnées**.
4. **Test baseline** : [doc 14](14_baseline_unsupervised.md) compare la
   taxonomie Huntington-informée à un clustering non-supervisé (k-means +
   HDBSCAN) sur WVS+Hofstede brut. Si la taxonomie ne bat pas un baseline
   data-driven, c'est un signal majeur — explicitement publié.
5. **Limite admise** : voir [doc 07](07_ethics_publication_policy.md)
   §« Restrictions d'usage » — le scoring ne doit pas être utilisé pour
   justifier des récits identitaires ou de conflit de civilisations.

### A2. Hofstede a été démoli méthodologiquement

**Critique** : les 6 dimensions Hofstede sont :

- **Biais d'échantillon** : population IBM masculine, technique, années
  1967–1973, dans des branches multinationales — non-représentative de la
  population générale du pays.
- **Assimilation nation = culture** : un État souverain n'a pas une culture
  uniforme.
- **Instabilité des dimensions** : MAS et IDV sont **fortement corrélées**,
  UAI a une faible variance expliquée.
- **Faible orthogonalité empirique** : l'orthogonalité est *postulée*, pas
  vérifiée sur les données contemporaines.

**Sources** :

- McSweeney, B. (2002). « Hofstede's model of national cultural differences
  and their consequences: A triumph of faith—a failure of analysis ». *Human
  Relations*, 55(1), 89-118.
- Baskerville, R. F. (2003). « Hofstede never studied culture ». *Accounting,
  Organizations and Society*, 28(1), 1-14.
- Schmitz, L. & Weber, W. (2014). « Are Hofstede's Dimensions Valid? ».
  *Interculture Journal*, 13(22).
- Minkov, M. & Hofstede, G. (2012). « Is National Culture a Meaningful
  Concept? Cultural Values Delineate Homogeneous National Clusters of
  In-Country Regions ». *Cross-Cultural Research*, 46(2), 133-159.
  → Minkov lui-même reconnait des limites.

**Impact** : si Hofstede est instable, `B_score = ℝ⁶` est instable. Les
centroïdes `μᵢ^score` héritent du biais IBM.

**Réponse du projet** :

1. **Renoncement à l'affirmation d'orthogonalité empirique** : la v3.0
   corrige `B_score.json` et [doc 08 §1.3](08_civilizational_basis.md)
   pour étiqueter l'orthogonalité comme **postulée par construction
   factorielle**, **non vérifiée sur les valeurs contemporaines**. Tout
   utilisateur souhaitant l'orthogonalité doit recourir à un PCA explicite
   sur les données publiées.
2. **Mahalanobis intra-civilisationnelle** : la v3.0 ajoute
   `d_score_mahalanobis_intra` qui pondère les axes par leur dispersion
   intra-civ pondérée — cela corrige la critique de **commensurabilité**.
   L'ancienne version (`d_score_mahalanobis_centroids`) reste publiée pour
   comparaison (cf. [doc 10](10_distance_algebra.md)).
3. **Bornage des conclusions** : aucun usage politique ou prédictif n'est
   revendiqué. Hofstede fournit une géométrie nuancée mais imparfaite,
   utilisée comme **structure de représentation**, pas comme **vérité
   anthropologique**.
4. **Couverture limitée admise** : ~100 pays couverts. Les États sans
   données Hofstede sont marqués `coverage: missing` ou `imputed`
   (cf. [doc 08 §5.1](08_civilizational_basis.md)).

### A3. Inglehart-Welzel est eurocentrique et a dérivé dans le temps

**Critique** : les axes TS et SE sont calibrés sur 6 vagues WVS hétérogènes,
et la dérive temporelle a été montrée. L'axe TS suggère un *télos*
modernisateur (laïcisation comme progression).

**Sources** :

- Beugelsdijk, S., Welzel, C. (2018). « Dimensions and Dynamics of National
  Culture: Synthesizing Hofstede With Inglehart ». *Journal of Cross-Cultural
  Psychology*, 49(10), 1469-1505. → analyse comparative + dérive.
- Welzel, C. (2013). *Freedom Rising: Human Empowerment and the Quest for
  Emancipation*. Cambridge University Press. → réponse aux critiques mais
  reste sur le télos.

**Impact** : `B_viz = ℝ²` repose sur des axes qui ne sont pas stables et
qui portent une orientation normative implicite.

**Réponse du projet** :

1. **Vague unique utilisée** : `cvs/` n'utilise que **WVS wave 7 (2017-2022)**,
   évitant le mélange de vagues. La dérive est donc figée à une date.
2. **Pas d'agrégation temporelle** : aucun État n'est positionné sur des
   moyennes inter-vagues.
3. **Étiquetage neutre des axes** : la doc 08 décrit T-S comme « religion,
   famille, autorité » et S-E comme « sécurité matérielle vs autonomie/
   diversité » — sans connotation normative.
4. **Mise à jour planifiée** : si la wave 8 publie, la base sera reconstruite.
5. **Limite admise** : voir [doc 08 §5.3](08_civilizational_basis.md)
   sur la corrélation résiduelle ~0.15 entre axes en wave 7.

### A4. WVS souffre de biais d'échantillonnage différentiels

**Critique** : les enquêtes WVS varient en taille d'échantillon, en
représentativité rurale/urbaine, en langue de l'enquête, et en taux de
réponse selon pays. Les coordonnées IW publiées masquent cette hétérogénéité.

**Sources** :

- Brunkert, L., Kruse, S., Welzel, C. (2019). « A Tale of Culture-Bound
  Regime Evolution ». *Comparative Sociology*, 18(5-6), 581-613.
- WVS Methodological Documentation (haerpfer et al. 2022) — métadonnées
  publiées par enquête.

**Impact** : `xₛ^viz` et son ellipse `Σₛ^viz` peuvent sous-estimer l'incertitude
réelle.

**Réponse du projet** :

1. **Ellipses 80% explicites** : `state_coordinates.json` publie l'ellipse
   `Σₛ^viz` dérivée des intervalles WVS. C'est imparfait mais explicite.
2. **Pas de propagation d'incertitude vers `M(s)`** — limite admise
   (cf. [doc 13](13_sensitivity_analysis.md) §« Travaux futurs »).
3. **Flag `data_quality.iw_coverage`** marque les imputations depuis
   waves antérieures ou proxies régionaux.

---

## B. Critiques sur l'opérationnalisation hybride

### B5. Mélanger `B_viz` (IW 2D) et `B_score` (Hofstede 6D) c'est mélanger pommes et oranges

**Critique** : IW et Hofstede sont issus de populations, méthodologies, et
époques **différentes**. Les juxtaposer dans un même pipeline opérationnel
suppose une commensurabilité qui n'est pas démontrée.

**Réponse du projet** :

1. **Séparation explicite** : `B_viz` et `B_score` sont **deux sous-espaces
   non-mélangés**. Aucune opération vectorielle entre les deux n'est faite.
2. **Rôles différents** : `B_viz` = visualisation 2D primaire ; `B_score` =
   scoring et tenseur. La doc 08 le précise.
3. **Non-simultanéité admise** : voir [doc 08 §5.4](08_civilizational_basis.md).
4. **Comparaison empirique** : la corrélation de Spearman entre `d_viz` et
   `d_score_euclidean` sur toutes les paires d'États du panel est publiée
   dans [doc 13 §5](13_sensitivity_analysis.md) (artefact
   `assets/data/empirical/sensitivity_cross_base_correlation.json`). Une
   valeur intermédiaire indiquerait des bases complémentaires ; une valeur
   faible confirmerait la critique de divergence pommes/oranges.

### B6. Le poids `α = 0.5` pour les États periphery est arbitraire

**Critique** : pondération par défaut `core=1, periphery=0.5, ambiguous=0`
n'est pas justifiée. Aucune sensibilité publiée.

**Réponse du projet** :

1. **Sensibilité publiée** : [doc 13 §4](13_sensitivity_analysis.md) balaye
   `periphery_weight ∈ {0.0, 0.25, 0.5, 0.75, 1.0}` et publie le déplacement
   Euclidien de chaque centroïde par rapport au défaut dans
   `assets/data/empirical/sensitivity_role_weights.json`.
2. **Justification doc 08 §4.1** : `0.5` est documenté comme **valeur
   éditoriale** dans [doc 08 §4.1](08_civilizational_basis.md),
   pas comme estimation calibrée.
3. **Manipulable** : la UI Streamlit `1_Documentary_Basis.py` permet
   d'itérer sur les pondérations.

### B7. Le softmax inverse-distance avec `β = 0.05` est ad-hoc

**Critique** : aucune justification empirique de `β = 0.05`. Le choix
détermine la **netteté** du vecteur d'affinité — un `β` plus faible donne
des distributions plus uniformes, plus élevé des distributions plus pointues.

**Réponse du projet** :

1. **Sweep publié** : [doc 13 §2](13_sensitivity_analysis.md) calcule
   `wₛ` pour `β ∈ {0.01, 0.025, 0.05, 0.1, 0.2}` et publie l'évolution de
   l'entropie moyenne et de la distance entre vecteurs d'affinité.
2. **Justification heuristique** : la doc 08 §4.2 indique l'échelle Hofstede
   (0-100, distances typiques 30-80) et `β = 0.05` qui donne des poids
   typiquement étalés entre 0.05 et 0.30 sur les 11 civilisations.
3. **Calibration empirique** : non revendiquée — voir
   [doc 05 (Scoring Calibration)](05_scoring_calibration.md).

### B8. Les extensions Buddhist/Indigenous/Oceanian chevauchent les catégories existantes

**Critique** : KOR appartient autant au Sinic qu'au Buddhist. BOL/ECU/PER
ont une identité indigène superposée à latin_american. La règle de
désambiguïsation n'existe pas formellement.

**Réponse du projet** :

1. **Désambiguïsation explicite** : la v3.0 ajoute une **règle de
   priorité** dans [doc 08 §3.4 (nouveau)](08_civilizational_basis.md)
   pour chaque ISO3 ambigu.
2. **Liste des cas ambigus** : `taxonomies/macro_civilizations.v2.json`
   porte le champ `ambiguous_cases[]` par civilisation où chaque ISO3
   contesté est documenté avec sa résolution.
3. **Affinité multi-civilisationnelle** : le vecteur `wₛ` capture
   précisément cette ambiguïté — un État ambigu aura `wₛ` étalé sur
   plusieurs civilisations, pas concentré sur une seule.

---

## C. Critiques mathématiques sur `M(s)` (anciennement `T(s)`)

### C9. *Physics envy* du « tenseur de contrainte »

**Critique** : nommer la matrice `T(s)` « tenseur de tension civilisationnelle »
crée une analogie suggestive (contrainte mécanique, fracture) sans
justification physique. C'est du *physics envy* (Smith 2009).

**Sources** :

- Smith, J. (2009). « Physics envy ». *Foreign Policy*. → critique générique
  des sciences sociales empruntant le vocabulaire de la mécanique.

**Réponse v3.0 — fix appliqué** :

- **Renommage** : `T(s)` → `M(s)` (second moment civilisationnel).
- L'analogie mécanique reste comme **remarque pédagogique secondaire** mais
  ne porte plus le nom.
- Le mot « anisotropie » est conservé car techniquement correct (mesure de
  concentration directionnelle d'une matrice 6×6 PSD), mais sans
  connotation de fracture.
- Cf. [doc 09 §1, note v3.0](09_civilizational_second_moment.md).

### C10. Formulation ambiguë : second moment vs covariance

**Critique** : `T = Σᵢ wᵢ (μᵢ − xₛ)(μᵢ − xₛ)ᵀ` n'est pas une covariance car
`xₛ` n'est pas le barycentre pondéré `μ̄ = Σᵢ wᵢ μᵢ`. Le doc v2.0 ne le
disait pas.

**Réponse v3.0 — fix appliqué** :

- [Doc 09 §1.1](09_civilizational_second_moment.md)
  expose la décomposition rigoureuse :
  `M = Cov_w(μ ; w) + (Σw) · (μ̄ − xₛ)(μ̄ − xₛ)ᵀ` avec démonstration.
- `state_moments.json` publie les deux composantes séparément sous
  `decomposition.intra_civilizational_covariance` et `decomposition.bias_term`.
- Le test `test_decomposition_consistency` vérifie l'identité
  numériquement État par État.

### C11. Redondance informationnelle de `M(s)` par rapport à `xₛ`

**Critique** : `wₛ` est dérivé de `xₛ` (softmax inverse-distance), donc
`M(s)` est doublement fonction de `xₛ`. Quelle est la **valeur ajoutée
informationnelle** de `M(s)` ?

**Réponse v3.0 — clarification doc** :

- [Doc 09 §1.3](09_civilizational_second_moment.md) :
  `M(s)` est une **structuration directionnelle** du signal `xₛ`. Les
  eigenvectors `eₖ` répondent à *dans quelles directions Hofstede l'État
  voit-il les civilisations dispersées ?*, ce que `xₛ` seul ne dit pas.
- Caractère **secondaire** explicitement admis : `M(s)` ne crée pas de
  signal nouveau, il en révèle la structure directionnelle.
- Test empirique : [doc 13 §3](13_sensitivity_analysis.md) vérifie si
  l'anisotropie `A(s)` corrèle avec une mesure indépendante de fragmentation
  civilisationnelle (par exemple Fragility Index).

### C12. Invariant `I2` mal défini

**Critique** : `I2 = tr(T²) − tr(T)²/n` n'est pas la définition canonique
de l'invariant de von Mises. La vraie définition utilise le déviateur
`s = T − tr(T)/n · I` et la double contraction `√(3/2 · s:s)`.

**Réponse v3.0 — fix appliqué** :

- `apps/basis_builder/moments.py` calcule `I2_von_mises = √(3/2 · s:s)`
  conforme à la mécanique des solides.
- Champ renommé en `I2_von_mises` dans `state_moment.schema.json`.
- Tests `test_von_mises_invariant_is_non_negative`.

### C13. Interprétation des `eₖ` comme « directions de fracture » non validée

**Critique** : le doc v2.0 §6 propose des prédictions pour TUR, IND, LBN
sans les confronter aux données calculées.

**Réponse v3.0 — fix partiel** :

- [Doc 09 §6](09_civilizational_second_moment.md)
  étiquette désormais ces lectures comme **hypothèses interprétatives**.
- [Doc 13 §3 « Plausibilité des cas connus »](13_sensitivity_analysis.md)
  confronte les prédictions aux mesures.
- Si la confrontation échoue, on l'écrit. Aucune réécriture *a posteriori*
  des prédictions.

---

## D. Critiques sur l'algèbre des distances

### D14. Mahalanobis sur 11 observations + ridge = peu robuste

**Critique** : `d_score^M_centroids` estime une covariance 6×6 sur 11
centroïdes avec ridge `λ=1`. Statistiquement, c'est très fragile.

**Réponse v3.0 — fix appliqué** :

- **Nouvelle métrique** `d_score_mahalanobis_intra` qui utilise la covariance
  **intra-civilisationnelle moyenne** (diagonale `Σ_intra[k,k] = ⟨σᵢ[k]²⟩ᵢ`).
- L'ancienne `d_score_mahalanobis_centroids` reste publiée pour comparaison.
- `d_hyb` utilise désormais `d_score^M_intra` (cf.
  [doc 10 §2.8](10_distance_algebra.md)).
- Tests dans `tests/test_distance_algebra.py` valident les deux.

### D15. Poids `(α, β, γ) = (0.4, 0.4, 0.2)` non justifiés empiriquement

**Critique** : choix éditoriaux sans validation.

**Réponse v3.0 — fix appliqué** :

- **Normalisation par médiane** : chaque composante est divisée par sa
  médiane panel avant combinaison convexe (cf.
  `normalise_distances_by_panel_median` dans `distances.py`).
- **Sweep** : [doc 13 §3](13_sensitivity_analysis.md) publie l'effet du
  changement de poids sur les voisinages calculés.
- Choix par défaut éditorial **assumé** et documenté
  ([doc 10 §2.8](10_distance_algebra.md)).

### D16. Circularité de `d_w^W`

**Critique** : la distance Wasserstein-2 utilise comme coût au sol
`D_ij = ‖μᵢ − μⱼ‖_2` qui dépend des centroïdes. Les affinités `wₛ` sont
dérivées des distances aux centroïdes. Donc `d_w^W` est une distance entre
deux objets dérivés des centroïdes, comparés selon une métrique elle-même
dérivée des centroïdes. **Circularité partielle**.

**Réponse v3.0 — admis explicitement** :

- [Doc 10 §2.6](10_distance_algebra.md)
  reconnaît la circularité.
- Conséquence : `d_w^W` est **fiable pour comparer deux États** mais
  **non interprétable absolument**.
- Travail futur : explorer un coût au sol indépendant (par exemple
  distances religieuses Pew).

---

## E. Critiques épistémologiques et éthiques

### E17. Essentialisme étatique : modéliser un État comme un point

**Critique** : représenter la France comme un point `xFRA^score ∈ ℝ⁶` masque
les fractures internes (urbain/rural, classes, religion, immigration). C'est
une essentialisation territoriale.

**Réponse du projet** :

1. **Scope déclaré** : `cvs/` est explicitement *State-first* (cf.
   [doc 03](03_state_first_scope.md)). L'objet est l'**État souverain**,
   pas la population.
2. **Anticipation ADM1** : l'architecture est prête à modéliser des unités
   sub-nationales (cf. [doc 04](04_adm1_preparation_policy.md)).
3. **Ellipses d'incertitude** : `Σₛ^viz` publie l'incertitude de localisation
   d'un État dans `B_viz`.
4. **Mise en garde explicite** dans [doc 07](07_ethics_publication_policy.md) :
   *« Cette modélisation ne capture pas les hétérogénéités internes »*.

### E18. Politique éthique trop courte (v2.0 = 8 lignes)

**Critique** : pour un projet qui prétend modéliser les civilisations, une
politique éthique de 8 lignes est insuffisante.

**Réponse v3.0 — fix appliqué** :

- [Doc 07](07_ethics_publication_policy.md) étoffée à ~80 lignes :
  audience cible, restrictions d'usage géopolitique, escalade en cas de
  mésusage, mécanisme de retrait, gouvernance des modifications, consent
  populations WVS, conflits d'intérêt, légitimité de la classification
  des États.

### E19. La classification des États est-elle elle-même légitime ?

**Critique** : l'avertissement *« ne pas classer des individus »* est répété,
mais la classification des États en civilisations peut alimenter des récits
identitaires ou de conflit de civilisations à l'échelle géopolitique.

**Réponse du projet** :

1. **Pas une classification, mais un scoring continu** : un État reçoit
   un **vecteur d'affinité** `wₛ ∈ Δ¹⁰`, pas une étiquette. La
   « civilisation dominante » n'est qu'un résumé visualisable.
2. **Limites d'usage explicites** : [doc 07](07_ethics_publication_policy.md)
   §« Restrictions d'usage géopolitique » interdit l'usage du scoring
   pour justifier des récits de fracture ou de hiérarchie civilisationnelle.
3. **Limite épistémologique admise** : voir [doc 07 §« Légitimité »](07_ethics_publication_policy.md).

---

## F. Critiques sur la rigueur statistique

### F20. Incertitude non propagée

**Critique** : les CI sur WVS, les σ Hofstede ne se propagent pas dans
`M(s)`, `d_hyb`, `wₛ`.

**Réponse v3.0 — partielle** :

- **Propagation déclarée comme travail futur** ([doc 13 §5](13_sensitivity_analysis.md)).
- **Sensibilité aux centroïdes via LOO publiée** ([doc 13 §1](13_sensitivity_analysis.md)).
- Pas de bootstrap formel sur les CI WVS en v3.0.

### F21. Tests de sensibilité non publiés en v2.0

**Critique** : sensibilité annoncée mais aucune mesure.

**Réponse v3.0 — fix appliqué** :

- [Doc 13 — Sensitivity analysis](13_sensitivity_analysis.md) publie :
  LOO sur archétypes, sweep `β`, sweep `(α, β, γ)`.
- Résultats versionnés dans `assets/data/empirical/sensitivity_*.json`.

### F22. Imputation depuis « proxies régionaux » non décrite

**Critique** : doc v2.0 §5.1 mentionne *« imputation depuis proxies
régionaux »* sans procédé.

**Réponse v3.0 — fix doc** :

- [Doc 08 §5.1](08_civilizational_basis.md) précise
  désormais la procédure : `np.nanmean` sur les dimensions disponibles,
  flag `coverage: imputed` sur le résultat.

### F23. Pas de baseline non-supervisé

**Critique** : la taxonomie Huntington-informée n'est jamais confrontée à
un clustering non-supervisé (k-means, HDBSCAN) sur les données brutes.

**Réponse v3.0 — fix appliqué** :

- [Doc 14 — Baseline non-supervisé](14_baseline_unsupervised.md) publie :
  k-means (k=11) + HDBSCAN sur WVS+Hofstede brut.
- Comparaison ARI, NMI à la taxonomie. Discussion des points de convergence
  et de divergence.

### F24. Pas de validation externe

**Critique** : `wₛ` n'est pas corrélé à des indicateurs externes (Pew, WGI,
Fragility Index).

**Réponse v3.0 — fix appliqué** :

- [Doc 12 — Validation empirique externe](12_empirical_validation.md)
  publie : corrélations Spearman entre `wₛ` et trois indicateurs
  indépendants (Pew Religious Composition, WGI, FSI).
- Bootstrap des CI à 95%.

---

## G. Critiques structurelles sur la documentation

### G25. Format hétérogène docs 00-07 (JSON-style) vs 08-15 (prose)

**Réponse v3.0 — fix appliqué** :

- [Docs 00-06](00_project_decisions.md) ont été harmonisés en prose
  long-form (~30-60 lignes chacun) avec contexte, justification, et
  références aux docs 08-15.

### G26. Absence de glossaire

**Réponse v3.0 — fix appliqué** :

- [Doc 15 — Glossaire](15_glossary.md) publie les définitions de tous les
  termes spécialisés : `B_doc`, `B_vec`, `M(s)`, `wₛ`, `d_hyb`, anisotropie,
  archétype, periphery, ambiguous, etc.

### G27. Absence de page « comment contribuer »

**Statut** : la page `site_src/docs/review/index.md existe depuis Phase 1b
mais reste minimale. Travail futur : étoffer.

---

## H. Synthèse — état des corrections

| # | Critique | Statut v3.0 |
|---|---|---|
| A1 | Huntington essentialiste | **Atténuée** : extensions + baseline |
| A2 | Hofstede critiqué | **Atténuée** : orthogonalité postulée, Mahalanobis intra |
| A3 | IW eurocentrique + dérive | **Bornée** : vague unique |
| A4 | WVS biais d'échantillon | **Admise** + ellipses publiées |
| B5 | Mélange IW + Hofstede | **Séparation explicite** + corrélation publiée |
| B6 | Poids `0.5` arbitraire | **Sensibilité publiée** (doc 13) |
| B7 | β=0.05 ad-hoc | **Sweep publié** (doc 13) |
| B8 | Extensions floues | **Règle de désambiguïsation** (doc 08 §3.4) |
| C9 | Physics envy | **Fix : rename M(s)** |
| C10 | Cov vs second moment | **Fix : décomposition publiée** |
| C11 | Redondance M ↔ x_s | **Clarifiée** doc 09 §1.3 |
| C12 | von Mises incorrect | **Fix : déviateur** |
| C13 | Eigenvecteurs interprétés | **Hypothèses + test doc 13** |
| D14 | Mahalanobis fragile | **Fix : version intra** |
| D15 | Poids hybride non justifiés | **Normalisation médiane + sweep** |
| D16 | Circularité Wasserstein | **Admise** doc 10 §2.6 |
| E17 | Essentialisme étatique | **Admis** + scope déclaré |
| E18 | Éthique trop courte | **Fix : doc 07 étoffée** |
| E19 | Légitimité classification | **Adressée** doc 07 |
| F20 | Incertitude non propagée | **Travail futur** + LOO publié |
| F21 | Tests de sensibilité | **Fix : doc 13** |
| F22 | Imputation opaque | **Fix : doc 08 §5.1** |
| F23 | Pas de baseline | **Fix : doc 14** |
| F24 | Pas de validation externe | **Fix : doc 12** |
| G25 | Format hétérogène | **Fix : docs 00-06 prose** |
| G26 | Pas de glossaire | **Fix : doc 15** |
| G27 | Pas de guide contribution | **Travail futur** |
| H28 | Circularité de la cascade d'imputation | **Réponse stratifiée** (cf. ci-dessous) |

24 critiques sur 27 ont reçu un **fix** ou une **réponse argumentée** en v3.0.
Les 3 restantes (F20, G27 et la difficulté épistémologique fondamentale E19)
sont **explicitement admises** comme limites du projet.

## Section H — Circularité de la cascade d'imputation

### H28 — « Vous imputez via la taxonomie que vous prétendez valider »

La V2 introduit une cascade d'imputation ([doc 16](16_imputation_cascade.md))
qui peut faire suspecter une circularité : le centroïde civilisationnel sert
de *prior* aux États non observés, et ce même centroïde est ensuite confronté
aux données externes pour validation. Trois clauses brisent cette circularité :

1. **Validation stratifiée par provenance** ([doc 12](12_empirical_validation.md)) :
   les tests de cohérence avec Pew, WGI, FSI sont calculés uniquement sur les
   États `observed`, jamais sur les `centroid_prior` (où la corrélation serait
   tautologique).
2. **Centroïdes calculés depuis les observés uniquement** : `compute_centroids()`
   pondère par `ROLE_WEIGHT` (core=1.0, periphery=0.5, ambiguous/interface=0.0)
   et n'utilise que les `member_states` avec données IW/Hofstede réelles. Les
   États `centroid_prior` n'influent jamais sur le centroïde dont ils héritent.
3. **Inflation de variance dans `M(s)`** ([doc 09](09_civilizational_second_moment.md)
   §1.1) : les invariants des États imputés sont marqués comme tels et la
   variance prior est explicite — un lecteur ne peut pas confondre une mesure
   avec un prior.

La cascade est donc un mécanisme de **couverture** sans **propagation circulaire**.

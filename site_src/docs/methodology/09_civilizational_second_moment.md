# 09 — Second moment civilisationnel `M(s)`

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.** Voir [`07_ethics_publication_policy.md](07_ethics_publication_policy.md).

!!! note "Renommage v3.0 (anciennement « tenseur de tension `T(s)` »)"
    L'objet mathématique est identique à celui publié sous le nom `T(s)` en v2.0.
    Le **nom** a été corrigé pour évacuer une analogie mécanique fragile : la
    formule `Σᵢ wᵢ (μᵢ − xₛ)(μᵢ − xₛ)ᵀ` est un **second moment pondéré**, pas
    une grandeur de contrainte. L'analogie aux milieux continus reste une
    métaphore pédagogique, jamais une physique. Voir
    [doc 11 §C9–C13](11_critiques_and_responses.md).

## 1. Définition et dérivation rigoureuse

Pour un État `s` avec :

- vecteur d'affinité `wₛ ∈ Δ¹⁰` (poids sur les 11 macro-civilisations, simplexe),
- coordonnée `xₛ ∈ B_score = ℝ⁶` (vecteur Hofstede 6D),
- centroïdes `μᵢ^score ∈ ℝ⁶` des civilisations `i = 1..11`,

le **second moment civilisationnel** est défini par :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − xₛ)(μᵢ − xₛ)ᵀ           ∈ ℝ^{6×6}
```

C'est l'**outer product pondéré** des écarts à chaque centroïde, sommé sur les
civilisations. Le résultat est :

- **symétrique** : `M = Mᵀ`,
- **positif semi-défini** : pour tout `u`, `uᵀMu = Σᵢ wₛ[i] · ((μᵢ − xₛ)·u)² ≥ 0`.

### 1.1 Décomposition Cov_w + biais

Soit `μ̄ = Σᵢ wₛ[i] · μᵢ` le **barycentre pondéré** des centroïdes sous
l'affinité de l'État. Alors :

```
M(s) = Cov_w(μ ; wₛ)  +  (Σᵢ wₛ[i]) · (μ̄ − xₛ)(μ̄ − xₛ)ᵀ
```

où `Cov_w(μ ; wₛ) = Σᵢ wₛ[i] · (μᵢ − μ̄)(μᵢ − μ̄)ᵀ` est la **covariance
pondérée des centroïdes autour de leur barycentre d'affinité**.

#### Démonstration

Écrivons `Δᵢ = μᵢ − xₛ = (μᵢ − μ̄) + (μ̄ − xₛ)`. Alors :

```
Δᵢ Δᵢᵀ = (μᵢ − μ̄)(μᵢ − μ̄)ᵀ
       + (μᵢ − μ̄)(μ̄ − xₛ)ᵀ
       + (μ̄ − xₛ)(μᵢ − μ̄)ᵀ
       + (μ̄ − xₛ)(μ̄ − xₛ)ᵀ
```

En sommant avec poids `wₛ[i]` et en utilisant `Σᵢ wₛ[i](μᵢ − μ̄) = 0` (par
définition de `μ̄`), les termes croisés s'annulent et il reste :

```
M(s) = Σᵢ wₛ[i] · (μᵢ − μ̄)(μᵢ − μ̄)ᵀ  +  (Σᵢ wₛ[i]) · (μ̄ − xₛ)(μ̄ − xₛ)ᵀ
     = Cov_w(μ ; wₛ)  +  (Σᵢ wₛ[i]) · (μ̄ − xₛ)(μ̄ − xₛ)ᵀ
```

(QED)

### 1.2 Interprétation des deux composantes

| Composante | Nature | Interprétation |
|---|---|---|
| `Cov_w(μ ; wₛ)` | Dispersion **intra-civilisationnelle** sous l'affinité de l'État | Étalement géométrique des centroïdes pondéré par `wₛ` — indépendant de `xₛ`. |
| `(μ̄ − xₛ)(μ̄ − xₛ)ᵀ · Σwₛ` | **Biais** de l'État par rapport à son barycentre d'affinité | Rang 1, aligné sur le vecteur `μ̄ − xₛ` — mesure à quel point l'État est en-dehors de la zone d'affinité qu'il revendique. |

Cette décomposition est publiée dans `state_moments.json` sous la clé
`decomposition` (cf. `schemas/state_moment.schema.json`).

### 1.3 Valeur informationnelle au-delà de `xₛ`

Une critique légitime (cf. [doc 11 §C11](11_critiques_and_responses.md)) est
que `wₛ` est déjà dérivé de `xₛ` (softmax inverse-distance, cf.
[doc 08 §4.2](08_civilizational_basis.md)),
donc `M(s)` est doublement fonction de `xₛ` et **redondant en information**.

La nuance : `M(s)` est une **fonction non-linéaire** de `xₛ` qui factorise
l'information selon **les directions Hofstede où les civilisations se
distribuent**. Là où `xₛ` répond à *où est l'État dans `B_score`*, `M(s)`
répond à *dans quelles directions l'État voit-il les civilisations
dispersées ?*. Les eigenvectors `eₖ` capturent ces directions.

C'est une information **secondaire** : elle ne crée pas de signal nouveau,
mais elle structure le signal existant selon des axes interprétables. Sa
validité empirique est testée dans [doc 13 — Sensitivity analysis](13_sensitivity_analysis.md).

## 2. Invariants scalaires

| Invariant | Formule | Interprétation |
|---|---|---|
| `I1 = tr(M)` | Trace | Magnitude totale de la dispersion pondérée |
| `I2_von_mises` | `√(3/2 · s:s)` avec `s = M − tr(M)/6 · I` (déviateur) | Mesure standard de l'anisotropie déviatorique (mécanique des solides) |
| `det(M)` | Déterminant | Volume du second moment |

**Correction v3.0** : la définition de `I2` en v2.0 était `tr(M²) − tr(M)²/n`
qui n'est pas la définition canonique de von Mises. La version corrigée
utilise la double contraction du déviateur `s:s`, conforme à l'usage en
mécanique des solides.

### 2.1 Décomposition propre

```
M(s) = Σₖ λₖ · eₖ ⊗ eₖ     avec λ₁ ≥ … ≥ λ₆ ≥ 0
```

- `λₖ` = **valeur propre k** — magnitude de dispersion sur la direction `eₖ`.
- `eₖ` = **direction principale** dans `B_score`, axes Hofstede combinés où
  la dispersion est maximale.

### 2.2 Index d'anisotropie

```
A(s) = (λ₁ − λ₆) / λ₁     ∈ [0, 1]
```

- `A ≈ 0` : dispersion **isotrope** — État équilibré, dispersion répartie.
- `A ≈ 1` : dispersion **concentrée sur un axe** — État avec un écart dominant
  dans une direction Hofstede combinée.
- Convention : si `λ₁ < ε`, alors `A := 0` (État monocivilisationnel à l'archétype).

## 3. Cas limites et propriétés

### 3.1 État monocivilisationnel à l'archétype

Si `wₛ[i₀] = 1` pour un unique `i₀` et `xₛ = μᵢ₀^score`, alors `M(s) = 0`.
Anisotropie `A := 0` par convention.

### 3.2 État équilibré entre 2 civilisations équidistantes

Si `wₛ[i] = wₛ[j] = 0.5` et `xₛ = (μᵢ + μⱼ)/2 = μ̄`, alors :

- `(μ̄ − xₛ) = 0` → biais nul.
- `Cov_w(μ ; wₛ)` est de rang 1 avec eigenvalue `‖μᵢ − μⱼ‖² / 4` selon
  la direction `μᵢ − μⱼ`.

`λ₁ = ‖μᵢ − μⱼ‖² / 4`, `λ₂ = … = λ₆ = 0`, `A = 1`.

### 3.3 État au barycentre du simplexe (`wₛ[i] = 1/11`)

Si `xₛ = μ̄ = (1/11) Σᵢ μᵢ`, alors le biais est nul et :

```
M(s) = (1/11) Σᵢ (μᵢ − μ̄)(μᵢ − μ̄)ᵀ
```

C'est exactement la **covariance empirique des 11 centroïdes**. Dispersion
intra-civilisationnelle pure, biais nul. Anisotropie modérée selon
l'éparpillement empirique des centroïdes dans `B_score`.

## 4. Schéma JSON

Cf. `schemas/state_moment.schema.json`. Champs publiés par État :

```json
{
  "iso3": "FRA",
  "M": [[6x6 matrix]],
  "eigenvalues": [λ_1, ..., λ_6],
  "eigenvectors": [[e_1], ..., [e_6]],
  "invariants": { "I1_trace": ..., "I2_von_mises": ..., "det": ... },
  "anisotropy": 0.42,
  "decomposition": {
    "weighted_barycentre_mu_bar": [6 values],
    "intra_civilizational_covariance": [[6x6]],
    "bias_term": [[6x6]],
    "trace_intra": ...,
    "trace_bias": ...
  },
  "quality_flags": { "monocivilizational": false, "low_evidence": false }
}
```

## 5. Tests

`tests/test_moment_mechanics.py` couvre :

- `test_moment_is_symmetric` : `‖M − Mᵀ‖_F < ε`.
- `test_moment_is_psd` : eigenvalues ≥ −ε.
- `test_invariant_trace_is_non_negative`, `test_von_mises_invariant_is_non_negative`.
- `test_monocivilizational_state_has_zero_moment`.
- `test_anisotropy_in_unit_interval`.
- `test_principal_directions_are_orthonormal`.
- **`test_decomposition_consistency`** (nouveau v3.0) : `M = Cov_w + biais`
  vérifié numériquement État par État.

## 6. Lectures appliquées

Le tableau ci-dessous propose des **hypothèses interprétatives** à confronter
aux données publiées dans `assets/data/state_moments.json`. Aucune de ces
lectures n'est validée empiriquement à ce stade — elles sont des prédictions
à tester.

| État | Profil attendu | `I1` attendue | Anisotropie attendue | Hypothèse |
|---|---|---|---|---|
| JPN | Quasi monocivilisationnel (Japanese) | basse | basse | État cohérent |
| FRA | Western dominant + influences ibères/méditerranéennes | moyenne | modérée | Identité affirmée mais avec sous-courants |
| TUR | Western / Islamic / Sinic-Orthodox marginal | élevée | élevée | Fracture documentée (UE vs Moyen-Orient) |
| IND | Hindic dominant + Sinic/Islamic minoritaires | élevée | modérée | Vaste héritage multi-civilisationnel |
| LBN | Western / Islamic / Orthodox imbriqués | très élevée | très élevée | Tension multi-confessionnelle structurelle |

Ces hypothèses sont confrontées aux mesures dans
[doc 13 — Sensitivity analysis](13_sensitivity_analysis.md).

## 7. Limites et précautions

1. **Pas de causalité** : `M(s)` mesure une **structure géométrique**, pas
   une dynamique de conflit. Aucune prédiction d'instabilité politique ou
   de guerre civile n'est dérivable.
2. **Sensibilité aux centroïdes** : `M(s)` dépend des `μᵢ^score` calculés
   sur les États archétypes (cf. [doc 08 §4.1](08_civilizational_basis.md)).
   Un changement d'archétypes modifie l'image. Sensibilité quantifiée dans
   [doc 13](13_sensitivity_analysis.md).
3. **Métrique Euclidienne** : `M` repose sur le produit scalaire usuel dans
   `B_score`, qui suppose des unités comparables. L'échelle Hofstede 0-100
   par axe le permet, mais il existe une littérature critique sur la
   commensurabilité des dimensions Hofstede (McSweeney 2002 — cf.
   [doc 11 §A2](11_critiques_and_responses.md)).
4. **Information secondaire** : `M(s)` est fonction non-linéaire de `xₛ`
   via `wₛ` ; il restructure le signal mais n'en crée pas. La décomposition
   `Cov_w + biais` rend cette nuance explicite.
5. **Analogie mécanique** : pédagogique uniquement. Aucun ressort, aucune
   contrainte, aucune dynamique élastique n'est postulée. Le mot
   « anisotropie » n'est qu'une convention de nommage pour `(λ₁−λ₆)/λ₁`.

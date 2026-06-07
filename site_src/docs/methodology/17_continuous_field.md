# 17 — Champ civilisationnel continu sur la sphère (V2)

> **Avertissement éthique** : ce champ est dérivé de sources publiques agrégées et **ne doit jamais** être utilisé pour classer des individus réels. Les valeurs publiées sont des moyennes statistiques sur des populations agrégées au niveau de l'État, propagées spatialement par un Gaussian Process. Voir [`07_ethics_publication_policy.md`](07_ethics_publication_policy.md).

## 1. Motivation : pourquoi abandonner l'État comme unité d'analyse

Les versions précédentes du projet attribuent **un vecteur civilisationnel par État souverain**. Cette représentation a deux limites épistémologiques :

1. **L'État n'est pas le support naturel des valeurs humaines.** Une frontière administrative coupe en deux des aires linguistiques, religieuses, urbaines. Le « vecteur français » est une moyenne pondérée artificielle entre la Bretagne, la Réunion et la frontière belge — utile pour des comparaisons macro, mais qui efface précisément la dynamique spatiale que la théorie de Huntington décrit en termes de *fault lines*.
2. **La dérivée n'est pas définie sur un graphe d'États.** Le gradient `∂x/∂(λ, φ)` — la grandeur qui dit où les valeurs *changent* le plus rapidement — n'a pas de sens sur 193 points discrets. Soit on l'approche par différences finies entre voisins (perd la subtilité locale), soit on interpole continûment.

Ce chapitre formalise un **champ vectoriel continu** `x : S² → ℝ²⊕ℝ⁶⊕Δ¹⁰` obtenu par interpolation Gaussian Process sur les coordonnées d'État, traitées non comme outputs mais comme **observations spatiales** localisées à leurs centroïdes pondérés par population.

## 2. Pipeline

```
state_coordinates.json  ─┐
                         │
populated_places.geojson ┼─► sample_points.json  ─► GP (Matérn 3/2)  ─► continuous_field_*.json
                         │                                                  │
                         └────► z-score normalisation                       ▼
                                                                Jacobienne analytique
                                                                ∂μ/∂λ, ∂μ/∂φ
```

### 2.1 Sample points par État (population-weighted)

Pour chaque ISO3 ONU :

1. Lister les villes Natural Earth 10m `populated_places` avec `ADM0_A3 == iso3` et `POP_MAX > 0`.
2. Appliquer un k-means pondéré (par population) sur les coordonnées de ces villes pour obtenir `k = min(5, 1 + ⌊log₁₀(population_M)⌋)` centres de cluster.
3. Pour chaque cluster, calculer son poids = fraction de la population nationale dans le cluster.

Résultat : **237 sample points** pour 193 États (USA/CHN/IND/BRA = 3 points ; ~150 États = 1 point). Pour les États sans coverage populated_places, fallback sur le centroïde géométrique du polygone ADM0.

**Production future** : remplacer Natural Earth 10m par **GPW v4 (SEDAC NASA)** ou **GHS-POP (JRC)** — grilles raster 1° qui captent la population rurale en plus des centres urbains.

### 2.2 Gaussian Process multi-output avec kernel Matérn 3/2

**V2** : un seul GP multi-output gère simultanément les **19 composantes** du vecteur d'État (`x_viz` 2D + `x_score` 6D + `affinity_vector` 11D). Le kernel est partagé ; seul le vecteur de coefficients `α` diffère par composante. Une seule factorisation Cholesky de `(K + diag(σ_n²))` est donc nécessaire — ~19× plus rapide que 19 fits indépendants.

- **Kernel** : Matérn 3/2 sur grand-cercle, `k(p, q) = σ² (1 + √3 · d/ℓ) exp(-√3 · d/ℓ)` où `d = arccos(sin φ_p sin φ_q + cos φ_p cos φ_q cos(λ_q - λ_p))`.
- **Hyperparamètres optimisés par ML** : `length_scale` et `noise_scale` (multiplicateur global) sont ajustés en maximisant le log marginal likelihood `log p(Y | θ)` par `scipy.optimize.minimize` (L-BFGS-B, 3 restarts pour échapper aux optima locaux). Pour le fit V2 :
  - `ℓ ≈ 0.105 rad ≈ 670 km` (plus court que la valeur initiale 0.4 rad, captant plus de structure régionale)
  - `noise_scale ≈ 0.64` (multiplicateur appliqué au bruit de base par-sample)
  - NLML au minimum ≈ 5820 sur 237 × 19 observations
- **Bruit par-sample** : chaque sample point hérite d'un `σ_n²` calibré sur la provenance de l'État correspondant (`observed` → 0.05, `observed_with_dim_imputation` → 0.10, `imputed_wvs_items` → 0.25, `imputed_pew` → 0.45, `imputed_governance` → 0.45, `centroid_prior` → 1.20). Le bruit est divisé par le poids du cluster (États multipoints : le cluster principal a un poids ≈ 1, les clusters mineurs ont un bruit plus fort).
- **Normalisation** : z-score par composante avant fit, dé-normalisation après prédiction. Stabilise le solveur Cholesky.

### 2.3 Prédiction sur grille 1° × 1°

- **V2** : grille longitudes ∈ [-180, 180) tous les 1°, latitudes ∈ [-90, 90] tous les 1° → 360 × 181 = 65 160 cellules.
- À chaque cellule : `(μ_c, σ²_c)` pour chacune des 19 composantes, plus la Jacobienne `(∂μ_c/∂λ, ∂μ_c/∂φ)`.
- **Format de sortie** : sidecar JSON (`continuous_field_v2_meta.json`, ~10 KB) avec metadata + grille + hyperparamètres + z-score stats ; archive numpy compressée (`continuous_field_v2_arrays.npz`, ~16 MB) pour les 19 × 4 = 76 grilles de `float32`. Chargement paresseux via `np.load`.

### 2.4 Calcul analytique du gradient

La Jacobienne du champ continu en `(λ, φ)` :

$$\frac{\partial \mu}{\partial \lambda}\bigg|_{q^*} = \frac{\partial k_*}{\partial \lambda} \cdot \alpha \quad\text{où}\quad \alpha = (K + \sigma_n^2 I)^{-1} y$$

Pour Matérn 3/2 :

$$\frac{\partial k}{\partial \lambda_q} = -\sigma^2 \frac{3}{\ell^2} d \exp\left(-\frac{\sqrt{3} d}{\ell}\right) \cdot \frac{\partial d}{\partial \lambda_q}$$

avec

$$\frac{\partial d}{\partial \lambda_q} = \frac{\cos \varphi_p \cos \varphi_q \sin(\lambda_q - \lambda_p)}{\sin d}, \quad \frac{\partial d}{\partial \varphi_q} = \frac{\cos \varphi_p \sin \varphi_q \cos(\lambda_q - \lambda_p) - \sin \varphi_p \cos \varphi_q}{\sin d}$$

À `d → 0`, la Jacobienne tend vers zéro de façon lisse (le préfacteur `d` domine la singularité `1/sin d`). Implémenté avec masque numérique pour `d < 1e-9`.

**Validation** : `tests/test_continuous_field.py::test_kernel_gradient_matches_finite_difference` et `test_gp_jacobian_matches_finite_difference` compare la formule analytique à une différence finie centrée à `ε = 1e-5`. Tolérance `5e-4` en valeur absolue. 10/10 tests passent.

## 3. Norme du gradient et fault lines

La magnitude du gradient dans la métrique riemannienne de la sphère :

$$\|\nabla \mu\|^2 = \frac{1}{\cos^2 \varphi} \left(\frac{\partial \mu}{\partial \lambda}\right)^2 + \left(\frac{\partial \mu}{\partial \varphi}\right)^2$$

Les pôles (|φ| > 75°) sont masqués (`NaN`) car la coordonnée `λ` devient dégénérée et le facteur `1/cos² φ` explose numériquement.

**Lecture cartographique** : une magnitude élevée = transition rapide du champ = *fault line civilisationnelle* au sens de Huntington. Le prototype TS (axe Traditional ↔ Secular-Rational) identifie correctement les frontières historiques :

- ~35-40°N, 0-15°E : Méditerranée sud (Maghreb islamique vs Europe latine) ;
- ~55-60°N, 15-20°E : ligne baltique (Europe catholique vs sphère orthodoxe/post-soviétique).

## 4. Conséquences pour les bases existantes

### 4.1 Distance algebra

Le champ continu permet de redéfinir la distance entre deux points `p, q ∈ S²` comme une **intégrale curviligne du gradient** le long du grand-cercle :

$$d_{\text{cult}}(p, q) = \int_{\gamma_{pq}} \|\nabla \mu(\gamma(t))\| \, dt$$

au lieu d'une distance euclidienne en `B_score`. Deux pays politiquement adjacents mais culturellement éloignés (Tchéquie ↔ Slovaquie : faible ; Tchéquie ↔ Roumanie : moyen ; Tchéquie ↔ Kazakhstan : élevé) auront des distances qui reflètent les transitions traversées, pas seulement leurs barycentres.

À implémenter dans `packages/civvec_core/algebra/` quand la V2 du champ continu est prête (cf. roadmap §6).

### 4.2 Second moment M(s)

Le tenseur `M(s)` est défini par État. Avec un champ continu, on peut définir un **tenseur de gradient** `G(p)` en chaque point `p` de la sphère :

$$G(p) = \nabla x_{\text{score}}(p)^\top \nabla x_{\text{score}}(p) \in \mathbb{R}^{6 \times 6}$$

C'est l'analogue du tenseur des déformations de Cauchy en milieu continu. Ses invariants signalent les zones de **stress culturel** (gradient fort dans toutes les directions = transition isotrope) vs **anisotropie directionnelle** (un seul axe culturel change). À explorer en V2.

## 5. Frontières d'État dans la visualisation

Les frontières ADM0 sont **conservées comme repère visuel** mais **ne contraignent pas le modèle**. Sur la carte :

- Couche du bas : choropleth raster du champ continu (cellules 1° à 5°).
- Couche du haut : lignes fines des frontières Natural Earth ADM0.
- Mode toggle : valeur du champ (TS, SE, PDI, …) vs magnitude du gradient (`fault lines`).

C'est un signal éditorial fort : « les valeurs culturelles n'obéissent pas aux frontières administratives ; voici la géographie continue qui en résulte ».

## 6. Statut V2 et roadmap V3

| Item | V2 (2026-06-07) | V3 prévu |
|---|---|---|
| 19 composantes (x_viz + x_score + affinity) | ✅ | — |
| Grille 1° × 1° (65 160 cellules) | ✅ | Optionnel : 0.25° (1 M cellules) |
| Hyperparamètres ML par marginal likelihood | ✅ (length_scale + noise_scale) | Optimisation simultanée par-output |
| Sample points par centroïde pondéré (population) | ✅ Natural Earth populated_places 10m | GPW v4 / GHS-POP raster pour rural |
| Bruit GP indexé sur cascade provenance | ✅ | — |
| Tests math (analytique vs FD) | ✅ 15/15 | Plus de cas edge |
| Page Streamlit avec sélecteur composantes | ✅ | — |
| MapLibre integration | ❌ | V3 prioritaire |
| Distance algebra basée sur le champ | ❌ | V3 — intégrale curviligne du gradient |
| Tenseur de déformation `G(p) = ∇x^T ∇x` | ❌ | V3 — invariants comme M(s) discret |
| Validation empirique (champ vs ESS NUTS-2) | ❌ | V3 |

## 7. Références

- Rasmussen, C. E. & Williams, C. K. I. (2006). *Gaussian Processes for Machine Learning*, MIT Press, ch. 4 (Matérn family).
- Genton, M. G. (2001). « Classes of Kernels for Machine Learning: A Statistics Perspective ». *Journal of Machine Learning Research*, 2, 299-312.
- Huntington, S. P. (1996). *The Clash of Civilizations*, ch. 2 (fault lines).
- Wackernagel, H. (2003). *Multivariate Geostatistics*, Springer (krigeage multivarié).

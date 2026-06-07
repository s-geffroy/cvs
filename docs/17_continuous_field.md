# 17 — Champ civilisationnel continu sur la sphère (prototype)

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

### 2.2 Gaussian Process avec kernel Matérn 3/2 sur la sphère

Pour chaque composante scalaire `c` du vecteur d'État (TS, SE, PDI, IDV, …, affinités), on fit un GP indépendant :

- **Kernel** : Matérn 3/2 sur grand-cercle, `k(p, q) = σ² (1 + √3 · d/ℓ) exp(-√3 · d/ℓ)` où `d = arccos(sin φ_p sin φ_q + cos φ_p cos φ_q cos(λ_q - λ_p))`.
- **Hyperparamètres prototype** : `ℓ = 0.4 rad ≈ 2540 km`, `σ² = 1`, `noise = 0.05`. Sera optimisé par maximum de marginal likelihood en V2.
- **Normalisation** : z-score sur les valeurs d'observation avant fit, dé-normalisation après prédiction. Stabilise numériquement le solveur Cholesky.

### 2.3 Prédiction sur grille 5° × 5°

- Grille longitudes ∈ [-180, 180) tous les 5°, latitudes ∈ [-90, 90] tous les 5° → 72 × 37 = 2664 cellules.
- À chaque cellule : `(μ, σ²)` du GP plus la Jacobienne `(∂μ/∂λ, ∂μ/∂φ)`.

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

## 6. Limites du prototype et roadmap V2

| Limitation prototype V2.1 | Adresse en V2 |
|---|---|
| 1 seule composante (TS) | 19 composantes (x_viz + x_score + affinity_vector), GP multi-output partagé K |
| Grille 5° × 5° (2664 cellules) | Grille 1° × 1° (~65 000 cellules), output tuilé |
| Hyperparamètres `ℓ`, `σ²`, `noise` fixés à la main | Maximisation de la marginal likelihood par L-BFGS |
| Sample points = villes Natural Earth 10m | GPW v4 ou GHS-POP raster pour la population rurale |
| Pas d'incertitude propagée depuis la cascade d'imputation | Bruit `σ_n²(s)` croît avec `data_quality.low_evidence` |
| Distances et tenseur de gradient non-implémentés | Intégration dans `packages/civvec_core/algebra/` et `moments.py` |

## 7. Références

- Rasmussen, C. E. & Williams, C. K. I. (2006). *Gaussian Processes for Machine Learning*, MIT Press, ch. 4 (Matérn family).
- Genton, M. G. (2001). « Classes of Kernels for Machine Learning: A Statistics Perspective ». *Journal of Machine Learning Research*, 2, 299-312.
- Huntington, S. P. (1996). *The Clash of Civilizations*, ch. 2 (fault lines).
- Wackernagel, H. (2003). *Multivariate Geostatistics*, Springer (krigeage multivarié).

"""Civilizational distance algebra (v3.0 — renamed from tension tensors).

Distances provided
------------------
- ``d_viz``                            : Euclidean distance in ``B_viz = ℝ²``.
- ``d_score_euclidean``                : Euclidean distance in ``B_score = ℝ⁶``.
- ``d_score_mahalanobis_centroids``    : Mahalanobis with **inter-civilization**
  covariance estimated from the 11 weighted centroids (low-rank, ridge=1.0).
  Kept for backwards comparability with the v2 metric.
- ``d_score_mahalanobis_intra``        : Mahalanobis with **intra-civilization**
  weighted-pooled covariance (diagonal of `sigma_score` averages — robust default).
- ``d_w_cosine``                       : cosine *dissimilarity* on affinity
  vectors (not a true distance — fails triangle).
- ``d_w_js``                           : Jensen-Shannon distance (sqrt of JSD).
- ``d_w_wasserstein``                  : Wasserstein-2 distance on the simplex
  (Sinkhorn). Ground cost = Euclidean distance between civilization centroids.
- ``d_M_frobenius``                    : Frobenius distance between second-moment
  tensors ``M(s)``. Renamed from ``d_T_frobenius`` to reflect the rename of the
  underlying object — see ``docs/11_critiques_and_responses.md`` §C9–C13.
- ``d_hybrid``                         : convex combination
  ``α · d_score_mahalanobis_intra + β · d_w_wasserstein + γ · d_M_frobenius``.

The hybrid weights are configurable but each component is **normalised by its
panel-wide median** before mixing — this is the empirical normalisation
documented in ``docs/13_sensitivity_analysis.md``.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .transport import sinkhorn_wasserstein_squared


@dataclass(frozen=True)
class HybridWeights:
    alpha: float = 0.4
    beta: float = 0.4
    gamma: float = 0.2

    def __post_init__(self) -> None:
        total = self.alpha + self.beta + self.gamma
        if not np.isclose(total, 1.0):
            raise ValueError(f"HybridWeights must sum to 1.0, got {total}")


def d_viz(x_viz_source: np.ndarray, x_viz_target: np.ndarray) -> float:
    return float(np.linalg.norm(np.asarray(x_viz_source) - np.asarray(x_viz_target)))


def d_score_euclidean(
    x_score_source: np.ndarray, x_score_target: np.ndarray
) -> float:
    return float(np.linalg.norm(np.asarray(x_score_source) - np.asarray(x_score_target)))


def _mahalanobis_distance(
    x_score_source: np.ndarray,
    x_score_target: np.ndarray,
    covariance_inverse: np.ndarray,
) -> float:
    diff = np.asarray(x_score_source) - np.asarray(x_score_target)
    quadratic = float(diff @ covariance_inverse @ diff)
    return float(np.sqrt(max(quadratic, 0.0)))


def d_score_mahalanobis_centroids(
    x_score_source: np.ndarray,
    x_score_target: np.ndarray,
    covariance_inverse: np.ndarray,
) -> float:
    """Mahalanobis distance using INTER-civilization covariance (centroid spread).

    Statistically fragile: covariance estimated on 11 observations in ℝ⁶ + ridge.
    Kept for backward comparability and inter-civ contrast emphasis.
    """
    return _mahalanobis_distance(x_score_source, x_score_target, covariance_inverse)


def d_score_mahalanobis_intra(
    x_score_source: np.ndarray,
    x_score_target: np.ndarray,
    covariance_inverse: np.ndarray,
) -> float:
    """Mahalanobis distance using INTRA-civilization weighted-pooled covariance.

    Robust default: reflects how much each Hofstede dimension actually varies
    *within* civilizations — so the metric down-weights axes that are noisy
    across the panel of archetype states.
    """
    return _mahalanobis_distance(x_score_source, x_score_target, covariance_inverse)


def d_w_cosine(
    affinity_source: np.ndarray, affinity_target: np.ndarray
) -> float:
    source = np.asarray(affinity_source, dtype=float)
    target = np.asarray(affinity_target, dtype=float)
    denominator = float(np.linalg.norm(source) * np.linalg.norm(target))
    if denominator == 0.0:
        return 1.0
    cosine_similarity = float(np.dot(source, target) / denominator)
    return float(1.0 - cosine_similarity)


def d_w_js(
    affinity_source: np.ndarray, affinity_target: np.ndarray
) -> float:
    source = np.asarray(affinity_source, dtype=float)
    target = np.asarray(affinity_target, dtype=float)
    source = source / max(np.sum(source), 1e-300)
    target = target / max(np.sum(target), 1e-300)
    mixture = 0.5 * (source + target)
    jsd = 0.5 * _kl_divergence(source, mixture) + 0.5 * _kl_divergence(target, mixture)
    return float(np.sqrt(max(jsd, 0.0)))


def _kl_divergence(p: np.ndarray, q: np.ndarray) -> float:
    mask = p > 0
    return float(np.sum(p[mask] * np.log(p[mask] / np.maximum(q[mask], 1e-300))))


def d_w_wasserstein(
    affinity_source: np.ndarray,
    affinity_target: np.ndarray,
    ground_cost_squared: np.ndarray,
    entropic_reg: float = 0.05,
) -> float:
    cost_squared = sinkhorn_wasserstein_squared(
        affinity_source, affinity_target, ground_cost_squared, entropic_reg=entropic_reg
    )
    return float(np.sqrt(max(cost_squared, 0.0)))


def d_M_frobenius(
    moment_source: np.ndarray, moment_target: np.ndarray
) -> float:
    """Frobenius distance between second-moment matrices M(s) and M(t)."""
    return float(
        np.linalg.norm(np.asarray(moment_source) - np.asarray(moment_target), ord="fro")
    )


def d_hybrid(
    d_score_mahalanobis_value: float,
    d_w_wasserstein_value: float,
    d_M_frobenius_value: float,
    weights: HybridWeights = HybridWeights(),
) -> float:
    """Convex combination of the three primary distances.

    Inputs SHOULD be pre-normalised (e.g. divided by their panel-wide medians)
    so the convex weights `(α, β, γ)` reflect *relative importance* rather than
    absolute scale. The builder calls ``normalise_distances_by_panel_median``
    before invoking this function.
    """
    return float(
        weights.alpha * d_score_mahalanobis_value
        + weights.beta * d_w_wasserstein_value
        + weights.gamma * d_M_frobenius_value
    )


def civilization_ground_cost_squared(
    centroid_mu_scores: np.ndarray,
) -> np.ndarray:
    """Return (n_civ, n_civ) matrix of squared Euclidean distances between centroids."""
    diff = centroid_mu_scores[:, None, :] - centroid_mu_scores[None, :, :]
    return np.sum(diff ** 2, axis=-1)


def weighted_centroid_covariance_inverse(
    centroid_mu_scores: np.ndarray,
    centroid_weights: np.ndarray | None = None,
    ridge: float = 1.0,
) -> np.ndarray:
    """Inverse-covariance of civilization CENTROIDS in B_score.

    Inter-civ spread. **Low statistical robustness** (n_civ=11 obs in ℝ⁶ + ridge).
    """
    n_civilizations = centroid_mu_scores.shape[0]
    if centroid_weights is None:
        centroid_weights = np.full(n_civilizations, 1.0 / n_civilizations)
    mean = np.average(centroid_mu_scores, axis=0, weights=centroid_weights)
    centered = centroid_mu_scores - mean
    covariance = centered.T @ (centered * centroid_weights[:, None])
    covariance += ridge * np.eye(covariance.shape[0])
    return np.linalg.inv(covariance)


def intra_civilizational_covariance_inverse(
    centroid_sigma_scores: np.ndarray,
    ridge: float = 1.0,
) -> np.ndarray:
    """Inverse of INTRA-civilizational variance (diagonal) averaged across civilizations.

    Robust default. Each civilization centroid carries a per-axis dispersion
    `sigma_score[k]` (std-dev of member-state Hofstede values on axis k).
    Pooling these variances across civilizations gives a diagonal covariance
    Σ_intra with entries Σ_intra[k,k] = mean_i(sigma_i[k]^2).

    The inverse weights axes by the inverse of their typical intra-civ variance,
    which is what Mahalanobis genuinely captures.
    """
    sigma_squared = np.asarray(centroid_sigma_scores, dtype=float) ** 2
    diagonal_variance = np.mean(sigma_squared, axis=0)
    covariance = np.diag(diagonal_variance) + ridge * np.eye(diagonal_variance.shape[0])
    return np.linalg.inv(covariance)


def normalise_distances_by_panel_median(
    distance_matrix: np.ndarray,
) -> np.ndarray:
    """Divide a distance matrix by the median of its upper-triangle off-diagonal entries.

    Used to put the three components of ``d_hybrid`` on comparable scales before
    convex combination.
    """
    upper_triangle_indices = np.triu_indices_from(distance_matrix, k=1)
    upper_triangle_values = distance_matrix[upper_triangle_indices]
    median_value = float(np.median(upper_triangle_values))
    if median_value < 1e-12:
        return distance_matrix
    return distance_matrix / median_value

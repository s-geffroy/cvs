"""Civilizational distance algebra.

Provides:
- d_viz             : Euclidean distance in B_viz (R^2)
- d_score_euclidean : Euclidean distance in B_score (R^6)
- d_score_mahalanobis: Mahalanobis distance in B_score with weighted civ-covariance
- d_w_cosine        : cosine *dissimilarity* on affinity vectors (not a true distance)
- d_w_js            : Jensen-Shannon distance (sqrt of JSD) on affinity vectors
- d_w_wasserstein   : Wasserstein-2 distance on the simplex (Sinkhorn)
- d_T_frobenius     : Frobenius distance between tension tensors
- d_hybrid          : convex combination alpha*d_score_M + beta*d_w_W + gamma*d_T
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


def d_score_mahalanobis(
    x_score_source: np.ndarray,
    x_score_target: np.ndarray,
    covariance_inverse: np.ndarray,
) -> float:
    diff = np.asarray(x_score_source) - np.asarray(x_score_target)
    quadratic = float(diff @ covariance_inverse @ diff)
    return float(np.sqrt(max(quadratic, 0.0)))


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


def d_T_frobenius(
    tensor_source: np.ndarray, tensor_target: np.ndarray
) -> float:
    return float(
        np.linalg.norm(np.asarray(tensor_source) - np.asarray(tensor_target), ord="fro")
    )


def d_hybrid(
    d_score_mahalanobis_value: float,
    d_w_wasserstein_value: float,
    d_T_frobenius_value: float,
    weights: HybridWeights = HybridWeights(),
) -> float:
    return float(
        weights.alpha * d_score_mahalanobis_value
        + weights.beta * d_w_wasserstein_value
        + weights.gamma * d_T_frobenius_value
    )


def civilization_ground_cost_squared(
    centroid_mu_scores: np.ndarray,
) -> np.ndarray:
    """Return (11, 11) matrix of squared Euclidean distances between civ centroids in B_score."""
    diff = centroid_mu_scores[:, None, :] - centroid_mu_scores[None, :, :]
    return np.sum(diff ** 2, axis=-1)


def weighted_covariance_inverse(
    centroid_mu_scores: np.ndarray,
    centroid_weights: np.ndarray | None = None,
    ridge: float = 1.0,
) -> np.ndarray:
    """Return (6, 6) inverse-covariance estimate over the civilization centroids."""
    n_civilizations = centroid_mu_scores.shape[0]
    if centroid_weights is None:
        centroid_weights = np.full(n_civilizations, 1.0 / n_civilizations)
    mean = np.average(centroid_mu_scores, axis=0, weights=centroid_weights)
    centered = centroid_mu_scores - mean
    covariance = (centered.T @ (centered * centroid_weights[:, None]))
    covariance += ridge * np.eye(covariance.shape[0])
    return np.linalg.inv(covariance)

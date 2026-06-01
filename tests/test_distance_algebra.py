"""Distance algebra properties (v3.0 — renamed from tension to second moment)."""
from __future__ import annotations

import numpy as np
import pytest

from packages.civvec_core.algebra.distances import (
    HybridWeights,
    civilization_ground_cost_squared,
    d_hybrid,
    d_M_frobenius,
    d_score_euclidean,
    d_score_mahalanobis_centroids,
    d_score_mahalanobis_intra,
    d_viz,
    d_w_cosine,
    d_w_js,
    d_w_wasserstein,
    intra_civilizational_covariance_inverse,
    normalise_distances_by_panel_median,
    weighted_centroid_covariance_inverse,
)


@pytest.fixture
def random_simplex_pair() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed=42)
    distribution_p = rng.dirichlet(np.ones(11))
    distribution_q = rng.dirichlet(np.ones(11))
    return distribution_p, distribution_q


def test_d_viz_non_negative_symmetric_identity() -> None:
    point_x = np.array([0.5, 0.5])
    point_y = np.array([1.5, -0.3])
    assert d_viz(point_x, point_x) == 0.0
    assert d_viz(point_x, point_y) >= 0
    assert np.isclose(d_viz(point_x, point_y), d_viz(point_y, point_x))


def test_d_score_euclidean_satisfies_triangle() -> None:
    score_x = np.array([40, 91, 62, 46, 26, 68], dtype=float)
    score_y = np.array([68, 71, 43, 86, 63, 48], dtype=float)
    score_z = np.array([54, 46, 95, 92, 88, 42], dtype=float)
    assert (
        d_score_euclidean(score_x, score_z)
        <= d_score_euclidean(score_x, score_y) + d_score_euclidean(score_y, score_z) + 1e-9
    )


def test_d_score_mahalanobis_centroids_zero_on_identity() -> None:
    score_x = np.array([40, 91, 62, 46, 26, 68], dtype=float)
    covariance_inverse = np.eye(6)
    assert d_score_mahalanobis_centroids(score_x, score_x, covariance_inverse) == 0.0


def test_d_score_mahalanobis_intra_zero_on_identity() -> None:
    score_x = np.array([40, 91, 62, 46, 26, 68], dtype=float)
    covariance_inverse = np.eye(6)
    assert d_score_mahalanobis_intra(score_x, score_x, covariance_inverse) == 0.0


def test_d_w_cosine_in_unit_interval(random_simplex_pair) -> None:
    distribution_p, distribution_q = random_simplex_pair
    assert 0.0 <= d_w_cosine(distribution_p, distribution_q) <= 2.0


def test_d_w_js_is_a_metric(random_simplex_pair) -> None:
    distribution_p, distribution_q = random_simplex_pair
    assert d_w_js(distribution_p, distribution_p) < 1e-9
    assert np.isclose(d_w_js(distribution_p, distribution_q), d_w_js(distribution_q, distribution_p))
    assert d_w_js(distribution_p, distribution_q) >= 0


def test_d_w_wasserstein_zero_on_identity(random_simplex_pair) -> None:
    distribution_p, _ = random_simplex_pair
    cost_squared = np.ones((11, 11)) - np.eye(11)
    distance_value = d_w_wasserstein(distribution_p, distribution_p, cost_squared)
    assert distance_value < 1e-2


def test_d_M_frobenius_zero_on_identity() -> None:
    moment_matrix = np.eye(6)
    assert d_M_frobenius(moment_matrix, moment_matrix) == 0.0


def test_hybrid_weights_must_sum_to_one() -> None:
    with pytest.raises(ValueError):
        HybridWeights(alpha=0.5, beta=0.5, gamma=0.5)


def test_d_hybrid_combination() -> None:
    distance_score_mahalanobis = 1.0
    distance_wasserstein = 2.0
    distance_moment_frobenius = 3.0
    weights = HybridWeights(0.4, 0.4, 0.2)
    expected_value = 0.4 * 1.0 + 0.4 * 2.0 + 0.2 * 3.0
    assert np.isclose(
        d_hybrid(distance_score_mahalanobis, distance_wasserstein, distance_moment_frobenius, weights),
        expected_value,
    )


def test_civilization_ground_cost_squared_symmetric() -> None:
    rng = np.random.default_rng(seed=0)
    centroid_mu_scores = rng.uniform(0, 100, size=(11, 6))
    cost_squared = civilization_ground_cost_squared(centroid_mu_scores)
    assert np.allclose(cost_squared, cost_squared.T)
    assert np.allclose(np.diag(cost_squared), 0.0)


def test_weighted_centroid_covariance_inverse_shape() -> None:
    rng = np.random.default_rng(seed=0)
    centroid_mu_scores = rng.uniform(0, 100, size=(11, 6))
    covariance_inverse = weighted_centroid_covariance_inverse(centroid_mu_scores)
    assert covariance_inverse.shape == (6, 6)


def test_intra_civilizational_covariance_inverse_shape() -> None:
    rng = np.random.default_rng(seed=0)
    centroid_sigma_scores = rng.uniform(5, 25, size=(11, 6))
    covariance_inverse = intra_civilizational_covariance_inverse(centroid_sigma_scores)
    assert covariance_inverse.shape == (6, 6)
    assert np.allclose(covariance_inverse, covariance_inverse.T, atol=1e-12)


def test_normalise_distances_by_panel_median_preserves_zero_diagonal() -> None:
    rng = np.random.default_rng(seed=3)
    raw_matrix = rng.uniform(0, 10, size=(7, 7))
    symmetric_matrix = 0.5 * (raw_matrix + raw_matrix.T)
    np.fill_diagonal(symmetric_matrix, 0.0)
    normalised_matrix = normalise_distances_by_panel_median(symmetric_matrix)
    assert np.allclose(np.diag(normalised_matrix), 0.0)
    upper_triangle = normalised_matrix[np.triu_indices(7, k=1)]
    assert np.isclose(np.median(upper_triangle), 1.0, atol=1e-6)

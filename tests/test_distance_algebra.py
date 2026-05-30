"""Distance algebra properties."""
from __future__ import annotations

import numpy as np
import pytest

from packages.civvec_core.algebra.distances import (
    HybridWeights,
    civilization_ground_cost_squared,
    d_hybrid,
    d_score_euclidean,
    d_score_mahalanobis,
    d_T_frobenius,
    d_viz,
    d_w_cosine,
    d_w_js,
    d_w_wasserstein,
    weighted_covariance_inverse,
)


@pytest.fixture
def random_simplex_pair() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed=42)
    p = rng.dirichlet(np.ones(11))
    q = rng.dirichlet(np.ones(11))
    return p, q


def test_d_viz_non_negative_symmetric_identity() -> None:
    x = np.array([0.5, 0.5])
    y = np.array([1.5, -0.3])
    assert d_viz(x, x) == 0.0
    assert d_viz(x, y) >= 0
    assert np.isclose(d_viz(x, y), d_viz(y, x))


def test_d_score_euclidean_satisfies_triangle() -> None:
    x = np.array([40, 91, 62, 46, 26, 68], dtype=float)
    y = np.array([68, 71, 43, 86, 63, 48], dtype=float)
    z = np.array([54, 46, 95, 92, 88, 42], dtype=float)
    assert d_score_euclidean(x, z) <= d_score_euclidean(x, y) + d_score_euclidean(y, z) + 1e-9


def test_d_score_mahalanobis_zero_on_identity() -> None:
    x = np.array([40, 91, 62, 46, 26, 68], dtype=float)
    covariance_inverse = np.eye(6)
    assert d_score_mahalanobis(x, x, covariance_inverse) == 0.0


def test_d_w_cosine_in_unit_interval(random_simplex_pair) -> None:
    p, q = random_simplex_pair
    assert 0.0 <= d_w_cosine(p, q) <= 2.0


def test_d_w_js_is_a_metric(random_simplex_pair) -> None:
    p, q = random_simplex_pair
    assert d_w_js(p, p) < 1e-9
    assert np.isclose(d_w_js(p, q), d_w_js(q, p))
    assert d_w_js(p, q) >= 0


def test_d_w_wasserstein_zero_on_identity(random_simplex_pair) -> None:
    p, _ = random_simplex_pair
    cost_squared = np.ones((11, 11)) - np.eye(11)
    distance = d_w_wasserstein(p, p, cost_squared)
    assert distance < 1e-2


def test_d_T_frobenius_zero_on_identity() -> None:
    T = np.eye(6)
    assert d_T_frobenius(T, T) == 0.0


def test_hybrid_weights_must_sum_to_one() -> None:
    with pytest.raises(ValueError):
        HybridWeights(alpha=0.5, beta=0.5, gamma=0.5)


def test_d_hybrid_combination() -> None:
    distance_score_m = 1.0
    distance_w_w = 2.0
    distance_t = 3.0
    weights = HybridWeights(0.4, 0.4, 0.2)
    expected = 0.4 * 1.0 + 0.4 * 2.0 + 0.2 * 3.0
    assert np.isclose(d_hybrid(distance_score_m, distance_w_w, distance_t, weights), expected)


def test_civilization_ground_cost_squared_symmetric() -> None:
    rng = np.random.default_rng(seed=0)
    centroid_mu_scores = rng.uniform(0, 100, size=(11, 6))
    cost_squared = civilization_ground_cost_squared(centroid_mu_scores)
    assert np.allclose(cost_squared, cost_squared.T)
    assert np.allclose(np.diag(cost_squared), 0.0)


def test_weighted_covariance_inverse_shape() -> None:
    rng = np.random.default_rng(seed=0)
    centroid_mu_scores = rng.uniform(0, 100, size=(11, 6))
    covariance_inverse = weighted_covariance_inverse(centroid_mu_scores)
    assert covariance_inverse.shape == (6, 6)

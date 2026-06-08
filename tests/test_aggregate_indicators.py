"""Tests for the three aggregate civilizational indicators (2.1, 3.1, 2.2)."""
from __future__ import annotations

import numpy as np
import pytest

from packages.civvec_core.continuous_field.aggregate_indicators import (
    X_SCORE_COMPONENT_NAMES,
    affinity_entropy_inverse_field,
    classification_margin_field,
    deformation_trace_field,
)


# ---------------------------------------------------------------------------
# 2.1 — Force d'identité (entropie inverse normalisée)
# ---------------------------------------------------------------------------


def test_affinity_entropy_inverse_one_at_pure_identity() -> None:
    """A cell where a single civilization dominates → indicator = 1."""
    grid_shape = (3, 4)
    affinities_by_civilization = {
        "western": np.ones(grid_shape),
        "orthodox": np.zeros(grid_shape),
        "islamic": np.zeros(grid_shape),
    }
    indicator_field = affinity_entropy_inverse_field(affinities_by_civilization)
    assert indicator_field.shape == grid_shape
    np.testing.assert_allclose(indicator_field, 1.0)


def test_affinity_entropy_inverse_zero_at_uniform_distribution() -> None:
    """A cell where the 11 affinities are equal → indicator = 0."""
    grid_shape = (2, 3)
    number_of_civilizations = 11
    affinities_by_civilization = {
        f"civ_{civilization_index}": np.full(grid_shape, 1.0 / number_of_civilizations)
        for civilization_index in range(number_of_civilizations)
    }
    indicator_field = affinity_entropy_inverse_field(affinities_by_civilization)
    np.testing.assert_allclose(indicator_field, 0.0, atol=1e-12)


def test_affinity_entropy_inverse_clamps_negatives_and_renormalises() -> None:
    """Negative GP outputs must be clamped before the entropy computation."""
    grid_shape = (1, 1)
    affinities_by_civilization = {
        "western": np.array([[0.8]]),
        "orthodox": np.array([[-0.3]]),  # would corrupt entropy if not clamped
        "islamic": np.array([[0.2]]),
    }
    indicator_field = affinity_entropy_inverse_field(affinities_by_civilization)
    # After clamp: [0.8, 0.0, 0.2] → simplex [0.8, 0.0, 0.2]
    # H = -(0.8·log0.8 + 0.2·log0.2) ≈ 0.5004
    # 1 - H/log(3) ≈ 1 - 0.5004/1.0986 ≈ 0.5446
    assert indicator_field.shape == grid_shape
    assert 0.0 <= indicator_field[0, 0] <= 1.0
    np.testing.assert_allclose(indicator_field[0, 0], 0.5446, atol=1e-3)


def test_affinity_entropy_inverse_bounded_within_unit_interval() -> None:
    """Random GP outputs (some negative) yield indicator ∈ [0, 1]."""
    rng = np.random.default_rng(42)
    grid_shape = (10, 10)
    affinities_by_civilization = {
        f"civ_{civilization_index}": rng.normal(0.1, 0.3, size=grid_shape)
        for civilization_index in range(11)
    }
    indicator_field = affinity_entropy_inverse_field(affinities_by_civilization)
    assert np.all(indicator_field >= 0.0)
    assert np.all(indicator_field <= 1.0 + 1e-9)


def test_affinity_entropy_inverse_requires_two_civilizations() -> None:
    with pytest.raises(ValueError):
        affinity_entropy_inverse_field({"western": np.ones((2, 2))})


# ---------------------------------------------------------------------------
# 3.1 — Tension culturelle (trace du tenseur de déformation)
# ---------------------------------------------------------------------------


def test_deformation_trace_sums_squared_gradient_magnitudes() -> None:
    grid_shape = (4, 5)
    gradient_magnitudes_by_component = {
        "x_viz_ts": np.full(grid_shape, 2.0),
        "x_viz_se": np.full(grid_shape, 3.0),
        "x_score_pdi": np.full(grid_shape, 1.0),
    }
    indicator_field = deformation_trace_field(gradient_magnitudes_by_component)
    np.testing.assert_allclose(indicator_field, 4.0 + 9.0 + 1.0)


def test_deformation_trace_preserves_nan_polar_mask() -> None:
    """Polar NaN cells must propagate through the sum-of-squares."""
    grid_shape = (3, 3)
    gradient_magnitudes_by_component = {
        "x_viz_ts": np.array(
            [[np.nan, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, np.nan]]
        ),
        "x_viz_se": np.ones(grid_shape),
    }
    indicator_field = deformation_trace_field(gradient_magnitudes_by_component)
    assert np.isnan(indicator_field[0, 0])
    assert np.isnan(indicator_field[2, 2])
    np.testing.assert_allclose(indicator_field[1, 1], 2.0)


def test_deformation_trace_z_score_normalisation_balances_components() -> None:
    """When stds are provided, gradient is rescaled to z-units before squaring.

    Without rescaling: x_score component (grad=20) crushes x_viz component (grad=1).
    With rescaling by std=20 vs std=1: both contribute 1.0 → balanced.
    """
    grid_shape = (2, 2)
    gradient_magnitudes_by_component = {
        "x_viz_ts": np.full(grid_shape, 1.0),
        "x_score_pdi": np.full(grid_shape, 20.0),
    }
    raw_trace = deformation_trace_field(gradient_magnitudes_by_component)
    z_normalised_trace = deformation_trace_field(
        gradient_magnitudes_by_component,
        z_score_std_by_component={"x_viz_ts": 1.0, "x_score_pdi": 20.0},
    )
    np.testing.assert_allclose(raw_trace, 1.0 + 400.0)
    np.testing.assert_allclose(z_normalised_trace, 1.0 + 1.0)


def test_deformation_trace_rejects_non_positive_std() -> None:
    with pytest.raises(ValueError):
        deformation_trace_field(
            {"x_viz_ts": np.ones((2, 2))},
            z_score_std_by_component={"x_viz_ts": 0.0},
        )


def test_deformation_trace_non_negative() -> None:
    rng = np.random.default_rng(7)
    grid_shape = (8, 8)
    gradient_magnitudes_by_component = {
        f"component_{component_index}": rng.normal(0.0, 1.0, size=grid_shape)
        for component_index in range(5)
    }
    indicator_field = deformation_trace_field(gradient_magnitudes_by_component)
    assert np.all(indicator_field >= 0.0)


# ---------------------------------------------------------------------------
# 2.2 — Profondeur du cœur (marge de classification)
# ---------------------------------------------------------------------------


def _build_x_score_field_at_point(point_in_b_score: np.ndarray) -> dict[str, np.ndarray]:
    """Build a 1×1 grid where every cell has the same B_score vector."""
    return {
        component_name: np.array([[point_in_b_score[component_index]]])
        for component_index, component_name in enumerate(X_SCORE_COMPONENT_NAMES)
    }


def test_classification_margin_zero_at_midpoint_of_two_centroids() -> None:
    """A point equidistant from two centroids (and far from the rest) → margin ≈ 0."""
    centroid_a = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    centroid_b = np.array([10.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    centroid_far = np.array([100.0, 100.0, 100.0, 100.0, 100.0, 100.0])
    centroids = np.stack([centroid_a, centroid_b, centroid_far], axis=0)
    midpoint = 0.5 * (centroid_a + centroid_b)
    covariance_inverse = np.eye(6)
    x_score_field = _build_x_score_field_at_point(midpoint)
    margin_field = classification_margin_field(
        x_score_field, centroids, covariance_inverse
    )
    np.testing.assert_allclose(margin_field[0, 0], 0.0, atol=1e-9)


def test_classification_margin_large_near_centroid() -> None:
    """A point close to one centroid and far from all others → large margin."""
    centroid_a = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    centroid_b = np.array([100.0, 100.0, 100.0, 100.0, 100.0, 100.0])
    centroid_c = np.array([-100.0, -100.0, -100.0, -100.0, -100.0, -100.0])
    centroids = np.stack([centroid_a, centroid_b, centroid_c], axis=0)
    near_a = np.array([0.1, 0.0, 0.0, 0.0, 0.0, 0.0])
    covariance_inverse = np.eye(6)
    x_score_field = _build_x_score_field_at_point(near_a)
    margin_field = classification_margin_field(
        x_score_field, centroids, covariance_inverse
    )
    # d_1 ≈ 0.1, d_2 ≈ 244.95 → margin ≈ 2448
    assert margin_field[0, 0] > 100.0


def test_classification_margin_rejects_missing_components() -> None:
    incomplete_field = {"x_score_pdi": np.zeros((1, 1))}
    centroids = np.zeros((3, 6))
    covariance_inverse = np.eye(6)
    with pytest.raises(KeyError):
        classification_margin_field(incomplete_field, centroids, covariance_inverse)


def test_classification_margin_rejects_bad_covariance_shape() -> None:
    centroid = np.zeros(6)
    centroids = np.stack([centroid, centroid + 1.0], axis=0)
    x_score_field = _build_x_score_field_at_point(np.zeros(6))
    with pytest.raises(ValueError):
        classification_margin_field(x_score_field, centroids, np.eye(5))


def test_classification_margin_non_negative_field_at_random_points() -> None:
    rng = np.random.default_rng(11)
    centroids = rng.normal(0.0, 30.0, size=(11, 6))
    grid_shape = (6, 9)
    x_score_field = {
        component_name: rng.normal(0.0, 30.0, size=grid_shape)
        for component_name in X_SCORE_COMPONENT_NAMES
    }
    covariance_inverse = np.eye(6) / (30.0 ** 2)
    margin_field = classification_margin_field(
        x_score_field, centroids, covariance_inverse
    )
    assert margin_field.shape == grid_shape
    finite_values = margin_field[np.isfinite(margin_field)]
    assert np.all(finite_values >= 0.0)

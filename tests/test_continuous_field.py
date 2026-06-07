"""Mathematical tests for the spherical GP and its analytical Jacobian.

The cornerstone is the comparison between the closed-form Jacobian and a
finite-difference approximation: if they disagree, the gradient is wrong
and every downstream visualisation / distance-weighting derivation is
corrupt.
"""
from __future__ import annotations

import numpy as np
import pytest

from packages.civvec_core.continuous_field.gp import SphericalGaussianProcess
from packages.civvec_core.continuous_field.kernels import (
    great_circle_distance,
    matern_3_2_sphere,
    matern_3_2_sphere_gradient,
)


def _random_unit_sphere_points(n_points: int, random_seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(random_seed)
    longitudes_rad = rng.uniform(-np.pi, np.pi, size=n_points)
    cos_polar = rng.uniform(-1.0, 1.0, size=n_points)
    latitudes_rad = np.arcsin(cos_polar)
    return longitudes_rad, latitudes_rad


def test_great_circle_distance_is_symmetric_and_nonnegative() -> None:
    longitudes_rad, latitudes_rad = _random_unit_sphere_points(20)
    distance_forward = great_circle_distance(
        longitudes_rad[0], latitudes_rad[0], longitudes_rad[1], latitudes_rad[1]
    )
    distance_backward = great_circle_distance(
        longitudes_rad[1], latitudes_rad[1], longitudes_rad[0], latitudes_rad[0]
    )
    assert np.isclose(distance_forward, distance_backward, atol=1e-12)
    assert 0.0 <= distance_forward <= np.pi + 1e-10


def test_matern_kernel_is_one_at_self() -> None:
    kernel_value = matern_3_2_sphere(
        np.array(0.5), np.array(0.3), np.array(0.5), np.array(0.3), length_scale=0.5
    )
    assert np.isclose(float(kernel_value), 1.0, atol=1e-12)


def test_matern_kernel_is_symmetric() -> None:
    longitudes_rad, latitudes_rad = _random_unit_sphere_points(5)
    kernel_forward = matern_3_2_sphere(
        longitudes_rad[0],
        latitudes_rad[0],
        longitudes_rad[1],
        latitudes_rad[1],
        length_scale=0.4,
    )
    kernel_backward = matern_3_2_sphere(
        longitudes_rad[1],
        latitudes_rad[1],
        longitudes_rad[0],
        latitudes_rad[0],
        length_scale=0.4,
    )
    assert np.isclose(float(kernel_forward), float(kernel_backward), atol=1e-12)


def test_kernel_gradient_matches_finite_difference() -> None:
    """The analytical gradient of the kernel wrt query coords must equal the FD approximation."""
    longitudes_train_rad, latitudes_train_rad = _random_unit_sphere_points(
        4, random_seed=1
    )
    longitudes_query_rad, latitudes_query_rad = _random_unit_sphere_points(
        6, random_seed=2
    )

    length_scale = 0.4
    epsilon = 1e-5

    grad_longitude_kernel, grad_latitude_kernel = matern_3_2_sphere_gradient(
        longitudes_train_rad[None, :],
        latitudes_train_rad[None, :],
        longitudes_query_rad[:, None],
        latitudes_query_rad[:, None],
        length_scale=length_scale,
    )

    kernel_plus_longitude = matern_3_2_sphere(
        longitudes_train_rad[None, :],
        latitudes_train_rad[None, :],
        longitudes_query_rad[:, None] + epsilon,
        latitudes_query_rad[:, None],
        length_scale=length_scale,
    )
    kernel_minus_longitude = matern_3_2_sphere(
        longitudes_train_rad[None, :],
        latitudes_train_rad[None, :],
        longitudes_query_rad[:, None] - epsilon,
        latitudes_query_rad[:, None],
        length_scale=length_scale,
    )
    finite_diff_longitude = (kernel_plus_longitude - kernel_minus_longitude) / (
        2 * epsilon
    )

    kernel_plus_latitude = matern_3_2_sphere(
        longitudes_train_rad[None, :],
        latitudes_train_rad[None, :],
        longitudes_query_rad[:, None],
        latitudes_query_rad[:, None] + epsilon,
        length_scale=length_scale,
    )
    kernel_minus_latitude = matern_3_2_sphere(
        longitudes_train_rad[None, :],
        latitudes_train_rad[None, :],
        longitudes_query_rad[:, None],
        latitudes_query_rad[:, None] - epsilon,
        length_scale=length_scale,
    )
    finite_diff_latitude = (kernel_plus_latitude - kernel_minus_latitude) / (
        2 * epsilon
    )

    assert np.allclose(grad_longitude_kernel, finite_diff_longitude, atol=1e-5), (
        f"Max |analytic - FD| longitude = "
        f"{np.max(np.abs(grad_longitude_kernel - finite_diff_longitude)):.3e}"
    )
    assert np.allclose(grad_latitude_kernel, finite_diff_latitude, atol=1e-5), (
        f"Max |analytic - FD| latitude = "
        f"{np.max(np.abs(grad_latitude_kernel - finite_diff_latitude)):.3e}"
    )


def test_gp_predict_matches_training_targets_at_zero_noise() -> None:
    longitudes_train_rad, latitudes_train_rad = _random_unit_sphere_points(
        10, random_seed=3
    )
    rng = np.random.default_rng(4)
    training_targets = rng.standard_normal(10)

    gp = SphericalGaussianProcess(
        longitudes_train=longitudes_train_rad,
        latitudes_train=latitudes_train_rad,
        target_values_train=training_targets,
        length_scale=0.5,
        noise_variance=1e-10,
    ).fit()

    predicted_mean, _ = gp.predict(longitudes_train_rad, latitudes_train_rad)
    assert np.allclose(predicted_mean, training_targets, atol=1e-4), (
        f"Max |predicted - target| = {np.max(np.abs(predicted_mean - training_targets)):.3e}"
    )


def test_gp_jacobian_matches_finite_difference() -> None:
    """The analytical GP Jacobian must agree with finite differences of the predicted mean."""
    longitudes_train_rad, latitudes_train_rad = _random_unit_sphere_points(
        15, random_seed=5
    )
    rng = np.random.default_rng(6)
    training_targets = rng.standard_normal(15)

    gp = SphericalGaussianProcess(
        longitudes_train=longitudes_train_rad,
        latitudes_train=latitudes_train_rad,
        target_values_train=training_targets,
        length_scale=0.5,
        noise_variance=0.05,
    ).fit()

    longitudes_query_rad, latitudes_query_rad = _random_unit_sphere_points(
        8, random_seed=7
    )
    # Stay away from the poles where the (1/cos φ) factor distorts comparisons.
    valid_mask = np.abs(latitudes_query_rad) < np.deg2rad(70.0)
    longitudes_query_rad = longitudes_query_rad[valid_mask]
    latitudes_query_rad = latitudes_query_rad[valid_mask]

    epsilon = 1e-5
    analytic_grad_longitude, analytic_grad_latitude = gp.jacobian(
        longitudes_query_rad, latitudes_query_rad
    )

    mean_plus_longitude, _ = gp.predict(
        longitudes_query_rad + epsilon, latitudes_query_rad
    )
    mean_minus_longitude, _ = gp.predict(
        longitudes_query_rad - epsilon, latitudes_query_rad
    )
    finite_diff_longitude = (mean_plus_longitude - mean_minus_longitude) / (2 * epsilon)

    mean_plus_latitude, _ = gp.predict(
        longitudes_query_rad, latitudes_query_rad + epsilon
    )
    mean_minus_latitude, _ = gp.predict(
        longitudes_query_rad, latitudes_query_rad - epsilon
    )
    finite_diff_latitude = (mean_plus_latitude - mean_minus_latitude) / (2 * epsilon)

    assert np.allclose(analytic_grad_longitude, finite_diff_longitude, atol=5e-4), (
        f"Max |analytic - FD| longitude = "
        f"{np.max(np.abs(analytic_grad_longitude - finite_diff_longitude)):.3e}"
    )
    assert np.allclose(analytic_grad_latitude, finite_diff_latitude, atol=5e-4), (
        f"Max |analytic - FD| latitude = "
        f"{np.max(np.abs(analytic_grad_latitude - finite_diff_latitude)):.3e}"
    )


def test_gp_predict_returns_finite_values_near_pole() -> None:
    """Predicted mean and variance must stay finite even when query points approach a pole."""
    longitudes_train_rad, latitudes_train_rad = _random_unit_sphere_points(
        5, random_seed=8
    )
    rng = np.random.default_rng(9)
    training_targets = rng.standard_normal(5)
    gp = SphericalGaussianProcess(
        longitudes_train=longitudes_train_rad,
        latitudes_train=latitudes_train_rad,
        target_values_train=training_targets,
        length_scale=0.5,
        noise_variance=0.05,
    ).fit()

    polar_longitudes_rad = np.array([0.0, 0.5, 1.0])
    polar_latitudes_rad = np.array([1.55, -1.55, 1.50])
    predicted_mean, predicted_variance = gp.predict(
        polar_longitudes_rad, polar_latitudes_rad
    )
    assert np.all(np.isfinite(predicted_mean))
    assert np.all(np.isfinite(predicted_variance))
    assert np.all(predicted_variance >= 0.0)


@pytest.mark.parametrize("length_scale", [0.2, 0.5, 1.0])
def test_gp_variance_is_low_near_training_points(length_scale: float) -> None:
    longitudes_train_rad, latitudes_train_rad = _random_unit_sphere_points(
        20, random_seed=10
    )
    rng = np.random.default_rng(11)
    training_targets = rng.standard_normal(20)
    gp = SphericalGaussianProcess(
        longitudes_train=longitudes_train_rad,
        latitudes_train=latitudes_train_rad,
        target_values_train=training_targets,
        length_scale=length_scale,
        noise_variance=0.01,
    ).fit()

    _, training_variance = gp.predict(longitudes_train_rad, latitudes_train_rad)
    assert training_variance.mean() < 0.05, (
        f"Variance at training points should be near zero but mean is {training_variance.mean():.3f}"
    )

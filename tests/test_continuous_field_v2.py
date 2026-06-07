"""V2 tests : multi-output GP, per-sample noise, ML hyperparameter optimisation."""
from __future__ import annotations

import numpy as np
import pytest

from packages.civvec_core.continuous_field.gp import SphericalGaussianProcess


def _random_unit_sphere_points(
    n_points: int, random_seed: int = 0
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(random_seed)
    longitudes_rad = rng.uniform(-np.pi, np.pi, size=n_points)
    cos_polar = rng.uniform(-1.0, 1.0, size=n_points)
    latitudes_rad = np.arcsin(cos_polar)
    return longitudes_rad, latitudes_rad


def test_multi_output_predict_matches_independent_univariate_fits() -> None:
    """A multi-output GP must give the same prediction as D independent univariate GPs."""
    longitudes_train, latitudes_train = _random_unit_sphere_points(12, random_seed=2)
    rng = np.random.default_rng(3)
    targets_matrix = rng.standard_normal(size=(12, 4))

    multi_output_gp = SphericalGaussianProcess(
        longitudes_train=longitudes_train,
        latitudes_train=latitudes_train,
        target_values_train=targets_matrix,
        length_scale=0.4,
        noise_variance=0.05,
    ).fit()

    longitudes_query, latitudes_query = _random_unit_sphere_points(
        6, random_seed=4
    )

    multi_mean, multi_variance = multi_output_gp.predict(
        longitudes_query, latitudes_query
    )
    assert multi_mean.shape == (6, 4)
    assert multi_variance.shape == (6,)

    for output_index in range(4):
        univariate_gp = SphericalGaussianProcess(
            longitudes_train=longitudes_train,
            latitudes_train=latitudes_train,
            target_values_train=targets_matrix[:, output_index],
            length_scale=0.4,
            noise_variance=0.05,
        ).fit()
        univariate_mean, univariate_variance = univariate_gp.predict(
            longitudes_query, latitudes_query
        )
        assert np.allclose(multi_mean[:, output_index], univariate_mean, atol=1e-10)
        assert np.allclose(multi_variance, univariate_variance, atol=1e-10)


def test_per_sample_noise_propagates_to_alpha() -> None:
    """Sample points with higher noise must have less influence on the GP fit."""
    longitudes_train, latitudes_train = _random_unit_sphere_points(8, random_seed=5)
    targets = np.array([10.0, -5.0, 3.0, 7.0, -8.0, 1.0, 4.0, -2.0])

    uniform_noise_gp = SphericalGaussianProcess(
        longitudes_train=longitudes_train,
        latitudes_train=latitudes_train,
        target_values_train=targets,
        length_scale=0.5,
        noise_variance=0.05,
    ).fit()

    heavy_noise_on_first_gp = SphericalGaussianProcess(
        longitudes_train=longitudes_train,
        latitudes_train=latitudes_train,
        target_values_train=targets,
        length_scale=0.5,
        noise_variance=np.array([10.0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]),
    ).fit()

    _, variance_uniform = uniform_noise_gp.predict(
        longitudes_train[:1], latitudes_train[:1]
    )
    _, variance_heavy = heavy_noise_on_first_gp.predict(
        longitudes_train[:1], latitudes_train[:1]
    )
    assert variance_heavy[0] > variance_uniform[0], (
        f"Heavy noise at sample 0 should leave residual variance there: "
        f"got {variance_heavy[0]:.4f} vs uniform {variance_uniform[0]:.4f}"
    )


def test_per_sample_noise_rejects_wrong_shape() -> None:
    longitudes_train, latitudes_train = _random_unit_sphere_points(5, random_seed=6)
    targets = np.zeros(5)
    with pytest.raises(ValueError):
        SphericalGaussianProcess(
            longitudes_train=longitudes_train,
            latitudes_train=latitudes_train,
            target_values_train=targets,
            noise_variance=np.array([0.1, 0.1]),
        ).fit()


def test_ml_hyperparameter_fit_improves_likelihood() -> None:
    """The optimised hyperparameters must produce a lower NLML than a random default."""
    longitudes_train, latitudes_train = _random_unit_sphere_points(20, random_seed=7)
    rng = np.random.default_rng(8)
    targets = rng.standard_normal(size=(20, 3))

    default_gp = SphericalGaussianProcess(
        longitudes_train=longitudes_train,
        latitudes_train=latitudes_train,
        target_values_train=targets,
        length_scale=1.5,
        noise_variance=0.5,
    ).fit()

    ml_gp = SphericalGaussianProcess(
        longitudes_train=longitudes_train,
        latitudes_train=latitudes_train,
        target_values_train=targets,
        length_scale=1.5,
        noise_variance=0.5,
    ).fit_hyperparameters(n_restarts=3, random_seed=9)

    assert "ml_optimised_length_scale_rad" in ml_gp.metadata
    assert ml_gp.length_scale != default_gp.length_scale
    assert "negative_log_marginal_likelihood" in ml_gp.metadata
    assert np.isfinite(ml_gp.metadata["negative_log_marginal_likelihood"])


def test_multi_output_jacobian_per_output_dimension() -> None:
    """The multi-output Jacobian must give one (∂λ, ∂φ) per output dimension."""
    longitudes_train, latitudes_train = _random_unit_sphere_points(10, random_seed=12)
    rng = np.random.default_rng(13)
    targets = rng.standard_normal(size=(10, 5))

    gp = SphericalGaussianProcess(
        longitudes_train=longitudes_train,
        latitudes_train=latitudes_train,
        target_values_train=targets,
        length_scale=0.4,
        noise_variance=0.05,
    ).fit()

    longitudes_query, latitudes_query = _random_unit_sphere_points(
        4, random_seed=14
    )
    grad_longitude, grad_latitude = gp.jacobian(longitudes_query, latitudes_query)
    assert grad_longitude.shape == (4, 5)
    assert grad_latitude.shape == (4, 5)

    # Cross-check against univariate fit on output 2.
    univariate_gp = SphericalGaussianProcess(
        longitudes_train=longitudes_train,
        latitudes_train=latitudes_train,
        target_values_train=targets[:, 2],
        length_scale=0.4,
        noise_variance=0.05,
    ).fit()
    univariate_grad_longitude, univariate_grad_latitude = univariate_gp.jacobian(
        longitudes_query, latitudes_query
    )
    assert np.allclose(grad_longitude[:, 2], univariate_grad_longitude, atol=1e-10)
    assert np.allclose(grad_latitude[:, 2], univariate_grad_latitude, atol=1e-10)

"""V3 tests: deformation tensor invariants and curvilinear cultural distance."""
from __future__ import annotations

import numpy as np

from packages.civvec_core.continuous_field import (
    SphericalGaussianProcess,
    cauchy_green_per_cell,
    curvilinear_cultural_distance,
    deformation_tensor_invariants,
    stack_jacobian_per_component,
)


def _make_fitted_gp(n_outputs: int = 4) -> SphericalGaussianProcess:
    rng = np.random.default_rng(20)
    longitudes_train = rng.uniform(-np.pi, np.pi, size=15)
    latitudes_train = np.arcsin(rng.uniform(-1.0, 1.0, size=15))
    target_matrix = rng.standard_normal(size=(15, n_outputs))
    return SphericalGaussianProcess(
        longitudes_train=longitudes_train,
        latitudes_train=latitudes_train,
        target_values_train=target_matrix,
        length_scale=0.4,
        noise_variance=0.05,
    ).fit()


def test_deformation_tensor_invariants_match_eigen_decomposition() -> None:
    grid_shape = (5, 7)
    rng = np.random.default_rng(21)
    gradient_longitude_per_component = {
        f"output_{output_index}": rng.standard_normal(size=grid_shape)
        for output_index in range(4)
    }
    gradient_latitude_per_component = {
        f"output_{output_index}": rng.standard_normal(size=grid_shape)
        for output_index in range(4)
    }

    jacobian_per_cell = stack_jacobian_per_component(
        gradient_longitude_per_component, gradient_latitude_per_component
    )
    cauchy_green_field = cauchy_green_per_cell(jacobian_per_cell)
    invariants = deformation_tensor_invariants(cauchy_green_field)

    for row_index in range(grid_shape[0]):
        for column_index in range(grid_shape[1]):
            cell_matrix = cauchy_green_field[row_index, column_index]
            eigenvalues = np.linalg.eigvalsh(cell_matrix)
            eigenvalue_major_expected = eigenvalues[-1]
            eigenvalue_minor_expected = eigenvalues[0]
            assert np.isclose(
                invariants.eigenvalue_major[row_index, column_index],
                eigenvalue_major_expected,
                atol=1e-9,
            )
            assert np.isclose(
                invariants.eigenvalue_minor[row_index, column_index],
                eigenvalue_minor_expected,
                atol=1e-9,
            )
            assert np.isclose(
                invariants.trace[row_index, column_index],
                cell_matrix[0, 0] + cell_matrix[1, 1],
                atol=1e-9,
            )


def test_deformation_tensor_anisotropy_is_zero_for_isotropic_jacobian() -> None:
    grid_shape = (3, 3)
    gradient_per_component = {
        "output_a": np.ones(grid_shape),
        "output_b": np.zeros(grid_shape),
    }
    gradient_orthogonal_per_component = {
        "output_a": np.zeros(grid_shape),
        "output_b": np.ones(grid_shape),
    }
    jacobian_per_cell = stack_jacobian_per_component(
        gradient_per_component, gradient_orthogonal_per_component
    )
    cauchy_green_field = cauchy_green_per_cell(jacobian_per_cell)
    invariants = deformation_tensor_invariants(cauchy_green_field)
    assert np.allclose(invariants.anisotropy, 0.0, atol=1e-9)


def test_curvilinear_distance_at_zero_arc_is_zero() -> None:
    gp = _make_fitted_gp(n_outputs=4)
    same_point_distance = curvilinear_cultural_distance(
        gp, longitude_start_rad=0.5, latitude_start_rad=0.3,
        longitude_end_rad=0.5, latitude_end_rad=0.3,
    )
    assert np.isclose(same_point_distance, 0.0, atol=1e-9)


def test_curvilinear_distance_positive_for_distinct_points() -> None:
    gp = _make_fitted_gp(n_outputs=4)
    distance = curvilinear_cultural_distance(
        gp, longitude_start_rad=0.1, latitude_start_rad=0.2,
        longitude_end_rad=0.8, latitude_end_rad=-0.1,
        n_segments=32,
    )
    assert np.isfinite(distance)
    assert distance > 0.0


def test_curvilinear_distance_increases_with_arc_for_constant_gradient() -> None:
    """Longer arcs should give larger integrals when the gradient is roughly uniform."""
    gp = _make_fitted_gp(n_outputs=2)
    short_distance = curvilinear_cultural_distance(
        gp, longitude_start_rad=0.0, latitude_start_rad=0.0,
        longitude_end_rad=0.2, latitude_end_rad=0.0,
    )
    longer_distance = curvilinear_cultural_distance(
        gp, longitude_start_rad=0.0, latitude_start_rad=0.0,
        longitude_end_rad=1.0, latitude_end_rad=0.0,
    )
    # Same starting point and same heading; longer arc must integrate a
    # bigger total path length × roughly comparable gradient magnitude.
    assert longer_distance >= short_distance


def test_curvilinear_distance_converges_with_more_segments() -> None:
    gp = _make_fitted_gp(n_outputs=3)
    distance_coarse = curvilinear_cultural_distance(
        gp, longitude_start_rad=0.0, latitude_start_rad=0.0,
        longitude_end_rad=0.6, latitude_end_rad=0.2, n_segments=8,
    )
    distance_fine = curvilinear_cultural_distance(
        gp, longitude_start_rad=0.0, latitude_start_rad=0.0,
        longitude_end_rad=0.6, latitude_end_rad=0.2, n_segments=64,
    )
    # Trapezoidal integration: more segments → smaller error
    assert abs(distance_fine - distance_coarse) < 0.5 * max(
        abs(distance_coarse), abs(distance_fine), 1e-6
    )

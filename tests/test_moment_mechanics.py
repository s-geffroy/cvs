"""Second-moment invariants M(s) (renamed from tension tensor T(s) in v3.0)."""
from __future__ import annotations

import numpy as np

from apps.basis_builder.moments import compute_second_moment


def test_moment_is_symmetric(computed_state_moments) -> None:
    for iso3, moment in computed_state_moments.items():
        matrix_M = np.array(moment.M, dtype=float)
        assert np.allclose(matrix_M, matrix_M.T, atol=1e-9), f"{iso3}: M not symmetric"


def test_moment_is_psd(computed_state_moments) -> None:
    for iso3, moment in computed_state_moments.items():
        eigenvalues = np.array(moment.eigenvalues, dtype=float)
        assert np.all(eigenvalues >= -1e-9), f"{iso3}: negative eigenvalue"


def test_invariant_trace_is_non_negative(computed_state_moments) -> None:
    for iso3, moment in computed_state_moments.items():
        assert moment.invariants["I1_trace"] >= -1e-9, f"{iso3}: trace < 0"


def test_von_mises_invariant_is_non_negative(computed_state_moments) -> None:
    for iso3, moment in computed_state_moments.items():
        assert moment.invariants["I2_von_mises"] >= -1e-9, f"{iso3}: von Mises < 0"


def test_monocivilizational_state_has_zero_moment(computed_centroids) -> None:
    from apps.basis_builder.projector import StateCoordinates

    centroid = next(iter(computed_centroids.values()))
    mu_score = [value if value is not None else 50.0 for value in centroid.mu_score]
    fake_state = StateCoordinates(
        iso3="ZZZ",
        label=None,
        x_viz=[0.0, 0.0],
        x_viz_ellipse=None,
        x_score=mu_score,
        affinity_vector={
            civilization_id: (1.0 if civilization_id == centroid.civilization_id else 0.0)
            for civilization_id in computed_centroids
        },
        data_quality={"iw_coverage": "present", "hofstede_coverage": "present", "low_evidence": False},
        source_refs=[],
    )
    moment = compute_second_moment(fake_state, computed_centroids)
    assert moment is not None
    assert moment.invariants["I1_trace"] < 1e-6


def test_anisotropy_in_unit_interval(computed_state_moments) -> None:
    for iso3, moment in computed_state_moments.items():
        assert 0.0 <= moment.anisotropy <= 1.0, f"{iso3}: A out of [0,1]"


def test_principal_directions_are_orthonormal(computed_state_moments) -> None:
    for iso3, moment in computed_state_moments.items():
        eigenvectors = np.array(moment.eigenvectors, dtype=float)
        identity_check = eigenvectors.T @ eigenvectors
        assert np.allclose(identity_check, np.eye(6), atol=1e-6), (
            f"{iso3}: eigenvectors not orthonormal"
        )


def test_decomposition_consistency(computed_state_moments) -> None:
    """M(s) = Cov_w(mu;w) + sum(w) * (mu_bar - x_s)(mu_bar - x_s)^T (up to numerical noise)."""
    for iso3, moment in computed_state_moments.items():
        matrix_M = np.array(moment.M, dtype=float)
        intra_covariance = np.array(
            moment.decomposition["intra_civilizational_covariance"], dtype=float
        )
        bias_term = np.array(moment.decomposition["bias_term"], dtype=float)
        reconstructed = intra_covariance + bias_term
        assert np.allclose(matrix_M, reconstructed, atol=1e-6), (
            f"{iso3}: decomposition M = Cov_w + bias not satisfied"
        )

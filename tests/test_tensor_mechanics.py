"""Tensor mechanics invariants."""
from __future__ import annotations

import numpy as np

from apps.basis_builder.tensors import compute_tension_tensor


def test_tensor_is_symmetric(computed_state_tensions) -> None:
    for iso3, tension in computed_state_tensions.items():
        T = np.array(tension.T, dtype=float)
        assert np.allclose(T, T.T, atol=1e-9), f"{iso3}: T not symmetric"


def test_tensor_is_psd(computed_state_tensions) -> None:
    for iso3, tension in computed_state_tensions.items():
        eigenvalues = np.array(tension.eigenvalues, dtype=float)
        assert np.all(eigenvalues >= -1e-9), f"{iso3}: negative eigenvalue"


def test_invariants_non_negative(computed_state_tensions) -> None:
    for iso3, tension in computed_state_tensions.items():
        assert tension.invariants["I1"] >= -1e-9, f"{iso3}: I1 < 0"


def test_monocivilizational_state_has_zero_tension(computed_centroids) -> None:
    from apps.basis_builder.projector import StateCoordinates

    centroid = next(iter(computed_centroids.values()))
    mu_score = [v if v is not None else 50.0 for v in centroid.mu_score]
    fake_state = StateCoordinates(
        iso3="ZZZ",
        label=None,
        x_viz=[0.0, 0.0],
        x_viz_ellipse=None,
        x_score=mu_score,
        affinity_vector={cid: (1.0 if cid == centroid.civilization_id else 0.0) for cid in computed_centroids},
        data_quality={"iw_coverage": "present", "hofstede_coverage": "present", "low_evidence": False},
        source_refs=[],
    )
    tension = compute_tension_tensor(fake_state, computed_centroids)
    assert tension is not None
    assert tension.invariants["I1"] < 1e-6


def test_anisotropy_in_unit_interval(computed_state_tensions) -> None:
    for iso3, tension in computed_state_tensions.items():
        assert 0.0 <= tension.anisotropy <= 1.0, f"{iso3}: A out of [0,1]"


def test_principal_directions_are_orthonormal(computed_state_tensions) -> None:
    for iso3, tension in computed_state_tensions.items():
        vectors = np.array(tension.eigenvectors, dtype=float)
        identity = vectors.T @ vectors
        assert np.allclose(identity, np.eye(6), atol=1e-6), (
            f"{iso3}: eigenvectors not orthonormal"
        )

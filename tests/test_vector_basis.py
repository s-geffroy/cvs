"""B_vec invariants: basis dimensions, centroids in domain, affinity simplex."""
from __future__ import annotations

import json

import numpy as np

from apps.basis_builder.paths import B_SCORE_PATH, B_VIZ_PATH


def test_B_viz_dimensions_are_two_and_orthogonality_label_is_honest() -> None:
    """v3.0 corrects the v2.0 misleading 'empirical_orthogonal_by_construction'
    label to 'postulated_orthogonal_not_empirically_verified' since the
    Inglehart-Welzel axes have ~0.15 residual correlation in wave 7
    (cf. doc 11 section A3).
    """
    b_viz = json.loads(B_VIZ_PATH.read_text())
    assert b_viz["dimensions"] == 2
    assert b_viz["orthogonality"] == "postulated_orthogonal_not_empirically_verified"


def test_B_score_dimensions_are_six() -> None:
    b_score = json.loads(B_SCORE_PATH.read_text())
    assert b_score["dimensions"] == 6
    axis_ids = [a["id"] for a in b_score["axes"]]
    assert axis_ids == ["e_PDI", "e_IDV", "e_MAS", "e_UAI", "e_LTO", "e_IVR"]


def test_each_civilization_has_at_least_3_archetype_states(computed_centroids) -> None:
    low_coverage_civilizations = {"japanese", "hindic", "indigenous", "oceanian"}
    for civ_id, centroid in computed_centroids.items():
        if civ_id in low_coverage_civilizations:
            assert centroid.computed_from_n_states >= 1
        else:
            assert centroid.computed_from_n_states >= 3, (
                f"{civ_id}: only {centroid.computed_from_n_states} archetypes"
            )


def test_centroid_score_in_domain(computed_centroids) -> None:
    for civ_id, centroid in computed_centroids.items():
        for value in centroid.mu_score:
            if value is None:
                continue
            assert 0.0 <= value <= 100.0, f"{civ_id}: mu_score out of [0,100] -> {value}"


def test_affinity_vector_is_simplex(computed_state_coordinates) -> None:
    for iso3, state in computed_state_coordinates.items():
        weights = list(state.affinity_vector.values())
        assert all(w >= 0 for w in weights), f"{iso3}: negative weight"
        assert np.isclose(sum(weights), 1.0, atol=1e-6), (
            f"{iso3}: sum(w) = {sum(weights)}"
        )

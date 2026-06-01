"""Shared pytest fixtures: build the basis once per session."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture(scope="session")
def computed_centroids():
    from apps.basis_builder.centroids import compute_centroids

    return compute_centroids()


@pytest.fixture(scope="session")
def computed_state_coordinates(computed_centroids):
    from apps.basis_builder.projector import project_states

    return project_states(computed_centroids)


@pytest.fixture(scope="session")
def computed_state_moments(computed_centroids, computed_state_coordinates):
    from apps.basis_builder.moments import compute_second_moment

    moments = {}
    for iso3, state in computed_state_coordinates.items():
        moment = compute_second_moment(state, computed_centroids)
        if moment is not None:
            moments[iso3] = moment
    return moments

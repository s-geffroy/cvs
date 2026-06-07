"""Centroid prior: fall back on a civilization's barycentre when nothing else is observed.

When a UN-member state has no Inglehart-Welzel coordinate, no Hofstede profile,
and no auxiliary source linkable to a calibration, we degenerate gracefully to
the **centroid of its curated civilization**:

    x_viz(s)    = mu_viz(civ)
    x_score(s)  = mu_score(civ)
    ellipse(s)  = sigma_viz(civ)
    sigma6(s)   = sigma_score(civ)

This is the bayesian prior over civilization positions, with no posterior
update because no observation is available. Downstream tensors gonfle their
diagonal by sigma_score(civ)^2 to propagate the uncertainty.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from apps.basis_builder.centroids import CivilizationCentroid


@dataclass(frozen=True)
class CentroidPriorCoordinates:
    x_viz: list[float]
    x_viz_ellipse: dict[str, Any]
    x_score: list[float]
    sigma_score: list[float]


def centroid_prior_for_state(
    civilization_id: str,
    centroids: dict[str, CivilizationCentroid],
) -> CentroidPriorCoordinates | None:
    """Return centroid-derived coordinates for a state, or None if the centroid is degenerate."""
    centroid = centroids.get(civilization_id)
    if centroid is None:
        return None
    if any(value is None for value in centroid.mu_viz):
        return None
    if any(value is None for value in centroid.mu_score):
        return None

    return CentroidPriorCoordinates(
        x_viz=[float(value) for value in centroid.mu_viz],
        x_viz_ellipse={
            "sigma": [[float(cell) for cell in row] for row in centroid.sigma_viz],
            "confidence_level": 0.80,
            "source": "centroid_prior",
        },
        x_score=[float(value) for value in centroid.mu_score],
        sigma_score=[float(value) for value in centroid.sigma_score],
    )

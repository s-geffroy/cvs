"""Compute the civilizational tension tensor T(s) for each state.

T(s) = Sum_i w_s[i] * (mu_i - x_s) outer (mu_i - x_s)   in R^{6x6}

Yields invariants (I1=trace, I2=von Mises analogue, det), eigenvalues
(sorted descending), eigenvectors, and anisotropy index A.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from .centroids import CivilizationCentroid, compute_centroids
from .load_hofstede import HOFSTEDE_DIMENSION_ORDER
from .paths import STATE_TENSORS_PATH
from .projector import StateCoordinates, project_states


@dataclass
class StateTension:
    iso3: str
    T: list[list[float]]
    eigenvalues: list[float]
    eigenvectors: list[list[float]]
    invariants: dict[str, float]
    anisotropy: float
    quality_flags: dict[str, bool]


def compute_tension_tensor(
    state: StateCoordinates,
    centroids: dict[str, CivilizationCentroid],
) -> StateTension | None:
    """Return T(s) and derived quantities, or None if x_score is missing."""
    if any(v is None for v in state.x_score):
        return None
    x_score = np.array(state.x_score, dtype=float)
    tensor = np.zeros((6, 6), dtype=float)
    for civ_id, weight in state.affinity_vector.items():
        centroid = centroids.get(civ_id)
        if centroid is None or any(v is None for v in centroid.mu_score):
            continue
        mu = np.array(centroid.mu_score, dtype=float)
        delta = mu - x_score
        tensor += float(weight) * np.outer(delta, delta)

    tensor = 0.5 * (tensor + tensor.T)
    eigenvalues, eigenvectors = np.linalg.eigh(tensor)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    eigenvalues = np.maximum(eigenvalues, 0.0)

    trace = float(np.trace(tensor))
    frobenius_squared = float(np.sum(eigenvalues ** 2))
    determinant = float(np.linalg.det(tensor))
    von_mises_proxy = max(frobenius_squared - (trace ** 2) / 6.0, 0.0)

    if eigenvalues[0] < 1e-9:
        anisotropy = 0.0
    else:
        anisotropy = float((eigenvalues[0] - eigenvalues[-1]) / eigenvalues[0])

    is_monocivilizational = (
        max(state.affinity_vector.values()) > 0.95 and trace < 1.0
    )

    return StateTension(
        iso3=state.iso3,
        T=tensor.tolist(),
        eigenvalues=eigenvalues.tolist(),
        eigenvectors=eigenvectors.tolist(),
        invariants={"I1": trace, "I2": von_mises_proxy, "det": determinant},
        anisotropy=anisotropy,
        quality_flags={
            "monocivilizational": is_monocivilizational,
            "low_evidence": bool(state.data_quality.get("low_evidence", False)),
            "computed_from_imputed": state.data_quality.get(
                "hofstede_coverage"
            ) == "imputed",
        },
    )


def compute_all_tensions() -> dict[str, StateTension]:
    centroids = compute_centroids()
    state_coords = project_states(centroids)
    tensions: dict[str, StateTension] = {}
    for iso3, state in state_coords.items():
        tension = compute_tension_tensor(state, centroids)
        if tension is not None:
            tensions[iso3] = tension
    return tensions


def write_tensions(tensions: dict[str, StateTension]) -> None:
    STATE_TENSORS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "_meta": {
            "schema": "state_tension.schema.json",
            "dimension_order_score": list(HOFSTEDE_DIMENSION_ORDER),
        },
        "tensions": [asdict(t) for t in tensions.values()],
    }
    STATE_TENSORS_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

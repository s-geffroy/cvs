"""Compute the civilizational second moment M(s) for each state.

Definition
----------
For a state ``s`` with affinity vector ``w_s ∈ Δ¹⁰`` and B_score coordinate
``x_s ∈ ℝ⁶``, the **weighted second moment** about ``x_s`` of the
civilizational centroids is

    M(s) = Σᵢ w_s[i] · (μᵢ − x_s)(μᵢ − x_s)ᵀ                ∈ ℝ^{6×6}

This is *not* a covariance: ``x_s`` is not the weighted barycentre. Using the
identity

    M(s) = Cov_w(μ; w) + (μ̄ − x_s)(μ̄ − x_s)ᵀ
    with μ̄ = Σᵢ w_s[i] · μᵢ

separates the **intra-civilizational dispersion** from the **bias** of the
state relative to its affinity-weighted barycentre. See
``docs/09_civilizational_second_moment.md`` for the derivation.

Outputs
-------
- ``M`` : 6×6 symmetric PSD matrix.
- ``eigenvalues`` (descending) and ``eigenvectors`` : directional dispersion.
- ``invariants`` :
    - ``I1 = tr(M)`` — total weighted second-moment magnitude.
    - ``I2_von_mises = sqrt(3/2 · s : s)`` where ``s = M − tr(M)/6 · I`` is the
      deviatoric part — the standard von Mises invariant.
    - ``det = det(M)``.
- ``anisotropy`` ``A = (λ₁ − λ₆) / λ₁ ∈ [0, 1]``.

The historical name "civilizational tension tensor T(s)" is **deprecated** in
favour of "civilizational second moment M(s)" — see
``docs/11_critiques_and_responses.md`` §C9–C13.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from .centroids import CivilizationCentroid, compute_centroids
from .load_hofstede import HOFSTEDE_DIMENSION_ORDER
from .paths import STATE_MOMENTS_PATH
from .projector import StateCoordinates, project_states


@dataclass
class StateSecondMoment:
    iso3: str
    M: list[list[float]]
    eigenvalues: list[float]
    eigenvectors: list[list[float]]
    invariants: dict[str, float]
    anisotropy: float
    quality_flags: dict[str, bool]
    decomposition: dict[str, Any]


def _von_mises_invariant(matrix: np.ndarray) -> float:
    """Standard von Mises invariant of a symmetric tensor: sqrt(3/2 · s:s).

    ``s = matrix − tr(matrix)/n · I`` is the deviatoric part. For ``n=6``
    this matches the engineering convention used in solid mechanics.
    """
    dimension = matrix.shape[0]
    deviatoric = matrix - (np.trace(matrix) / dimension) * np.eye(dimension)
    double_contraction = float(np.sum(deviatoric * deviatoric))
    return float(np.sqrt(max(1.5 * double_contraction, 0.0)))


def compute_second_moment(
    state: StateCoordinates,
    centroids: dict[str, CivilizationCentroid],
) -> StateSecondMoment | None:
    """Return M(s) and derived quantities.

    Under the imputation cascade, ``x_score`` is non-null for every UN
    member state. When ``x_score_provenance != observed`` the diagonal of
    ``M`` is inflated by the per-dimension prior variance
    (``x_score_sigma_prior^2`` for ``centroid_prior``, the calibration RMSE
    squared for ``imputed_governance``). This propagates the imputation
    uncertainty rather than masquerading priors as hard observations.
    """
    if any(coordinate_value is None for coordinate_value in state.x_score):
        return None
    x_score = np.array(state.x_score, dtype=float)

    weighted_barycentre = np.zeros(6, dtype=float)
    weight_sum = 0.0
    centroid_mu_scores: list[np.ndarray] = []
    centroid_weights: list[float] = []

    for civilization_id, civilization_weight in state.affinity_vector.items():
        centroid = centroids.get(civilization_id)
        if centroid is None or any(value is None for value in centroid.mu_score):
            continue
        mu_score = np.array(centroid.mu_score, dtype=float)
        weighted_barycentre += float(civilization_weight) * mu_score
        weight_sum += float(civilization_weight)
        centroid_mu_scores.append(mu_score)
        centroid_weights.append(float(civilization_weight))

    if weight_sum < 1e-12:
        return None
    weighted_barycentre /= weight_sum

    moment_matrix = np.zeros((6, 6), dtype=float)
    intra_covariance = np.zeros((6, 6), dtype=float)
    for mu_score, civilization_weight in zip(centroid_mu_scores, centroid_weights):
        delta_to_state = mu_score - x_score
        moment_matrix += civilization_weight * np.outer(delta_to_state, delta_to_state)
        delta_to_barycentre = mu_score - weighted_barycentre
        intra_covariance += civilization_weight * np.outer(
            delta_to_barycentre, delta_to_barycentre
        )

    moment_matrix = 0.5 * (moment_matrix + moment_matrix.T)
    intra_covariance = 0.5 * (intra_covariance + intra_covariance.T)
    bias_term = np.outer(
        weighted_barycentre - x_score, weighted_barycentre - x_score
    ) * weight_sum

    sigma_prior = state.data_quality.get("x_score_sigma_prior")
    if sigma_prior is not None:
        prior_variance_inflation = np.diag(
            np.square(np.array(sigma_prior, dtype=float))
        )
        moment_matrix = moment_matrix + prior_variance_inflation
    else:
        prior_variance_inflation = np.zeros((6, 6), dtype=float)

    eigenvalues, eigenvectors = np.linalg.eigh(moment_matrix)
    ordering = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[ordering]
    eigenvectors = eigenvectors[:, ordering]
    eigenvalues = np.maximum(eigenvalues, 0.0)

    trace_value = float(np.trace(moment_matrix))
    determinant_value = float(np.linalg.det(moment_matrix))
    von_mises_value = _von_mises_invariant(moment_matrix)

    anisotropy_value = (
        0.0
        if eigenvalues[0] < 1e-9
        else float((eigenvalues[0] - eigenvalues[-1]) / eigenvalues[0])
    )

    is_monocivilizational = (
        max(state.affinity_vector.values()) > 0.95 and trace_value < 1.0
    )

    return StateSecondMoment(
        iso3=state.iso3,
        M=moment_matrix.tolist(),
        eigenvalues=eigenvalues.tolist(),
        eigenvectors=eigenvectors.tolist(),
        invariants={
            "I1_trace": trace_value,
            "I2_von_mises": von_mises_value,
            "det": determinant_value,
        },
        anisotropy=anisotropy_value,
        quality_flags={
            "monocivilizational": is_monocivilizational,
            "low_evidence": bool(state.data_quality.get("low_evidence", False)),
            "computed_from_imputed": state.data_quality.get(
                "x_score_provenance"
            )
            in ("imputed_governance", "centroid_prior"),
            "x_score_provenance": state.data_quality.get(
                "x_score_provenance", "unknown"
            ),
            "diagonal_inflated_by_prior": sigma_prior is not None,
        },
        decomposition={
            "weighted_barycentre_mu_bar": weighted_barycentre.tolist(),
            "intra_civilizational_covariance": intra_covariance.tolist(),
            "bias_term": bias_term.tolist(),
            "prior_variance_inflation": prior_variance_inflation.tolist(),
            "trace_intra": float(np.trace(intra_covariance)),
            "trace_bias": float(np.trace(bias_term)),
            "trace_prior_inflation": float(np.trace(prior_variance_inflation)),
        },
    )


def compute_all_second_moments() -> dict[str, StateSecondMoment]:
    centroids = compute_centroids()
    state_coords = project_states(centroids)
    moments: dict[str, StateSecondMoment] = {}
    for iso3, state in state_coords.items():
        moment_record = compute_second_moment(state, centroids)
        if moment_record is not None:
            moments[iso3] = moment_record
    return moments


def write_second_moments(moments: dict[str, StateSecondMoment]) -> None:
    STATE_MOMENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "_meta": {
            "schema": "state_moment.schema.json",
            "dimension_order_score": list(HOFSTEDE_DIMENSION_ORDER),
            "matrix_field": "M",
            "definition": (
                "M(s) = sum_i w_s[i] * (mu_i - x_s) outer (mu_i - x_s) "
                "= Cov_w(mu;w) + weight_sum * (mu_bar - x_s)(mu_bar - x_s)^T"
            ),
        },
        "moments": [asdict(moment) for moment in moments.values()],
    }
    STATE_MOMENTS_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

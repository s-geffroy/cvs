"""Aggregate civilizational indicators derived from the GP continuous field.

Three scalar fields summarising the 19-component continuous field. They are
designed to be read in two distinct regimes:

- **Paired regime (2.1 ⊕ 3.1)** — :func:`affinity_entropy_inverse_field` and
  :func:`deformation_trace_field` are complementary: the first measures
  *identity sharpness* (is one civilization clearly dominant here?), the
  second measures *spatial texture* (does the field change rapidly here?).
  A user must consult both to disambiguate the four quadrants of the
  (identity × tension) plane — see doc 17 §4.4.1.

- **Standalone regime (2.2)** — :func:`classification_margin_field` collapses
  position, identity and frontier into a single signed scalar via the
  geometry of civilization centroids in ``B_score``: high = deep in a core,
  near zero = equidistant from two cores (= fault line). Self-sufficient.

All three operate on dense grids produced by
``apps.basis_builder.field.train_v2`` — no GP refit.
"""
from __future__ import annotations

from collections.abc import Mapping

import numpy as np

X_SCORE_COMPONENT_NAMES: tuple[str, ...] = (
    "x_score_pdi",
    "x_score_idv",
    "x_score_mas",
    "x_score_uai",
    "x_score_lto",
    "x_score_ivr",
)


def affinity_entropy_inverse_field(
    affinity_predicted_mean_by_civilization: Mapping[str, np.ndarray],
) -> np.ndarray:
    """Indicator 2.1 — ``1 − H(p) / log K`` where K is the number of civilizations.

    The GP does not preserve the simplex constraint on the affinity vector
    (predicted means can be slightly negative and need not sum to one). We
    clamp to non-negative, renormalise per cell, then compute the Shannon
    entropy with the convention ``0·log 0 = 0``.

    Returns a field in ``[0, 1]``: ``1`` = pure identity (a single
    civilization dominates), ``0`` = maximally interstitial (uniform across
    K civilizations).
    """
    civilization_ids_ordered = list(affinity_predicted_mean_by_civilization.keys())
    number_of_civilizations = len(civilization_ids_ordered)
    if number_of_civilizations < 2:
        raise ValueError(
            "Need at least two civilizations to compute an entropy "
            f"(got {number_of_civilizations})."
        )

    affinity_stacked = np.stack(
        [
            np.asarray(affinity_predicted_mean_by_civilization[civilization_id])
            for civilization_id in civilization_ids_ordered
        ],
        axis=-1,
    )
    affinity_clamped = np.maximum(affinity_stacked, 0.0)
    row_sum = np.sum(affinity_clamped, axis=-1, keepdims=True)
    safe_row_sum = np.where(row_sum > 1e-12, row_sum, 1.0)
    probabilities = affinity_clamped / safe_row_sum

    safe_probabilities = np.where(probabilities > 0.0, probabilities, 1.0)
    log_probabilities = np.where(
        probabilities > 0.0, np.log(safe_probabilities), 0.0
    )
    shannon_entropy = -np.sum(probabilities * log_probabilities, axis=-1)
    return 1.0 - shannon_entropy / np.log(number_of_civilizations)


def deformation_trace_field(
    gradient_magnitude_by_component: Mapping[str, np.ndarray],
    z_score_std_by_component: Mapping[str, float] | None = None,
) -> np.ndarray:
    """Indicator 3.1 — ``tr(G(p)) = Σ_c ‖∇x_c‖²`` over the 19 components.

    ``gradient_magnitude`` already encodes the spherically-corrected norm
    ``√((∂μ/∂λ)²/cos²φ + (∂μ/∂φ)²)`` (cf. ``train_v2.py`` lines 239-242),
    so ``tr(G)`` reduces to a sum of squares.

    When ``z_score_std_by_component`` is supplied (one std per component),
    each gradient magnitude is rescaled to its z-score units before squaring:
    ``Σ_c (‖∇x_c‖ / σ_c)²``. This balances the contribution of every cultural
    axis — without this rescaling, Hofstede dimensions (σ ≈ 10–25) crush
    Inglehart-Welzel (σ ≈ 0.6) and the affinity components (σ ≈ 0.1) in the
    raw sum. The z-score-normalised form is what produces a faithful
    "civilizational tension" indicator that integrates all 19 axes on equal
    footing.

    The polar mask (NaN at ``|φ| ≥ 75°``) is inherited unchanged through the
    sum. Output has the same shape as the input grids and is non-negative.
    """
    component_names = list(gradient_magnitude_by_component.keys())
    if not component_names:
        raise ValueError("Need at least one component to compute tr(G).")
    accumulator = np.zeros_like(
        np.asarray(gradient_magnitude_by_component[component_names[0]]),
        dtype=np.float64,
    )
    for component_name in component_names:
        gradient_magnitude = np.asarray(
            gradient_magnitude_by_component[component_name], dtype=np.float64
        )
        if z_score_std_by_component is not None:
            std = float(z_score_std_by_component.get(component_name, 1.0))
            if std <= 0.0:
                raise ValueError(
                    f"z_score_std_by_component[{component_name!r}] must be > 0; "
                    f"got {std}"
                )
            gradient_magnitude = gradient_magnitude / std
        accumulator = accumulator + gradient_magnitude ** 2
    return accumulator


def classification_margin_field(
    x_score_field_by_component: Mapping[str, np.ndarray],
    centroid_mu_scores: np.ndarray,
    covariance_inverse: np.ndarray,
) -> np.ndarray:
    """Indicator 2.2 — ``(d₂ − d₁) / d₁`` Davies-Bouldin-local classification margin.

    For each grid cell, the Mahalanobis distance to each civilization centroid
    is computed in ``B_score`` using the supplied ``covariance_inverse`` (by
    convention the intra-civilizational pooled covariance produced by
    :func:`civvec_core.algebra.distances.intra_civilizational_covariance_inverse`,
    consistent with the project-wide robust default).

    The output is ``≥ 0``: large values mean the cell sits deep in a single
    civilization core (the second-nearest centroid is much further than the
    nearest); values approaching zero mark fault lines where two centroids
    are nearly equidistant.

    Parameters
    ----------
    x_score_field_by_component
        Must contain the six keys listed in :data:`X_SCORE_COMPONENT_NAMES`.
    centroid_mu_scores
        Shape ``(K, 6)`` — civilization centroid means in B_score.
    covariance_inverse
        Shape ``(6, 6)`` — inverse of the chosen B_score covariance.
    """
    missing = [
        component_name
        for component_name in X_SCORE_COMPONENT_NAMES
        if component_name not in x_score_field_by_component
    ]
    if missing:
        raise KeyError(
            f"x_score_field_by_component missing required components: {missing}"
        )

    x_score_stacked = np.stack(
        [
            np.asarray(x_score_field_by_component[component_name], dtype=np.float64)
            for component_name in X_SCORE_COMPONENT_NAMES
        ],
        axis=-1,
    )

    centroids_array = np.asarray(centroid_mu_scores, dtype=np.float64)
    if centroids_array.ndim != 2 or centroids_array.shape[1] != 6:
        raise ValueError(
            f"centroid_mu_scores must have shape (K, 6); got {centroids_array.shape}"
        )

    covariance_inverse_array = np.asarray(covariance_inverse, dtype=np.float64)
    if covariance_inverse_array.shape != (6, 6):
        raise ValueError(
            f"covariance_inverse must have shape (6, 6); got "
            f"{covariance_inverse_array.shape}"
        )

    differences_to_centroids = (
        x_score_stacked[..., None, :] - centroids_array[None, None, :, :]
    )
    quadratic_form = np.einsum(
        "...ki,ij,...kj->...k",
        differences_to_centroids,
        covariance_inverse_array,
        differences_to_centroids,
    )
    mahalanobis_distances = np.sqrt(np.maximum(quadratic_form, 0.0))

    distances_sorted_ascending = np.sort(mahalanobis_distances, axis=-1)
    nearest_distance = distances_sorted_ascending[..., 0]
    second_nearest_distance = distances_sorted_ascending[..., 1]
    safe_nearest = np.where(nearest_distance > 1e-12, nearest_distance, np.nan)
    return (second_nearest_distance - nearest_distance) / safe_nearest

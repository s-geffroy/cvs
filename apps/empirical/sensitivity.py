"""Sensitivity analysis for the civilizational basis (doc 13).

Three independent sensitivities are computed:

1. **Leave-one-out (LOO)** on archetype states for each civilization centroid:
   for each (civilization, archetype) pair, recompute the centroid without
   that archetype and report the displacement in ``B_score`` and ``B_viz``.
2. **Sweep over β** (softmax inverse-distance temperature): for
   ``β ∈ {0.01, 0.025, 0.05, 0.1, 0.2}`` recompute the affinity vector
   ``w_s`` for every state and report the mean affinity entropy and the
   fraction of states whose ``argmax`` civilization changes vs the default.
3. **Sweep over hybrid weights (α, β, γ)** on a discretised simplex grid:
   recompute the panel-median-normalised hybrid distance matrix and report
   the Spearman rank correlation of pairwise distances vs the default
   (0.4, 0.4, 0.2).
"""
from __future__ import annotations

import json

import numpy as np

from apps.basis_builder.centroids import (
    ROLE_WEIGHT,
    CivilizationCentroid,
    _to_list,
    _weighted_mean_and_cov,
    compute_centroids,
)
from apps.basis_builder.load_hofstede import HOFSTEDE_DIMENSION_ORDER, load_hofstede
from apps.basis_builder.load_iw import load_inglehart_welzel
from apps.basis_builder.moments import compute_second_moment
from apps.basis_builder.paths import EMPIRICAL_DIR, MACRO_CIVILIZATIONS_V2_PATH
from apps.basis_builder.projector import (
    DEFAULT_AFFINITY_BETA,
    project_states,
    softmax_affinity,
)


def _euclidean(point_a: np.ndarray, point_b: np.ndarray) -> float:
    diff = point_a - point_b
    return float(np.sqrt(float(diff @ diff)))


def _aggregate_civilization_centroid(
    civilization_id: str,
    member_states: list[dict],
    iw_coords: dict,
    hofstede_profiles: dict,
) -> CivilizationCentroid | None:
    """Aggregate a civilization centroid from an arbitrary member-state list.

    Mirrors the logic in ``apps.basis_builder.centroids.compute_centroids`` but
    operates on a caller-provided member list (for LOO).
    """
    viz_points: list[np.ndarray] = []
    viz_weights: list[float] = []
    score_points: list[np.ndarray] = []
    score_weights: list[float] = []
    contributing_states: list[dict] = []
    iw_states_used = 0
    hofstede_states_used = 0

    for member_record in member_states:
        iso3 = member_record["iso3"]
        role_weight = ROLE_WEIGHT.get(member_record["role"], 0.0)
        if role_weight == 0.0:
            continue

        iw_record = iw_coords.get(iso3)
        if iw_record is not None:
            viz_points.append(np.array([iw_record.ts, iw_record.se], dtype=float))
            viz_weights.append(role_weight)
            iw_states_used += 1

        hofstede_record = hofstede_profiles.get(iso3)
        if hofstede_record is not None and hofstede_record.coverage != "missing":
            mean_fill = np.nanmean(hofstede_record.values)
            score_values = np.where(np.isnan(hofstede_record.values), mean_fill, hofstede_record.values)
            score_points.append(score_values)
            score_weights.append(role_weight)
            hofstede_states_used += 1

        contributing_states.append(
            {"iso3": iso3, "weight": role_weight, "role": member_record["role"]}
        )

    viz_array = np.array(viz_points) if viz_points else np.empty((0, 2))
    viz_weight_array = np.array(viz_weights) if viz_weights else np.empty(0)
    mu_viz, sigma_viz = _weighted_mean_and_cov(viz_array, viz_weight_array)

    score_array = np.array(score_points) if score_points else np.empty((0, 6))
    score_weight_array = np.array(score_weights) if score_weights else np.empty(0)
    mu_score, sigma_score_full = _weighted_mean_and_cov(score_array, score_weight_array)
    sigma_score = np.sqrt(np.maximum(np.diag(sigma_score_full), 0.0))

    return CivilizationCentroid(
        civilization_id=civilization_id,
        mu_viz=_to_list(mu_viz),
        sigma_viz=_to_list(sigma_viz),
        mu_score=_to_list(mu_score),
        sigma_score=_to_list(sigma_score),
        member_states=contributing_states,
        low_archetype_coverage=max(iw_states_used, hofstede_states_used) < 3,
        computed_from_n_states=max(iw_states_used, hofstede_states_used),
        evidence_basis={
            "iw_states_used": iw_states_used,
            "hofstede_states_used": hofstede_states_used,
        },
    )


def leave_one_out_on_archetypes() -> dict:
    """For each civilization, recompute mu_score / mu_viz omitting each archetype state."""
    iw_coords = load_inglehart_welzel()
    hofstede_profiles = load_hofstede()
    taxonomy = json.loads(MACRO_CIVILIZATIONS_V2_PATH.read_text())

    loo_results: list[dict] = []
    for civilization in taxonomy["civilizations"]:
        civilization_id = civilization["id"]
        member_states = civilization["member_states"]
        baseline_centroid = _aggregate_civilization_centroid(
            civilization_id, member_states, iw_coords, hofstede_profiles
        )
        if baseline_centroid is None:
            continue
        baseline_mu_score = np.asarray(
            [value if value is not None else np.nan for value in baseline_centroid.mu_score],
            dtype=float,
        )
        baseline_mu_viz = np.asarray(
            [value if value is not None else np.nan for value in baseline_centroid.mu_viz],
            dtype=float,
        )

        archetype_displacements: list[dict] = []
        for member_record in member_states:
            omitted_iso3 = member_record["iso3"]
            remaining_members = [
                other_record for other_record in member_states
                if other_record["iso3"] != omitted_iso3
            ]
            if not remaining_members:
                continue
            recomputed_centroid = _aggregate_civilization_centroid(
                civilization_id, remaining_members, iw_coords, hofstede_profiles
            )
            if recomputed_centroid is None:
                continue
            recomputed_mu_score = np.asarray(
                [value if value is not None else np.nan for value in recomputed_centroid.mu_score],
                dtype=float,
            )
            recomputed_mu_viz = np.asarray(
                [value if value is not None else np.nan for value in recomputed_centroid.mu_viz],
                dtype=float,
            )

            valid_score_mask = ~np.isnan(baseline_mu_score) & ~np.isnan(recomputed_mu_score)
            mu_score_displacement = (
                _euclidean(baseline_mu_score[valid_score_mask], recomputed_mu_score[valid_score_mask])
                if valid_score_mask.any()
                else float("nan")
            )
            valid_viz_mask = ~np.isnan(baseline_mu_viz) & ~np.isnan(recomputed_mu_viz)
            mu_viz_displacement = (
                _euclidean(baseline_mu_viz[valid_viz_mask], recomputed_mu_viz[valid_viz_mask])
                if valid_viz_mask.any()
                else float("nan")
            )

            archetype_displacements.append(
                {
                    "omitted_iso3": omitted_iso3,
                    "role": member_record["role"],
                    "mu_score_displacement": mu_score_displacement,
                    "mu_viz_displacement": mu_viz_displacement,
                }
            )

        archetype_displacements.sort(
            key=lambda record: (record["mu_score_displacement"]
                                if not np.isnan(record["mu_score_displacement"]) else -1.0),
            reverse=True,
        )
        loo_results.append(
            {
                "civilization_id": civilization_id,
                "archetype_displacements": archetype_displacements,
                "max_score_displacement": (
                    archetype_displacements[0]["mu_score_displacement"]
                    if archetype_displacements else 0.0
                ),
            }
        )

    return {
        "_meta": {
            "method": "leave_one_out_archetype",
            "dimension_order_score": list(HOFSTEDE_DIMENSION_ORDER),
            "weighting_scheme": "role_default (core=1, periphery=0.5, ambiguous=0)",
        },
        "civilizations": loo_results,
    }


def sweep_beta_softmax(
    beta_values: tuple[float, ...] = (0.01, 0.025, 0.05, 0.1, 0.2),
) -> dict:
    """Recompute affinity vectors w_s under varying softmax temperatures."""
    centroids = compute_centroids()
    state_coordinates = project_states(centroids)
    civilization_ids = list(centroids.keys())

    per_beta_results: list[dict] = []
    argmax_at_default: dict[str, str] = {}
    for beta_value in beta_values:
        per_state_records: list[dict] = []
        entropy_values: list[float] = []
        argmax_this_beta: dict[str, str] = {}
        for iso3, state in state_coordinates.items():
            if any(value is None for value in state.x_score):
                continue
            x_score = np.array(state.x_score, dtype=float)
            affinity_vector = softmax_affinity(x_score, centroids, beta=beta_value)
            weight_array = np.array(
                [affinity_vector[civilization_id] for civilization_id in civilization_ids],
                dtype=float,
            )
            with np.errstate(divide="ignore", invalid="ignore"):
                positive_weights = weight_array[weight_array > 0]
                entropy_value = float(-np.sum(positive_weights * np.log(positive_weights)))
            argmax_civilization = civilization_ids[int(np.argmax(weight_array))]
            argmax_this_beta[iso3] = argmax_civilization
            per_state_records.append(
                {
                    "iso3": iso3,
                    "argmax_civilization": argmax_civilization,
                    "max_weight": float(weight_array.max()),
                    "entropy": entropy_value,
                }
            )
            entropy_values.append(entropy_value)
        per_beta_results.append(
            {
                "beta": beta_value,
                "mean_entropy": float(np.mean(entropy_values)) if entropy_values else 0.0,
                "median_max_weight": (
                    float(np.median([entry["max_weight"] for entry in per_state_records]))
                    if per_state_records else 0.0
                ),
                "n_states": len(per_state_records),
            }
        )
        if np.isclose(beta_value, DEFAULT_AFFINITY_BETA):
            argmax_at_default = argmax_this_beta

    if argmax_at_default:
        argmax_agreement: list[dict] = []
        for beta_value in beta_values:
            argmax_this_beta = {}
            for iso3, state in state_coordinates.items():
                if any(value is None for value in state.x_score):
                    continue
                x_score = np.array(state.x_score, dtype=float)
                affinity_vector = softmax_affinity(x_score, centroids, beta=beta_value)
                weight_array = np.array(
                    [affinity_vector[civilization_id] for civilization_id in civilization_ids],
                    dtype=float,
                )
                argmax_this_beta[iso3] = civilization_ids[int(np.argmax(weight_array))]
            common_iso3s = set(argmax_this_beta) & set(argmax_at_default)
            agreement = (
                sum(1 for iso3 in common_iso3s
                    if argmax_this_beta[iso3] == argmax_at_default[iso3]) / len(common_iso3s)
            ) if common_iso3s else float("nan")
            argmax_agreement.append({"beta": beta_value, "fraction_argmax_matches_default": agreement})
    else:
        argmax_agreement = []

    return {
        "_meta": {
            "method": "softmax_beta_sweep",
            "default_beta": DEFAULT_AFFINITY_BETA,
            "civilization_id_order": civilization_ids,
        },
        "per_beta": per_beta_results,
        "argmax_agreement_with_default": argmax_agreement,
    }


def _rank_correlation_spearman(values_a: np.ndarray, values_b: np.ndarray) -> float:
    if values_a.shape != values_b.shape or values_a.size < 3:
        return float("nan")
    rank_a = np.argsort(np.argsort(values_a)).astype(float)
    rank_b = np.argsort(np.argsort(values_b)).astype(float)
    rank_a -= rank_a.mean()
    rank_b -= rank_b.mean()
    denominator = float(np.sqrt(float(rank_a @ rank_a) * float(rank_b @ rank_b)))
    if denominator < 1e-12:
        return float("nan")
    return float(rank_a @ rank_b / denominator)


def sweep_hybrid_weights(grid_step: float = 0.1) -> dict:
    """Sweep (alpha, beta, gamma) on a simplex grid and report Spearman rho to default."""
    from packages.civvec_core.algebra.distances import (
        HybridWeights,
        civilization_ground_cost_squared,
        d_M_frobenius,
        d_score_mahalanobis_intra,
        d_w_wasserstein,
        intra_civilizational_covariance_inverse,
        normalise_distances_by_panel_median,
    )

    centroids = compute_centroids()
    state_coordinates = project_states(centroids)
    civilization_ids = list(centroids.keys())

    centroid_mu_array = np.array(
        [[value if value is not None else 50.0
          for value in centroids[civilization_id].mu_score]
         for civilization_id in civilization_ids],
        dtype=float,
    )
    centroid_sigma_array = np.array(
        [[value if value is not None else 0.0
          for value in (centroids[civilization_id].sigma_score or [0.0] * 6)]
         for civilization_id in civilization_ids],
        dtype=float,
    )
    ground_cost_squared = civilization_ground_cost_squared(centroid_mu_array)
    covariance_inverse_intra = intra_civilizational_covariance_inverse(centroid_sigma_array)

    eligible_iso3s: list[str] = []
    x_score_records: list[np.ndarray] = []
    affinity_records: list[np.ndarray] = []
    moment_records: list[np.ndarray] = []
    for iso3, state in state_coordinates.items():
        if any(value is None for value in state.x_score):
            continue
        if any(value is None for value in state.x_viz):
            continue
        moment_record = compute_second_moment(state, centroids)
        if moment_record is None:
            continue
        eligible_iso3s.append(iso3)
        x_score_records.append(np.array(state.x_score, dtype=float))
        affinity_records.append(
            np.array([state.affinity_vector[civilization_id]
                      for civilization_id in civilization_ids], dtype=float)
        )
        moment_records.append(np.array(moment_record.M, dtype=float))

    n_states = len(eligible_iso3s)
    if n_states < 2:
        return {
            "_meta": {"method": "hybrid_sweep", "n_states": n_states},
            "grid_results": [],
        }

    d_score_intra_matrix = np.zeros((n_states, n_states))
    d_wasserstein_matrix = np.zeros((n_states, n_states))
    d_moment_frobenius_matrix = np.zeros((n_states, n_states))
    for left in range(n_states):
        for right in range(left + 1, n_states):
            d_score_intra_matrix[left, right] = d_score_mahalanobis_intra(
                x_score_records[left], x_score_records[right], covariance_inverse_intra
            )
            d_wasserstein_matrix[left, right] = d_w_wasserstein(
                affinity_records[left], affinity_records[right], ground_cost_squared
            )
            d_moment_frobenius_matrix[left, right] = d_M_frobenius(
                moment_records[left], moment_records[right]
            )
            d_score_intra_matrix[right, left] = d_score_intra_matrix[left, right]
            d_wasserstein_matrix[right, left] = d_wasserstein_matrix[left, right]
            d_moment_frobenius_matrix[right, left] = d_moment_frobenius_matrix[left, right]

    normalised_intra = normalise_distances_by_panel_median(d_score_intra_matrix)
    normalised_wasserstein = normalise_distances_by_panel_median(d_wasserstein_matrix)
    normalised_moment = normalise_distances_by_panel_median(d_moment_frobenius_matrix)

    upper_triangle_indices = np.triu_indices(n_states, k=1)
    default_weights = HybridWeights()
    default_hybrid_matrix = (
        default_weights.alpha * normalised_intra
        + default_weights.beta * normalised_wasserstein
        + default_weights.gamma * normalised_moment
    )
    default_upper_triangle_values = default_hybrid_matrix[upper_triangle_indices]

    grid_results: list[dict] = []
    step_count = int(round(1.0 / grid_step))
    for alpha_index in range(step_count + 1):
        alpha_value = alpha_index * grid_step
        for beta_index in range(step_count + 1 - alpha_index):
            beta_value = beta_index * grid_step
            gamma_value = 1.0 - alpha_value - beta_value
            if gamma_value < -1e-9:
                continue
            gamma_value = max(0.0, gamma_value)
            hybrid_matrix = (
                alpha_value * normalised_intra
                + beta_value * normalised_wasserstein
                + gamma_value * normalised_moment
            )
            spearman_rho = _rank_correlation_spearman(
                hybrid_matrix[upper_triangle_indices], default_upper_triangle_values
            )
            grid_results.append(
                {
                    "alpha": float(alpha_value),
                    "beta": float(beta_value),
                    "gamma": float(gamma_value),
                    "spearman_rho_vs_default": spearman_rho,
                }
            )

    return {
        "_meta": {
            "method": "hybrid_weights_sweep",
            "n_states": n_states,
            "grid_step": grid_step,
            "default_weights": {
                "alpha": default_weights.alpha,
                "beta": default_weights.beta,
                "gamma": default_weights.gamma,
            },
        },
        "iso3_order": eligible_iso3s,
        "grid_results": grid_results,
    }


def sweep_role_weights(
    periphery_weight_values: tuple[float, ...] = (0.0, 0.25, 0.5, 0.75, 1.0),
) -> dict:
    """Recompute civilization centroids under varying ``periphery`` archetype weight.

    Reports the maximum displacement in ``B_score`` of each centroid relative
    to the default (periphery=0.5) — a direct measure of sensitivity to the
    editorial periphery-vs-core weighting choice.
    """
    iw_coords = load_inglehart_welzel()
    hofstede_profiles = load_hofstede()
    taxonomy = json.loads(MACRO_CIVILIZATIONS_V2_PATH.read_text())

    default_periphery_weight = 0.5
    per_periphery_results: list[dict] = []
    default_mu_score_by_civilization: dict[str, np.ndarray] = {}

    for periphery_weight in periphery_weight_values:
        custom_role_weights = {"core": 1.0, "periphery": float(periphery_weight),
                               "interface": 0.0, "ambiguous": 0.0}
        civilization_records: list[dict] = []
        for civilization in taxonomy["civilizations"]:
            civilization_id = civilization["id"]
            viz_points: list[np.ndarray] = []
            viz_weights: list[float] = []
            score_points: list[np.ndarray] = []
            score_weights: list[float] = []
            for member_record in civilization["member_states"]:
                role_weight_value = custom_role_weights.get(member_record["role"], 0.0)
                if role_weight_value == 0.0:
                    continue
                iso3 = member_record["iso3"]
                iw_record = iw_coords.get(iso3)
                if iw_record is not None:
                    viz_points.append(np.array([iw_record.ts, iw_record.se], dtype=float))
                    viz_weights.append(role_weight_value)
                hofstede_record = hofstede_profiles.get(iso3)
                if hofstede_record is not None and hofstede_record.coverage != "missing":
                    mean_fill = np.nanmean(hofstede_record.values)
                    values = np.where(np.isnan(hofstede_record.values), mean_fill, hofstede_record.values)
                    score_points.append(values)
                    score_weights.append(role_weight_value)
            if score_points and score_weights:
                weight_sum = sum(score_weights)
                weights_array = np.array(score_weights, dtype=float) / weight_sum
                mu_score = np.average(score_points, axis=0, weights=weights_array)
            else:
                mu_score = np.full(6, np.nan)
            civilization_records.append({
                "civilization_id": civilization_id,
                "mu_score": [float(v) if not np.isnan(v) else None for v in mu_score],
            })
            if np.isclose(periphery_weight, default_periphery_weight):
                default_mu_score_by_civilization[civilization_id] = mu_score

        per_periphery_results.append({
            "periphery_weight": float(periphery_weight),
            "centroids": civilization_records,
        })

    sensitivity_results: list[dict] = []
    for record in per_periphery_results:
        peripheryweight = record["periphery_weight"]
        displacements: dict[str, float] = {}
        for civilization in record["centroids"]:
            civilization_id = civilization["civilization_id"]
            mu_score_array = np.array(
                [v if v is not None else np.nan for v in civilization["mu_score"]],
                dtype=float,
            )
            default_mu_score = default_mu_score_by_civilization.get(civilization_id)
            if default_mu_score is None:
                continue
            valid_mask = ~np.isnan(mu_score_array) & ~np.isnan(default_mu_score)
            if valid_mask.any():
                displacement = float(np.linalg.norm(
                    mu_score_array[valid_mask] - default_mu_score[valid_mask]
                ))
            else:
                displacement = float("nan")
            displacements[civilization_id] = displacement
        sensitivity_results.append({
            "periphery_weight": peripheryweight,
            "centroid_displacements_vs_default": displacements,
            "max_displacement": max(
                [v for v in displacements.values() if not np.isnan(v)],
                default=0.0,
            ),
        })

    return {
        "_meta": {
            "method": "role_weight_sweep_on_periphery",
            "default_periphery_weight": default_periphery_weight,
            "core_weight_fixed": 1.0,
            "ambiguous_weight_fixed": 0.0,
        },
        "sensitivity": sensitivity_results,
    }


def correlation_d_viz_vs_d_score() -> dict:
    """Spearman rank correlation between d_viz and d_score_euclidean across all state pairs.

    Quantifies whether the two-base mix (IW + Hofstede) is internally
    consistent: a high correlation means the two bases agree on which states
    are close; a low correlation indicates that the bases capture different
    cultural dimensions (and the mixed pipeline is informationally richer).
    """
    from packages.civvec_core.algebra.distances import d_score_euclidean, d_viz

    centroids = compute_centroids()
    state_coordinates = project_states(centroids)

    iso3_list: list[str] = []
    x_viz_records: list[np.ndarray] = []
    x_score_records: list[np.ndarray] = []
    for iso3, state in state_coordinates.items():
        if any(value is None for value in state.x_viz):
            continue
        if any(value is None for value in state.x_score):
            continue
        iso3_list.append(iso3)
        x_viz_records.append(np.array(state.x_viz, dtype=float))
        x_score_records.append(np.array(state.x_score, dtype=float))

    n_states = len(iso3_list)
    d_viz_values: list[float] = []
    d_score_values: list[float] = []
    for left in range(n_states):
        for right in range(left + 1, n_states):
            d_viz_values.append(d_viz(x_viz_records[left], x_viz_records[right]))
            d_score_values.append(d_score_euclidean(x_score_records[left], x_score_records[right]))

    d_viz_array = np.asarray(d_viz_values, dtype=float)
    d_score_array = np.asarray(d_score_values, dtype=float)
    spearman_rho = _rank_correlation_spearman(d_viz_array, d_score_array)

    return {
        "_meta": {
            "method": "cross_base_pairwise_correlation",
            "n_states_paired": n_states,
            "n_pairs": len(d_viz_values),
        },
        "spearman_rho_d_viz_vs_d_score_euclidean": spearman_rho,
        "interpretation": (
            "rho > 0.7: the two bases largely agree (B_viz and B_score capture overlapping signal);"
            " rho in [0.4, 0.7]: moderate agreement, complementary information;"
            " rho < 0.4: bases diverge — the mixed pipeline is informationally richer"
            " but mixing pommes/oranges is more salient (cf. doc 11 section B5)."
        ),
    }


def run_all_sensitivity_analyses() -> dict[str, str]:
    EMPIRICAL_DIR.mkdir(parents=True, exist_ok=True)
    paths_written: dict[str, str] = {}

    loo_payload = leave_one_out_on_archetypes()
    loo_path = EMPIRICAL_DIR / "sensitivity_leave_one_out.json"
    loo_path.write_text(json.dumps(loo_payload, indent=2, ensure_ascii=False))
    paths_written["leave_one_out"] = str(loo_path)

    beta_payload = sweep_beta_softmax()
    beta_path = EMPIRICAL_DIR / "sensitivity_beta_sweep.json"
    beta_path.write_text(json.dumps(beta_payload, indent=2, ensure_ascii=False))
    paths_written["beta_sweep"] = str(beta_path)

    hybrid_payload = sweep_hybrid_weights()
    hybrid_path = EMPIRICAL_DIR / "sensitivity_hybrid_weights.json"
    hybrid_path.write_text(json.dumps(hybrid_payload, indent=2, ensure_ascii=False))
    paths_written["hybrid_sweep"] = str(hybrid_path)

    role_weights_payload = sweep_role_weights()
    role_weights_path = EMPIRICAL_DIR / "sensitivity_role_weights.json"
    role_weights_path.write_text(json.dumps(role_weights_payload, indent=2, ensure_ascii=False))
    paths_written["role_weights"] = str(role_weights_path)

    cross_base_payload = correlation_d_viz_vs_d_score()
    cross_base_path = EMPIRICAL_DIR / "sensitivity_cross_base_correlation.json"
    cross_base_path.write_text(json.dumps(cross_base_payload, indent=2, ensure_ascii=False))
    paths_written["cross_base_correlation"] = str(cross_base_path)

    return paths_written

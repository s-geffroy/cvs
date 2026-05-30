"""Compute civilization centroids in B_viz (R^2) and B_score (R^6).

For each macro-civilization, aggregate over its archetype member states (role=core, weight=1;
role=periphery, weight=0.5; role=ambiguous/interface excluded) and emit:
- mu_viz (2,), sigma_viz (2x2 covariance)
- mu_score (6,), sigma_score (6,) per-axis std-deviation
- list of contributing states + computed_from_n_states
- low_archetype_coverage flag (propagated from taxonomy)
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from .load_hofstede import HOFSTEDE_DIMENSION_ORDER, load_hofstede
from .load_iw import load_inglehart_welzel
from .paths import CIVILIZATION_CENTROIDS_PATH, MACRO_CIVILIZATIONS_V2_PATH

ROLE_WEIGHT: dict[str, float] = {
    "core": 1.0,
    "periphery": 0.5,
    "interface": 0.0,
    "ambiguous": 0.0,
}


@dataclass
class CivilizationCentroid:
    civilization_id: str
    mu_viz: list[float]
    sigma_viz: list[list[float]]
    mu_score: list[float]
    sigma_score: list[float]
    member_states: list[dict[str, Any]]
    low_archetype_coverage: bool
    computed_from_n_states: int
    evidence_basis: dict[str, int]


def _weighted_mean_and_cov(
    points: np.ndarray, weights: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Return weighted mean (d,) and weighted covariance (d, d)."""
    weight_sum = float(np.sum(weights))
    if weight_sum == 0.0 or points.size == 0:
        dim = points.shape[1] if points.ndim == 2 else 1
        return np.full(dim, np.nan), np.zeros((dim, dim))
    mean = np.average(points, axis=0, weights=weights)
    centered = points - mean
    cov = (centered.T @ (centered * weights[:, None])) / weight_sum
    return mean, cov


def compute_centroids() -> dict[str, CivilizationCentroid]:
    """Compute centroids for the 11 macro-civilizations."""
    iw_coords = load_inglehart_welzel()
    hofstede_profiles = load_hofstede()
    taxonomy = json.loads(MACRO_CIVILIZATIONS_V2_PATH.read_text())

    centroids: dict[str, CivilizationCentroid] = {}
    for civ in taxonomy["civilizations"]:
        civilization_id = civ["id"]
        viz_points: list[np.ndarray] = []
        viz_weights: list[float] = []
        score_points: list[np.ndarray] = []
        score_weights: list[float] = []
        contributing_states: list[dict[str, Any]] = []
        iw_states_used = 0
        hofstede_states_used = 0

        for member in civ["member_states"]:
            iso3 = member["iso3"]
            role_weight = ROLE_WEIGHT.get(member["role"], 0.0)
            if role_weight == 0.0:
                continue

            iw = iw_coords.get(iso3)
            if iw is not None:
                viz_points.append(np.array([iw.ts, iw.se], dtype=float))
                viz_weights.append(role_weight)
                iw_states_used += 1

            hof = hofstede_profiles.get(iso3)
            if hof is not None and hof.coverage != "missing":
                mean_fill = np.nanmean(hof.values)
                values = np.where(np.isnan(hof.values), mean_fill, hof.values)
                score_points.append(values)
                score_weights.append(role_weight)
                hofstede_states_used += 1

            contributing_states.append(
                {"iso3": iso3, "weight": role_weight, "role": member["role"]}
            )

        viz_arr = np.array(viz_points) if viz_points else np.empty((0, 2))
        viz_w_arr = np.array(viz_weights) if viz_weights else np.empty(0)
        mu_viz, sigma_viz = _weighted_mean_and_cov(viz_arr, viz_w_arr)

        score_arr = np.array(score_points) if score_points else np.empty((0, 6))
        score_w_arr = np.array(score_weights) if score_weights else np.empty(0)
        mu_score, sigma_score_full = _weighted_mean_and_cov(score_arr, score_w_arr)
        sigma_score = np.sqrt(np.maximum(np.diag(sigma_score_full), 0.0))

        n_contrib = max(iw_states_used, hofstede_states_used)
        low_coverage = bool(civ.get("low_archetype_coverage", False)) or n_contrib < 3

        centroids[civilization_id] = CivilizationCentroid(
            civilization_id=civilization_id,
            mu_viz=_to_list(mu_viz),
            sigma_viz=_to_list(sigma_viz),
            mu_score=_to_list(mu_score),
            sigma_score=_to_list(sigma_score),
            member_states=contributing_states,
            low_archetype_coverage=low_coverage,
            computed_from_n_states=n_contrib,
            evidence_basis={
                "iw_states_used": iw_states_used,
                "hofstede_states_used": hofstede_states_used,
            },
        )
    return centroids


def _to_list(arr: np.ndarray) -> list:
    """Convert NaN to None for JSON-friendly output."""
    if arr.ndim == 1:
        return [None if (isinstance(x, float) and np.isnan(x)) else float(x) for x in arr]
    return [[None if np.isnan(x) else float(x) for x in row] for row in arr]


def write_centroids(centroids: dict[str, CivilizationCentroid]) -> None:
    CIVILIZATION_CENTROIDS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "schema": "civilization_centroid.schema.json",
            "dimension_order_score": list(HOFSTEDE_DIMENSION_ORDER),
        },
        "centroids": [asdict(c) for c in centroids.values()],
    }
    CIVILIZATION_CENTROIDS_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def inject_centroid_coords_into_taxonomy(
    centroids: dict[str, CivilizationCentroid],
) -> None:
    """Inject mu_viz, sigma_viz, mu_score, sigma_score into macro_civilizations.v2.json in place."""
    taxonomy = json.loads(MACRO_CIVILIZATIONS_V2_PATH.read_text())
    for civ in taxonomy["civilizations"]:
        centroid = centroids.get(civ["id"])
        if centroid is None:
            continue
        civ["mu_viz"] = centroid.mu_viz
        civ["sigma_viz"] = centroid.sigma_viz
        civ["mu_score"] = centroid.mu_score
        civ["sigma_score"] = centroid.sigma_score
    MACRO_CIVILIZATIONS_V2_PATH.write_text(json.dumps(taxonomy, indent=2, ensure_ascii=False))

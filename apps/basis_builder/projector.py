"""Project each sovereign state into B_viz and B_score, derive affinity vector.

Affinity vector is computed via softmax inverse-distance in B_score:
  w_s[i] = exp(-beta * d(x_s^score, mu_i^score)) / Z
where Z normalises over the 11 civilizations.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from .centroids import CivilizationCentroid, compute_centroids
from .load_hofstede import HOFSTEDE_DIMENSION_ORDER, load_hofstede
from .load_iw import load_inglehart_welzel
from .paths import STATE_COORDINATES_PATH

DEFAULT_AFFINITY_BETA: float = 0.05


@dataclass
class StateCoordinates:
    iso3: str
    label: str | None
    x_viz: list[float | None]
    x_viz_ellipse: dict[str, Any] | None
    x_score: list[float | None]
    affinity_vector: dict[str, float]
    data_quality: dict[str, Any]
    source_refs: list[str]


def softmax_affinity(
    x_score: np.ndarray,
    centroids: dict[str, CivilizationCentroid],
    beta: float = DEFAULT_AFFINITY_BETA,
) -> dict[str, float]:
    """Derive simplex weights over civilizations via softmax inverse-distance."""
    if np.any(np.isnan(x_score)):
        return {civ_id: 1.0 / len(centroids) for civ_id in centroids}
    distances: dict[str, float] = {}
    for civ_id, centroid in centroids.items():
        mu = np.array(
            [v if v is not None else np.nan for v in centroid.mu_score], dtype=float
        )
        if np.any(np.isnan(mu)):
            distances[civ_id] = float("inf")
            continue
        distances[civ_id] = float(np.linalg.norm(x_score - mu))
    finite = {k: v for k, v in distances.items() if np.isfinite(v)}
    if not finite:
        return {civ_id: 1.0 / len(centroids) for civ_id in centroids}
    min_d = min(finite.values())
    logits = {k: -beta * (v - min_d) for k, v in finite.items()}
    exp_logits = {k: float(np.exp(v)) for k, v in logits.items()}
    total = sum(exp_logits.values())
    weights = {k: v / total for k, v in exp_logits.items()}
    for civ_id in centroids:
        weights.setdefault(civ_id, 0.0)
    return weights


def project_states(
    centroids: dict[str, CivilizationCentroid] | None = None,
) -> dict[str, StateCoordinates]:
    """Compute B_viz and B_score coordinates for every state observed in IW or Hofstede."""
    if centroids is None:
        centroids = compute_centroids()

    iw_coords = load_inglehart_welzel()
    hofstede_profiles = load_hofstede()
    all_iso3s = set(iw_coords.keys()) | set(hofstede_profiles.keys())

    state_coords: dict[str, StateCoordinates] = {}
    for iso3 in sorted(all_iso3s):
        iw = iw_coords.get(iso3)
        hof = hofstede_profiles.get(iso3)

        if iw is not None:
            x_viz: list[float | None] = [float(iw.ts), float(iw.se)]
            x_viz_ellipse: dict[str, Any] | None = {
                "sigma": [
                    [float(iw.ts_ci ** 2), 0.0],
                    [0.0, float(iw.se_ci ** 2)],
                ],
                "confidence_level": 0.80,
            }
            iw_coverage = "present"
        else:
            x_viz = [None, None]
            x_viz_ellipse = None
            iw_coverage = "missing"

        if hof is not None and hof.coverage != "missing":
            score_values_raw = hof.values
            if np.any(np.isnan(score_values_raw)):
                mean_fill = float(np.nanmean(score_values_raw))
                score_values_filled = np.where(
                    np.isnan(score_values_raw), mean_fill, score_values_raw
                )
                hofstede_coverage = "imputed"
            else:
                score_values_filled = score_values_raw
                hofstede_coverage = "present"
            x_score: list[float | None] = [float(v) for v in score_values_filled]
            affinity_vector = softmax_affinity(score_values_filled, centroids)
        else:
            x_score = [None] * 6
            hofstede_coverage = "missing"
            affinity_vector = {civ_id: 1.0 / len(centroids) for civ_id in centroids}

        low_evidence = iw_coverage == "missing" or hofstede_coverage == "missing"

        state_coords[iso3] = StateCoordinates(
            iso3=iso3,
            label=None,
            x_viz=x_viz,
            x_viz_ellipse=x_viz_ellipse,
            x_score=x_score,
            affinity_vector=affinity_vector,
            data_quality={
                "iw_coverage": iw_coverage,
                "hofstede_coverage": hofstede_coverage,
                "low_evidence": low_evidence,
            },
            source_refs=["wvs_wave7_2022", "hofstede_2010"],
        )
    return state_coords


def write_state_coordinates(state_coords: dict[str, StateCoordinates]) -> None:
    STATE_COORDINATES_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "schema": "state_coordinates.schema.json",
            "dimension_order_score": list(HOFSTEDE_DIMENSION_ORDER),
            "affinity_beta": DEFAULT_AFFINITY_BETA,
        },
        "states": [asdict(s) for s in state_coords.values()],
    }
    STATE_COORDINATES_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

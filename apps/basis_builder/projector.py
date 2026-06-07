"""Project each sovereign state into B_viz and B_score, derive affinity vector.

Coverage cascade (decreasing observational quality):

1. ``observed`` — Inglehart-Welzel direct for ``x_viz``; Hofstede direct for
   ``x_score`` (missing per-dimension cells filled by row mean, marked
   ``observed_with_dim_imputation``).
2. ``imputed_pew`` / ``imputed_governance`` — auxiliary public sources
   calibrated via ridge regression on the observed intersection (see
   ``packages/civvec_core/imputation/``). The local Pew/WGI/FSI files cover
   the same ~63 states as Hofstede, so this tier currently rarely fires —
   the scaffolding is in place for future extended sources (UNDP HDR,
   V-Dem, WVS waves 5-6, UN voting).
3. ``centroid_prior`` — fall back on the centroid (``mu_viz``, ``mu_score``)
   of the curated civilization. Triggered for the ~130 UN members with no
   survey data. For ambiguous cases the first listed competing civilization
   provides the prior.

The cascade guarantees ``x_viz ∈ ℝ²`` and ``x_score ∈ ℝ⁶`` are non-null for
all 193 UN member states. Each output coordinate carries a ``provenance``
tag so distance algebra and the second-moment tensor can stratify analyses.

Affinity vector ``w_s[i]`` is the softmax inverse-distance to the 11
civilization centroids in B_score. For imputed/prior states the affinity is
computed on the imputed ``x_score`` and tagged accordingly — uniform 1/11 is
no longer used as a fallback.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from packages.civvec_core.imputation.centroid_prior import (
    CentroidPriorCoordinates,
    centroid_prior_for_state,
)
from packages.civvec_core.imputation.governance_to_hofstede import (
    GovernanceToHofstedeModel,
    fit_governance_to_hofstede,
)
from packages.civvec_core.imputation.pew_to_iw import (
    PewToIWModel,
    fit_pew_to_iw,
)

from .centroids import CivilizationCentroid, compute_centroids
from .load_fsi import load_fsi
from .load_hofstede import HOFSTEDE_DIMENSION_ORDER, load_hofstede
from .load_iw import load_inglehart_welzel
from .load_pew import load_pew
from .load_un_voting import load_un_voting
from .load_undp_hdr import load_undp_hdr
from .load_vdem import load_vdem
from .load_wgi import load_wgi
from .paths import STATE_COORDINATES_PATH
from .taxonomy_membership import load_iso3_to_membership
from .un_members import un_member_iso3_codes

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
    curated_civilization: str | None = None
    curated_role: str | None = None
    curated_civilizations_competing: list[str] | None = None
    sub_cluster_id: str | None = None
    sub_cluster_label: str | None = None


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


def _select_centroid_for_fallback(
    iso3: str,
    membership_entry,
    centroids: dict[str, CivilizationCentroid],
) -> tuple[str | None, CentroidPriorCoordinates | None]:
    """Pick the civilization centroid to fall back on for a state with no observation."""
    if membership_entry is None:
        return None, None
    civilization_id = membership_entry.curated_civilization
    if civilization_id is None and membership_entry.curated_civilizations_competing:
        civilization_id = membership_entry.curated_civilizations_competing[0]
    if civilization_id is None:
        return None, None
    prior = centroid_prior_for_state(civilization_id, centroids)
    if prior is None:
        return civilization_id, None
    return civilization_id, prior


def project_states(
    centroids: dict[str, CivilizationCentroid] | None = None,
) -> dict[str, StateCoordinates]:
    """Compute B_viz and B_score for every UN member state via the imputation cascade."""
    if centroids is None:
        centroids = compute_centroids()

    iw_coords = load_inglehart_welzel()
    hofstede_profiles = load_hofstede()
    pew_profiles = load_pew()
    wgi_profiles = load_wgi()
    fsi_profiles = load_fsi()
    undp_profiles = load_undp_hdr()
    voting_profiles = load_un_voting()
    vdem_profiles = load_vdem()
    membership_index = load_iso3_to_membership()
    un_iso3s = un_member_iso3_codes()

    pew_to_iw_model: PewToIWModel | None = fit_pew_to_iw(
        pew_profiles, iw_coords, undp_profiles, voting_profiles, vdem_profiles
    )
    governance_to_hofstede_model: GovernanceToHofstedeModel | None = (
        fit_governance_to_hofstede(
            wgi_profiles,
            fsi_profiles,
            undp_profiles,
            voting_profiles,
            vdem_profiles,
            hofstede_profiles,
        )
    )

    state_coords: dict[str, StateCoordinates] = {}

    for iso3 in sorted(un_iso3s):
        membership_entry = membership_index.get(iso3)
        fallback_civilization_id, fallback_prior = _select_centroid_for_fallback(
            iso3, membership_entry, centroids
        )

        x_viz, x_viz_ellipse, x_viz_provenance = _resolve_x_viz(
            iso3,
            iw_coords,
            pew_profiles,
            undp_profiles,
            voting_profiles,
            vdem_profiles,
            pew_to_iw_model,
            fallback_prior,
        )

        x_score, x_score_provenance, x_score_sigma = _resolve_x_score(
            iso3,
            hofstede_profiles,
            wgi_profiles,
            fsi_profiles,
            undp_profiles,
            voting_profiles,
            vdem_profiles,
            governance_to_hofstede_model,
            fallback_prior,
        )

        affinity_vector = softmax_affinity(np.array(x_score, dtype=float), centroids)

        curated_civilization = (
            membership_entry.curated_civilization if membership_entry else None
        )
        curated_role = membership_entry.curated_role if membership_entry else None
        curated_competing = (
            list(membership_entry.curated_civilizations_competing)
            if membership_entry and membership_entry.curated_civilizations_competing
            else None
        )
        sub_cluster_id = (
            membership_entry.sub_cluster_id if membership_entry else None
        )
        sub_cluster_label = (
            membership_entry.sub_cluster_label if membership_entry else None
        )

        low_evidence = (
            x_viz_provenance != "observed" or x_score_provenance != "observed"
        )

        data_quality: dict[str, Any] = {
            "iw_coverage": (
                "present"
                if x_viz_provenance in ("observed", "imputed_wvs_items")
                else "missing"
            ),
            "hofstede_coverage": (
                "present" if x_score_provenance == "observed" else "missing"
            ),
            "low_evidence": low_evidence,
            "x_viz_provenance": x_viz_provenance,
            "x_score_provenance": x_score_provenance,
            "x_score_sigma_prior": x_score_sigma,
            "fallback_civilization_id": fallback_civilization_id,
        }

        state_coords[iso3] = StateCoordinates(
            iso3=iso3,
            label=None,
            x_viz=x_viz,
            x_viz_ellipse=x_viz_ellipse,
            x_score=x_score,
            affinity_vector=affinity_vector,
            data_quality=data_quality,
            source_refs=_source_refs(x_viz_provenance, x_score_provenance),
            curated_civilization=curated_civilization,
            curated_role=curated_role,
            curated_civilizations_competing=curated_competing,
            sub_cluster_id=sub_cluster_id,
            sub_cluster_label=sub_cluster_label,
        )

    if pew_to_iw_model is not None:
        _attach_calibration_meta(state_coords, "pew_to_iw_model", {
            "training_n": len(pew_to_iw_model.training_iso3),
            "rmse_ts": pew_to_iw_model.rmse_ts,
            "rmse_se": pew_to_iw_model.rmse_se,
        })
    if governance_to_hofstede_model is not None:
        _attach_calibration_meta(state_coords, "governance_to_hofstede_model", {
            "training_n": len(governance_to_hofstede_model.training_iso3),
            "rmse_per_dimension": governance_to_hofstede_model.rmse_per_dimension,
        })

    return state_coords


def _resolve_x_viz(
    iso3: str,
    iw_coords,
    pew_profiles,
    undp_profiles,
    voting_profiles,
    vdem_profiles,
    pew_to_iw_model: PewToIWModel | None,
    fallback_prior: CentroidPriorCoordinates | None,
) -> tuple[list[float | None], dict[str, Any] | None, str]:
    iw = iw_coords.get(iso3)
    if iw is not None:
        provenance_label = (
            "observed"
            if iw.source == "wvs_wave7_official"
            else "imputed_wvs_items"
        )
        x_viz: list[float | None] = [float(iw.ts), float(iw.se)]
        x_viz_ellipse = {
            "sigma": [
                [float(iw.ts_ci ** 2), 0.0],
                [0.0, float(iw.se_ci ** 2)],
            ],
            "confidence_level": 0.80,
            "source": iw.source,
        }
        return x_viz, x_viz_ellipse, provenance_label

    pew = pew_profiles.get(iso3)
    undp = undp_profiles.get(iso3)
    voting = voting_profiles.get(iso3)
    vdem = vdem_profiles.get(iso3)
    if pew_to_iw_model is not None and pew_to_iw_model.has_minimal_signal(
        pew, undp, voting, vdem
    ):
        ts_pred, se_pred = pew_to_iw_model.predict(pew, undp, voting, vdem)
        rmse_ts = pew_to_iw_model.rmse_ts
        rmse_se = pew_to_iw_model.rmse_se
        x_viz = [float(ts_pred), float(se_pred)]
        x_viz_ellipse = {
            "sigma": [
                [rmse_ts ** 2, 0.0],
                [0.0, rmse_se ** 2],
            ],
            "confidence_level": 0.80,
            "source": "imputed_pew",
        }
        return x_viz, x_viz_ellipse, "imputed_pew"

    if fallback_prior is not None:
        return list(fallback_prior.x_viz), fallback_prior.x_viz_ellipse, "centroid_prior"

    # Unmappable: keep nulls so downstream consumers can detect the failure.
    return [None, None], None, "unresolved"


def _resolve_x_score(
    iso3: str,
    hofstede_profiles,
    wgi_profiles,
    fsi_profiles,
    undp_profiles,
    voting_profiles,
    vdem_profiles,
    governance_to_hofstede_model: GovernanceToHofstedeModel | None,
    fallback_prior: CentroidPriorCoordinates | None,
) -> tuple[list[float | None], str, list[float] | None]:
    hof = hofstede_profiles.get(iso3)
    if hof is not None and hof.coverage != "missing":
        score_values_raw = hof.values
        if np.any(np.isnan(score_values_raw)):
            mean_fill = float(np.nanmean(score_values_raw))
            score_values_filled = np.where(
                np.isnan(score_values_raw), mean_fill, score_values_raw
            )
            return [float(v) for v in score_values_filled], "observed_with_dim_imputation", None
        return [float(v) for v in score_values_raw], "observed", None

    wgi = wgi_profiles.get(iso3)
    fsi = fsi_profiles.get(iso3)
    undp = undp_profiles.get(iso3)
    voting = voting_profiles.get(iso3)
    vdem = vdem_profiles.get(iso3)
    if (
        governance_to_hofstede_model is not None
        and len(governance_to_hofstede_model.weights_per_dimension)
        == len(HOFSTEDE_DIMENSION_ORDER)
        and governance_to_hofstede_model.has_minimal_signal(wgi, fsi, undp, voting, vdem)
    ):
        prediction = governance_to_hofstede_model.predict(wgi, fsi, undp, voting, vdem)
        rmse_vector = [
            governance_to_hofstede_model.rmse_per_dimension[dimension]
            for dimension in HOFSTEDE_DIMENSION_ORDER
        ]
        return [float(v) for v in prediction], "imputed_governance", rmse_vector

    if fallback_prior is not None:
        return (
            list(fallback_prior.x_score),
            "centroid_prior",
            list(fallback_prior.sigma_score),
        )

    return [None] * 6, "unresolved", None


def _source_refs(x_viz_provenance: str, x_score_provenance: str) -> list[str]:
    refs: list[str] = []
    if x_viz_provenance == "observed":
        refs.append("wvs_wave7_2022")
    elif x_viz_provenance == "imputed_pew":
        refs.append("pew_religious_composition_2020")
    elif x_viz_provenance == "centroid_prior":
        refs.append("huntington_1996")
    if x_score_provenance in ("observed", "observed_with_dim_imputation"):
        refs.append("hofstede_2010")
    elif x_score_provenance == "imputed_governance":
        refs.extend(["wgi_2022", "fsi_2024"])
    elif x_score_provenance == "centroid_prior" and "huntington_1996" not in refs:
        refs.append("huntington_1996")
    return refs


def _attach_calibration_meta(
    state_coords: dict[str, StateCoordinates], key: str, payload: dict[str, Any]
) -> None:
    """Attach a model-quality summary onto every state's data_quality block."""
    for state in state_coords.values():
        state.data_quality[key] = payload


def write_state_coordinates(state_coords: dict[str, StateCoordinates]) -> None:
    STATE_COORDINATES_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "schema": "state_coordinates.schema.json",
            "dimension_order_score": list(HOFSTEDE_DIMENSION_ORDER),
            "affinity_beta": DEFAULT_AFFINITY_BETA,
            "cascade": [
                "observed",
                "imputed_pew",
                "imputed_governance",
                "centroid_prior",
            ],
        },
        "states": [asdict(s) for s in state_coords.values()],
    }
    STATE_COORDINATES_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

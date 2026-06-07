"""Calibrate auxiliary public indicators (Pew religion + UNDP HDR) → Inglehart-Welzel (ts, se).

Two ridge regressions target the two IW axes independently:
``ts`` (Traditional → Secular-Rational) and ``se`` (Survival → Self-Expression).

Feature vector (combined Pew + UNDP HDR, missing components mean-filled):

- one-hot encoding of Pew ``dominant_group`` (Christian/Muslim/Hindu/Buddhist/
  Jewish/Folk/Unaffiliated/Other) — 8 binary features
- Pew ``dominant_share_pct / 100``
- UNDP ``hdi`` (correlates with both axes)
- UNDP ``gii`` (gender inequality — inversely correlates with SE)
- UNDP ``mean_years_schooling / 15`` (correlates with TS — secular-rational)
- UNDP ``log(gnipc)`` (normalised by training; correlates with both)
- intercept

Coverage gain: with UNDP added, the calibration can predict IW for ~190
states (UNDP covers nearly all UN members), versus ~63 with Pew alone.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from apps.basis_builder.load_iw import IWCoordinate
from apps.basis_builder.load_pew import PewProfile
from apps.basis_builder.load_un_voting import UNVotingProfile
from apps.basis_builder.load_undp_hdr import UNDPProfile
from apps.basis_builder.load_vdem import VDemProfile


FEATURE_NAMES: tuple[str, ...] = (
    "pew_christians",
    "pew_muslims",
    "pew_hindus",
    "pew_buddhists",
    "pew_jews",
    "pew_unaffiliated",
    "pew_other_religions",
    "undp_hdi",
    "undp_gii",
    "undp_mys_norm",
    "undp_eys_norm",
    "undp_log_gnipc",
    "un_voting_idealpoint",
    "vdem_libdem",
    "vdem_civil_liberties",
    "vdem_religious_freedom",
    "vdem_gender_empowerment",
    "intercept",
)


def _raw_feature_components(
    pew: PewProfile | None,
    undp: UNDPProfile | None,
    voting: UNVotingProfile | None,
    vdem: VDemProfile | None,
) -> dict[str, float | None]:
    components: dict[str, float | None] = {
        "pew_christians": pew.christians if pew is not None else None,
        "pew_muslims": pew.muslims if pew is not None else None,
        "pew_hindus": pew.hindus if pew is not None else None,
        "pew_buddhists": pew.buddhists if pew is not None else None,
        "pew_jews": pew.jews if pew is not None else None,
        "pew_unaffiliated": pew.unaffiliated if pew is not None else None,
        "pew_other_religions": pew.other_religions if pew is not None else None,
        "undp_hdi": undp.hdi if undp is not None else None,
        "undp_gii": undp.gii if undp is not None else None,
        "undp_mys_norm": (
            undp.mean_years_schooling / 15.0
            if undp is not None and undp.mean_years_schooling is not None
            else None
        ),
        "undp_eys_norm": (
            undp.expected_years_schooling / 20.0
            if undp is not None and undp.expected_years_schooling is not None
            else None
        ),
        "undp_log_gnipc": (
            float(np.log(undp.gnipc)) if undp is not None and undp.gnipc else None
        ),
        "un_voting_idealpoint": voting.idealpoint if voting is not None else None,
        "vdem_libdem": vdem.libdem if vdem is not None else None,
        "vdem_civil_liberties": vdem.civil_liberties if vdem is not None else None,
        "vdem_religious_freedom": vdem.religious_freedom if vdem is not None else None,
        "vdem_gender_empowerment": vdem.gender_empowerment if vdem is not None else None,
        "intercept": 1.0,
    }
    return components


def _ridge_fit(features: np.ndarray, targets: np.ndarray, alpha: float) -> np.ndarray:
    """Closed-form ridge via lstsq augmentation."""
    n_features = features.shape[1]
    sqrt_alpha = np.sqrt(alpha)
    penalty_block = sqrt_alpha * np.eye(n_features)
    penalty_block[-1, -1] = 0.0
    augmented_features = np.vstack([features, penalty_block])
    augmented_targets = np.concatenate([targets, np.zeros(n_features)])
    solution, *_ = np.linalg.lstsq(augmented_features, augmented_targets, rcond=None)
    return solution


@dataclass
class PewToIWModel:
    weights_ts: np.ndarray
    weights_se: np.ndarray
    training_iso3: tuple[str, ...]
    rmse_ts: float
    rmse_se: float
    feature_means: dict[str, float]
    feature_order: tuple[str, ...] = FEATURE_NAMES

    def _filled_feature_vector(
        self,
        pew: PewProfile | None,
        undp: UNDPProfile | None,
        voting: UNVotingProfile | None,
        vdem: VDemProfile | None,
    ) -> np.ndarray:
        raw_components = _raw_feature_components(pew, undp, voting, vdem)
        return np.array(
            [
                raw_components[name]
                if raw_components[name] is not None
                else self.feature_means[name]
                for name in self.feature_order
            ],
            dtype=float,
        )

    def predict(
        self,
        pew: PewProfile | None,
        undp: UNDPProfile | None,
        voting: UNVotingProfile | None,
        vdem: VDemProfile | None,
    ) -> tuple[float, float]:
        feature_vector = self._filled_feature_vector(pew, undp, voting, vdem)
        return (
            float(feature_vector @ self.weights_ts),
            float(feature_vector @ self.weights_se),
        )

    def has_minimal_signal(
        self,
        pew: PewProfile | None,
        undp: UNDPProfile | None,
        voting: UNVotingProfile | None,
        vdem: VDemProfile | None,
    ) -> bool:
        raw_components = _raw_feature_components(pew, undp, voting, vdem)
        return any(
            value is not None
            for name, value in raw_components.items()
            if name != "intercept"
        )


def fit_pew_to_iw(
    pew_profiles: dict[str, PewProfile],
    iw_coords: dict[str, IWCoordinate],
    undp_profiles: dict[str, UNDPProfile] | None = None,
    voting_profiles: dict[str, UNVotingProfile] | None = None,
    vdem_profiles: dict[str, VDemProfile] | None = None,
    ridge_alpha: float = 1.0,
) -> PewToIWModel | None:
    """Fit on IW ∩ (Pew ∪ UNDP ∪ UN voting ∪ V-Dem). Missing per-feature values mean-filled."""
    undp_profiles = undp_profiles or {}
    voting_profiles = voting_profiles or {}
    vdem_profiles = vdem_profiles or {}
    training_iso3 = sorted(
        iso3
        for iso3 in iw_coords
        if iso3 in pew_profiles
        or iso3 in undp_profiles
        or iso3 in voting_profiles
        or iso3 in vdem_profiles
    )
    if len(training_iso3) < 10:
        return None

    raw_components_per_state = [
        _raw_feature_components(
            pew_profiles.get(iso3),
            undp_profiles.get(iso3),
            voting_profiles.get(iso3),
            vdem_profiles.get(iso3),
        )
        for iso3 in training_iso3
    ]

    feature_means: dict[str, float] = {}
    for component_name in FEATURE_NAMES:
        observed_values = [
            components[component_name]
            for components in raw_components_per_state
            if components[component_name] is not None
        ]
        feature_means[component_name] = (
            float(np.mean(observed_values)) if observed_values else 0.0
        )

    feature_matrix = np.array(
        [
            [
                components[name]
                if components[name] is not None
                else feature_means[name]
                for name in FEATURE_NAMES
            ]
            for components in raw_components_per_state
        ],
        dtype=float,
    )
    targets_ts = np.array([iw_coords[iso3].ts for iso3 in training_iso3])
    targets_se = np.array([iw_coords[iso3].se for iso3 in training_iso3])

    weights_ts = _ridge_fit(feature_matrix, targets_ts, ridge_alpha)
    weights_se = _ridge_fit(feature_matrix, targets_se, ridge_alpha)

    loo_residuals_ts: list[float] = []
    loo_residuals_se: list[float] = []
    for hold_out_index in range(len(training_iso3)):
        mask = np.ones(len(training_iso3), dtype=bool)
        mask[hold_out_index] = False
        weights_ts_loo = _ridge_fit(feature_matrix[mask], targets_ts[mask], ridge_alpha)
        weights_se_loo = _ridge_fit(feature_matrix[mask], targets_se[mask], ridge_alpha)
        loo_residuals_ts.append(
            targets_ts[hold_out_index]
            - float(feature_matrix[hold_out_index] @ weights_ts_loo)
        )
        loo_residuals_se.append(
            targets_se[hold_out_index]
            - float(feature_matrix[hold_out_index] @ weights_se_loo)
        )
    rmse_ts = float(np.sqrt(np.mean(np.square(loo_residuals_ts))))
    rmse_se = float(np.sqrt(np.mean(np.square(loo_residuals_se))))

    return PewToIWModel(
        weights_ts=weights_ts,
        weights_se=weights_se,
        training_iso3=tuple(training_iso3),
        rmse_ts=rmse_ts,
        rmse_se=rmse_se,
        feature_means=feature_means,
    )

"""Calibrate auxiliary public indicators (WGI + FSI + UNDP HDR) → Hofstede 6D.

Six independent ridge regressions (α = 1.0), one per Hofstede dimension
(``pdi``, ``idv``, ``mas``, ``uai``, ``lto``, ``ivr``). The feature vector
combines the auxiliary sources that exist for a given state — missing
sources are handled by per-feature masking (set the feature to its training
mean), which preserves the training intersection size without dropping
states at prediction time.

Active features:

- ``rule_of_law`` z-score (WGI)
- ``fsi_total / 120`` normalised in [0, 1]
- ``hdi`` (UNDP Human Development Index, 0-1)
- ``gii`` (UNDP Gender Inequality Index, 0-1, lower = more equal)
- ``log(gnipc)`` (log GNI per capita, normalised by training std)
- ``mean_years_schooling / 15`` (UNDP, normalised)
- ``expected_years_schooling / 20`` (UNDP, normalised)
- intercept (last column, unregularised)

Adding UNDP indicators pulls training set size from ~63 (Hofstede ∩ WGI ∩ FSI)
to ~63 (still bounded by Hofstede), but unlocks **imputation for ~190 states**
because UNDP covers nearly all UN members. The training set still only
spans the observed Hofstede ∩ auxiliary intersection, but prediction is now
possible for any state with the auxiliary features present.

The leave-one-out RMSE per dimension is reported so consumers can decide
whether to trust the imputation or fall back on the centroid prior. Some
Hofstede dimensions (notably ``mas``) remain hard to recover from public
proxies — the prior centroïde tier remains the fallback when this RMSE is
too large relative to the dimension's range.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from apps.basis_builder.load_fsi import FSIProfile
from apps.basis_builder.load_hofstede import HOFSTEDE_DIMENSION_ORDER, HofstedeProfile
from apps.basis_builder.load_un_voting import UNVotingProfile
from apps.basis_builder.load_undp_hdr import UNDPProfile
from apps.basis_builder.load_vdem import VDemProfile
from apps.basis_builder.load_wgi import WGIProfile


FEATURE_COMPONENT_ORDER: tuple[str, ...] = (
    "rule_of_law",
    "fsi_total_norm",
    "hdi",
    "gii",
    "log_gnipc_norm",
    "mys_norm",
    "eys_norm",
    "un_voting_idealpoint",
    "vdem_libdem",
    "vdem_gender_empowerment",
    "vdem_corruption",
    "vdem_civil_liberties",
    "vdem_religious_freedom",
    "vdem_rule_of_law",
    "intercept",
)


def _raw_feature_components(
    wgi: WGIProfile | None,
    fsi: FSIProfile | None,
    undp: UNDPProfile | None,
    voting: UNVotingProfile | None,
    vdem: VDemProfile | None,
) -> dict[str, float | None]:
    components: dict[str, float | None] = {
        "rule_of_law": wgi.rule_of_law if wgi is not None else None,
        "fsi_total_norm": (fsi.total_score / 120.0) if fsi is not None else None,
        "hdi": undp.hdi if undp is not None else None,
        "gii": undp.gii if undp is not None else None,
        "log_gnipc_norm": (
            float(np.log(undp.gnipc)) if undp is not None and undp.gnipc else None
        ),
        "mys_norm": (
            undp.mean_years_schooling / 15.0
            if undp is not None and undp.mean_years_schooling is not None
            else None
        ),
        "eys_norm": (
            undp.expected_years_schooling / 20.0
            if undp is not None and undp.expected_years_schooling is not None
            else None
        ),
        "un_voting_idealpoint": voting.idealpoint if voting is not None else None,
        "vdem_libdem": vdem.libdem if vdem is not None else None,
        "vdem_gender_empowerment": (
            vdem.gender_empowerment if vdem is not None else None
        ),
        "vdem_corruption": vdem.corruption if vdem is not None else None,
        "vdem_civil_liberties": vdem.civil_liberties if vdem is not None else None,
        "vdem_religious_freedom": (
            vdem.religious_freedom if vdem is not None else None
        ),
        "vdem_rule_of_law": vdem.rule_of_law if vdem is not None else None,
        "intercept": 1.0,
    }
    return components


def _ridge_fit(features: np.ndarray, targets: np.ndarray, alpha: float) -> np.ndarray:
    """Closed-form ridge via lstsq augmentation, intercept column unregularised."""
    n_features = features.shape[1]
    sqrt_alpha = np.sqrt(alpha)
    penalty_block = sqrt_alpha * np.eye(n_features)
    penalty_block[-1, -1] = 0.0  # do not regularise the intercept (last column)
    augmented_features = np.vstack([features, penalty_block])
    augmented_targets = np.concatenate([targets, np.zeros(n_features)])
    solution, *_ = np.linalg.lstsq(augmented_features, augmented_targets, rcond=None)
    return solution


@dataclass
class GovernanceToHofstedeModel:
    weights_per_dimension: dict[str, np.ndarray]
    training_iso3: tuple[str, ...]
    rmse_per_dimension: dict[str, float]
    feature_means: dict[str, float]  # used to fill missing features at predict time
    feature_order: tuple[str, ...] = FEATURE_COMPONENT_ORDER

    def predict(
        self,
        wgi: WGIProfile | None,
        fsi: FSIProfile | None,
        undp: UNDPProfile | None,
        voting: UNVotingProfile | None,
        vdem: VDemProfile | None,
    ) -> np.ndarray:
        raw_components = _raw_feature_components(wgi, fsi, undp, voting, vdem)
        filled_feature_vector = np.array(
            [
                raw_components[name]
                if raw_components[name] is not None
                else self.feature_means[name]
                for name in self.feature_order
            ],
            dtype=float,
        )
        return np.array(
            [
                float(filled_feature_vector @ self.weights_per_dimension[dimension])
                for dimension in HOFSTEDE_DIMENSION_ORDER
            ],
            dtype=float,
        )

    def has_minimal_signal(
        self,
        wgi: WGIProfile | None,
        fsi: FSIProfile | None,
        undp: UNDPProfile | None,
        voting: UNVotingProfile | None,
        vdem: VDemProfile | None,
    ) -> bool:
        """At least one informative (non-intercept) feature must be present."""
        raw_components = _raw_feature_components(wgi, fsi, undp, voting, vdem)
        return any(
            value is not None
            for name, value in raw_components.items()
            if name != "intercept"
        )


def fit_governance_to_hofstede(
    wgi_profiles: dict[str, WGIProfile],
    fsi_profiles: dict[str, FSIProfile],
    undp_profiles: dict[str, UNDPProfile],
    voting_profiles: dict[str, UNVotingProfile],
    vdem_profiles: dict[str, VDemProfile],
    hofstede_profiles: dict[str, HofstedeProfile],
    ridge_alpha: float = 1.0,
) -> GovernanceToHofstedeModel | None:
    """Fit six ridges on the training intersection (states with Hofstede + ≥1 auxiliary).

    Missing auxiliary features in the training set are filled by their column mean,
    so we keep all states with at least one auxiliary signal.
    """
    training_iso3 = sorted(
        iso3
        for iso3 in hofstede_profiles
        if hofstede_profiles[iso3].coverage != "missing"
        and (
            iso3 in wgi_profiles
            or iso3 in fsi_profiles
            or iso3 in undp_profiles
            or iso3 in voting_profiles
            or iso3 in vdem_profiles
        )
    )
    if len(training_iso3) < 10:
        return None

    raw_components_per_state = [
        _raw_feature_components(
            wgi_profiles.get(iso3),
            fsi_profiles.get(iso3),
            undp_profiles.get(iso3),
            voting_profiles.get(iso3),
            vdem_profiles.get(iso3),
        )
        for iso3 in training_iso3
    ]

    feature_means: dict[str, float] = {}
    for component_name in FEATURE_COMPONENT_ORDER:
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
                components[name] if components[name] is not None else feature_means[name]
                for name in FEATURE_COMPONENT_ORDER
            ]
            for components in raw_components_per_state
        ],
        dtype=float,
    )

    hofstede_target_matrix = np.array(
        [hofstede_profiles[iso3].values for iso3 in training_iso3]
    )

    weights_per_dimension: dict[str, np.ndarray] = {}
    rmse_per_dimension: dict[str, float] = {}

    for dimension_index, dimension_name in enumerate(HOFSTEDE_DIMENSION_ORDER):
        targets = hofstede_target_matrix[:, dimension_index]
        valid_mask = ~np.isnan(targets)
        if valid_mask.sum() < 10:
            continue
        valid_features = feature_matrix[valid_mask]
        valid_targets = targets[valid_mask]
        weights_per_dimension[dimension_name] = _ridge_fit(
            valid_features, valid_targets, ridge_alpha
        )

        loo_residuals: list[float] = []
        for hold_out_index in range(len(valid_targets)):
            mask = np.ones(len(valid_targets), dtype=bool)
            mask[hold_out_index] = False
            weights_loo = _ridge_fit(
                valid_features[mask], valid_targets[mask], ridge_alpha
            )
            loo_residuals.append(
                valid_targets[hold_out_index]
                - float(valid_features[hold_out_index] @ weights_loo)
            )
        rmse_per_dimension[dimension_name] = float(
            np.sqrt(np.mean(np.square(loo_residuals)))
        )

    return GovernanceToHofstedeModel(
        weights_per_dimension=weights_per_dimension,
        training_iso3=tuple(training_iso3),
        rmse_per_dimension=rmse_per_dimension,
        feature_means=feature_means,
    )

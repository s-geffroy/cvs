"""Imputation cascade for state coordinates in B_viz (R^2) and B_score (R^6).

Three tiers, in decreasing observational quality:

1. ``observed`` — Hofstede/Inglehart-Welzel direct, no transformation.
2. ``imputed_*`` — auxiliary public sources (Pew religious composition, WGI
   rule of law, FSI fragility, UNDP HDR composite indices, UN GA voting
   affinity, V-Dem, WVS earlier waves) calibrated via ridge regression on
   the intersection with observed states.
3. ``centroid_prior`` — when no observation is available, the state inherits
   the centroid of its curated civilization (``mu_viz``, ``mu_score``) with
   the centroid covariance reported as the ellipse.

Each output coordinate carries a ``provenance`` tag so downstream consumers
(distance algebra, second-moment tensors, UI map) can stratify analyses by
data quality. See ``docs/16_imputation_cascade.md`` for the full methodology.
"""
from .centroid_prior import centroid_prior_for_state
from .governance_to_hofstede import (
    GovernanceToHofstedeModel,
    fit_governance_to_hofstede,
)
from .pew_to_iw import PewToIWModel, fit_pew_to_iw

__all__ = [
    "centroid_prior_for_state",
    "PewToIWModel",
    "fit_pew_to_iw",
    "GovernanceToHofstedeModel",
    "fit_governance_to_hofstede",
]

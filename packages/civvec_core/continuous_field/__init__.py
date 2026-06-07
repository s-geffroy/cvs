"""Continuous civilizational field on the sphere — replaces the per-state vector.

This package treats each sovereign state's coordinates ``(x_viz, x_score,
affinity_vector)`` not as the *output* but as **observation samples** of an
underlying continuous field ``x: S² → ℝ²⊕ℝ⁶⊕Δ¹⁰``. Each state contributes
one or several sample points located at its **population-weighted centroid(s)**,
and a Gaussian Process on great-circle distance interpolates between them
with a Matérn 3/2 kernel.

The output is a continuous, queryable field. Its **analytical Jacobian**
``∂x/∂λ, ∂x/∂φ`` gives the spatial gradient — the natural mathematical
notion of "rate of cultural change along a direction" — without any
artificial step at state borders.

See ``docs/17_continuous_field.md`` for the methodology, kernel choice,
and the philosophical rationale (the state is a discrete administrative
unit, not the natural support of human values).
"""
from .kernels import matern_3_2_sphere, matern_3_2_sphere_gradient
from .gp import SphericalGaussianProcess
from .sample_points import generate_sample_points_per_state
from .deformation_tensor import (
    DeformationTensorInvariants,
    cauchy_green_per_cell,
    deformation_tensor_invariants,
    stack_jacobian_per_component,
)
from .curvilinear_distance import curvilinear_cultural_distance

__all__ = [
    "matern_3_2_sphere",
    "matern_3_2_sphere_gradient",
    "SphericalGaussianProcess",
    "generate_sample_points_per_state",
    "DeformationTensorInvariants",
    "cauchy_green_per_cell",
    "deformation_tensor_invariants",
    "stack_jacobian_per_component",
    "curvilinear_cultural_distance",
]

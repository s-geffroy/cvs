"""Right Cauchy-Green deformation tensor of the continuous field.

For the multi-output Gaussian Process producing
``x(λ, φ) ∈ ℝ^{19}``, the spatial Jacobian is

    J(λ, φ) = [ ∂x/∂λ | ∂x/∂φ ]  ∈ ℝ^{19 × 2}

The right Cauchy-Green tensor (the natural metric pulled back from output
space to input space)

    G(λ, φ) = J(λ, φ)ᵀ · J(λ, φ)  ∈ ℝ^{2 × 2}

is the continuous-field analogue of the discrete state second moment
``M(s)`` defined in :mod:`apps.basis_builder.moments`. Its invariants
- trace (sum of squared component gradients along both axes)
- determinant (signed area-element distortion)
- anisotropy ``(λ₁ − λ₂)/λ₁`` (how directional the deformation is)
provide a richer fault-line summary than the scalar ``‖∇x‖`` magnitude.

This module operates on the dense gradient arrays produced by ``train_v2.py``
— it does not refit any GP. It only differentiates the already-stored
``∂x/∂λ`` and ``∂x/∂φ`` for each component.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class DeformationTensorInvariants:
    trace: np.ndarray  # tr(G) per cell
    determinant: np.ndarray
    eigenvalue_major: np.ndarray
    eigenvalue_minor: np.ndarray
    anisotropy: np.ndarray  # in [0, 1] when both eigenvalues are non-negative


def stack_jacobian_per_component(
    gradient_longitude_per_component: dict[str, np.ndarray],
    gradient_latitude_per_component: dict[str, np.ndarray],
) -> np.ndarray:
    """Stack per-component gradient grids into a J(p) tensor of shape (n_lat, n_lon, 19, 2)."""
    component_names_ordered = list(gradient_longitude_per_component.keys())
    grid_shape = gradient_longitude_per_component[component_names_ordered[0]].shape
    jacobian_per_cell = np.empty(
        grid_shape + (len(component_names_ordered), 2), dtype=np.float64
    )
    for component_index, component_name in enumerate(component_names_ordered):
        jacobian_per_cell[..., component_index, 0] = (
            gradient_longitude_per_component[component_name]
        )
        jacobian_per_cell[..., component_index, 1] = (
            gradient_latitude_per_component[component_name]
        )
    return jacobian_per_cell


def cauchy_green_per_cell(jacobian_per_cell: np.ndarray) -> np.ndarray:
    """Compute G(p) = J(p)ᵀ J(p) per grid cell; output shape (n_lat, n_lon, 2, 2)."""
    return np.einsum("...di,...dj->...ij", jacobian_per_cell, jacobian_per_cell)


def deformation_tensor_invariants(
    cauchy_green_field: np.ndarray,
) -> DeformationTensorInvariants:
    """Trace, determinant, eigenvalues, anisotropy per grid cell."""
    trace_field = (
        cauchy_green_field[..., 0, 0] + cauchy_green_field[..., 1, 1]
    )
    determinant_field = (
        cauchy_green_field[..., 0, 0] * cauchy_green_field[..., 1, 1]
        - cauchy_green_field[..., 0, 1] * cauchy_green_field[..., 1, 0]
    )

    # Closed-form eigenvalues of a 2×2 symmetric matrix
    # λ_± = (tr ± √(tr² − 4 det)) / 2
    discriminant = trace_field ** 2 - 4.0 * determinant_field
    discriminant_clipped = np.maximum(discriminant, 0.0)
    sqrt_discriminant = np.sqrt(discriminant_clipped)
    eigenvalue_major = 0.5 * (trace_field + sqrt_discriminant)
    eigenvalue_minor = 0.5 * (trace_field - sqrt_discriminant)

    safe_major = np.where(eigenvalue_major > 1e-12, eigenvalue_major, np.nan)
    anisotropy = (eigenvalue_major - eigenvalue_minor) / safe_major

    return DeformationTensorInvariants(
        trace=trace_field,
        determinant=determinant_field,
        eigenvalue_major=eigenvalue_major,
        eigenvalue_minor=eigenvalue_minor,
        anisotropy=anisotropy,
    )

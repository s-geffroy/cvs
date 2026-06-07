"""Matérn 3/2 covariance kernel on the unit sphere, with analytical gradients.

The unit-sphere version is parametrised by:
- great-circle distance ``d(p, q) = arccos(sin φ_p sin φ_q + cos φ_p cos φ_q cos(λ_p - λ_q))``
  with all coordinates in radians, output in radians of arc (range [0, π]).
- correlation length ``ℓ`` (in radians) controlling the smoothness.
- signal variance ``σ²``.

Matérn 3/2 form:
    k(p, q) = σ² (1 + √3 · d/ℓ) · exp(-√3 · d/ℓ)

The gradient ``∂k/∂(λ_q, φ_q)`` is required for the GP's predictive Jacobian
``∂μ_GP/∂(λ, φ)``. Closed form:

    ∂k/∂q = -σ² (3/ℓ²) d · exp(-√3 · d/ℓ) · ∂d/∂q

with the great-circle gradient (derived from ``d = arccos(A)`` where
``A = sin φ_p sin φ_q + cos φ_p cos φ_q cos(λ_q - λ_p)``):

    ∂d/∂λ_q = (cos φ_p cos φ_q · sin(λ_q - λ_p)) / sin(d)
    ∂d/∂φ_q = (cos φ_p sin φ_q · cos(λ_q - λ_p) − sin φ_p cos φ_q) / sin(d)

At ``d = 0`` the gradient is zero (the kernel has a smooth maximum at its
own input). We guard against the ``1/sin(d)`` singularity by clipping
``sin(d) >= 1e-12``.

The kernel is tested in ``tests/test_continuous_field.py`` against
finite-difference approximations on a 100-point grid.
"""
from __future__ import annotations

import numpy as np


SQRT_3 = float(np.sqrt(3.0))


def great_circle_distance(
    longitude_p: np.ndarray,
    latitude_p: np.ndarray,
    longitude_q: np.ndarray,
    latitude_q: np.ndarray,
) -> np.ndarray:
    """Great-circle distance on the unit sphere, broadcasting-aware.

    All inputs in radians. Output in radians of arc (range [0, π]).
    """
    cos_arc = (
        np.sin(latitude_p) * np.sin(latitude_q)
        + np.cos(latitude_p) * np.cos(latitude_q) * np.cos(longitude_q - longitude_p)
    )
    # Guard against floating-point overflow outside [-1, 1] caused by tiny
    # rounding errors when p == q (which gives cos_arc = 1.0 exactly in real
    # arithmetic but 1.0 + epsilon in floats).
    cos_arc_clipped = np.clip(cos_arc, -1.0, 1.0)
    return np.arccos(cos_arc_clipped)


def matern_3_2_sphere(
    longitude_p: np.ndarray,
    latitude_p: np.ndarray,
    longitude_q: np.ndarray,
    latitude_q: np.ndarray,
    length_scale: float,
    signal_variance: float = 1.0,
) -> np.ndarray:
    """Matérn 3/2 kernel evaluated on the unit sphere.

    Parameters
    ----------
    longitude_p, latitude_p, longitude_q, latitude_q : arrays in radians.
    length_scale : correlation length on the sphere (in radians).
    signal_variance : ``σ²`` prefactor (default 1.0).
    """
    distance = great_circle_distance(
        longitude_p, latitude_p, longitude_q, latitude_q
    )
    scaled_distance = SQRT_3 * distance / length_scale
    return signal_variance * (1.0 + scaled_distance) * np.exp(-scaled_distance)


def matern_3_2_sphere_gradient(
    longitude_p: np.ndarray,
    latitude_p: np.ndarray,
    longitude_q: np.ndarray,
    latitude_q: np.ndarray,
    length_scale: float,
    signal_variance: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Closed-form gradient ``(∂k/∂λ_q, ∂k/∂φ_q)`` of the Matérn 3/2 kernel.

    Returns a tuple ``(grad_longitude, grad_latitude)`` with the same broadcast
    shape as ``great_circle_distance``. At ``d → 0`` the gradient vanishes
    smoothly; we evaluate the analytical limit via the small-d expansion
    rather than dividing by ``sin(d)`` to avoid 0/0 singularities.
    """
    distance = great_circle_distance(
        longitude_p, latitude_p, longitude_q, latitude_q
    )
    scaled_distance = SQRT_3 * distance / length_scale

    # Radial part of the gradient: dk/dd = -σ² (3/ℓ²) d · exp(-√3 d/ℓ)
    radial_derivative = (
        -signal_variance
        * (3.0 / length_scale ** 2)
        * distance
        * np.exp(-scaled_distance)
    )

    sin_distance = np.sin(distance)
    safe_sin_distance = np.where(sin_distance > 1e-12, sin_distance, 1.0)

    # Great-circle gradient ∂d/∂(λ_q, φ_q) — uses safe denominator to avoid
    # 0/0; corrected to 0 at d ≈ 0 below.
    grad_longitude_distance = (
        np.cos(latitude_p)
        * np.cos(latitude_q)
        * np.sin(longitude_q - longitude_p)
    ) / safe_sin_distance
    grad_latitude_distance = (
        np.cos(latitude_p)
        * np.sin(latitude_q)
        * np.cos(longitude_q - longitude_p)
        - np.sin(latitude_p) * np.cos(latitude_q)
    ) / safe_sin_distance

    # When d is essentially zero, both the radial part and ∂d/∂q are well
    # defined (radial → 0 because distance is in the numerator). Force ∂d/∂q
    # to 0 in that regime to avoid propagating spurious finite values.
    near_zero_distance_mask = distance < 1e-9
    grad_longitude_distance = np.where(
        near_zero_distance_mask, 0.0, grad_longitude_distance
    )
    grad_latitude_distance = np.where(
        near_zero_distance_mask, 0.0, grad_latitude_distance
    )

    grad_longitude = radial_derivative * grad_longitude_distance
    grad_latitude = radial_derivative * grad_latitude_distance
    return grad_longitude, grad_latitude

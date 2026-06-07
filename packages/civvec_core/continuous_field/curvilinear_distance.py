"""Curvilinear cultural distance derived from the continuous field's gradient.

Given two query points ``p, q`` on the sphere, the natural civilizational
distance is the integral of the gradient magnitude along the geodesic
connecting them:

    d_cult(p, q) = ∫_{γ(p,q)} ‖∇x(γ(t))‖ dt

where ``γ(p, q)`` is the great-circle arc and ``‖∇x‖`` is the Frobenius
norm of the Jacobian ``J(p) ∈ ℝ^{19×2}`` (sum of squared component
gradients in the spherical metric ``ds² = R² (cos²φ dλ² + dφ²)``).

Two states **culturally distant despite geographic proximity** (e.g.
Czechia ↔ Romania crossing the Catholic/Orthodox fault line) get a
larger distance than two states **culturally close despite geographic
distance** (e.g. Argentina ↔ Spain across the Atlantic). This is what
makes the continuous field operationally useful for the algebra layer.

The integration uses trapezoidal sampling over ``n_segments`` great-circle
points, computed via spherical interpolation (``slerp`` in radians).
The Jacobian at each sample point is obtained from the fitted GP through
its closed-form analytical jacobian — the integral is therefore exact in
the discretisation limit, no Monte Carlo needed.
"""
from __future__ import annotations

import numpy as np

from .gp import SphericalGaussianProcess


def _spherical_slerp(
    longitude_start_rad: float,
    latitude_start_rad: float,
    longitude_end_rad: float,
    latitude_end_rad: float,
    interpolation_parameter: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Slerp along the great circle between two points on the unit sphere.

    ``interpolation_parameter`` is an array in [0, 1] giving the fraction of
    the arc traversed; returns longitudes and latitudes in radians of the
    intermediate points.
    """
    cos_arc = (
        np.sin(latitude_start_rad) * np.sin(latitude_end_rad)
        + np.cos(latitude_start_rad)
        * np.cos(latitude_end_rad)
        * np.cos(longitude_end_rad - longitude_start_rad)
    )
    cos_arc_clipped = np.clip(cos_arc, -1.0, 1.0)
    arc_length = np.arccos(cos_arc_clipped)

    if arc_length < 1e-9:
        # Antipodal-degenerate or coincident: just return the start point
        return (
            np.full_like(interpolation_parameter, longitude_start_rad),
            np.full_like(interpolation_parameter, latitude_start_rad),
        )

    sin_arc = np.sin(arc_length)

    # Convert each endpoint to a 3-vector, then interpolate
    start_vector = np.array(
        [
            np.cos(latitude_start_rad) * np.cos(longitude_start_rad),
            np.cos(latitude_start_rad) * np.sin(longitude_start_rad),
            np.sin(latitude_start_rad),
        ]
    )
    end_vector = np.array(
        [
            np.cos(latitude_end_rad) * np.cos(longitude_end_rad),
            np.cos(latitude_end_rad) * np.sin(longitude_end_rad),
            np.sin(latitude_end_rad),
        ]
    )

    sin_arc_complement = np.sin((1.0 - interpolation_parameter) * arc_length) / sin_arc
    sin_arc_progress = np.sin(interpolation_parameter * arc_length) / sin_arc

    interpolated_vectors = (
        sin_arc_complement[:, None] * start_vector[None, :]
        + sin_arc_progress[:, None] * end_vector[None, :]
    )

    interpolated_longitudes = np.arctan2(
        interpolated_vectors[:, 1], interpolated_vectors[:, 0]
    )
    interpolated_latitudes = np.arcsin(np.clip(interpolated_vectors[:, 2], -1.0, 1.0))
    return interpolated_longitudes, interpolated_latitudes


def _gradient_magnitude_at_points(
    gaussian_process: SphericalGaussianProcess,
    longitudes_rad: np.ndarray,
    latitudes_rad: np.ndarray,
) -> np.ndarray:
    """Frobenius norm of the Jacobian (summed over outputs) on the spherical metric."""
    grad_longitude, grad_latitude = gaussian_process.jacobian(
        longitudes_rad, latitudes_rad
    )
    safe_cos_latitude = np.maximum(np.cos(latitudes_rad), 1e-3)

    if gaussian_process.is_multi_output:
        magnitude_per_component_squared = (
            (grad_longitude / safe_cos_latitude[..., None]) ** 2
            + grad_latitude ** 2
        )
        magnitude_at_points = np.sqrt(magnitude_per_component_squared.sum(axis=-1))
    else:
        magnitude_at_points = np.sqrt(
            (grad_longitude / safe_cos_latitude) ** 2 + grad_latitude ** 2
        )
    return magnitude_at_points


def curvilinear_cultural_distance(
    gaussian_process: SphericalGaussianProcess,
    longitude_start_rad: float,
    latitude_start_rad: float,
    longitude_end_rad: float,
    latitude_end_rad: float,
    n_segments: int = 32,
) -> float:
    """Integrate ‖∇x‖ along the great-circle between two points.

    Output units: the integrand uses the spherical metric (``1/cos φ`` factor
    on the longitudinal partial derivative), so the result is dimensionally
    *cultural distance per radian of arc length* integrated over the radian
    arc. Multiply by the Earth radius (6371 km) to get *cultural distance per
    km* if desired.
    """
    if n_segments < 2:
        raise ValueError("n_segments must be ≥ 2 for trapezoidal integration.")

    interpolation_parameter = np.linspace(0.0, 1.0, n_segments + 1)
    longitudes_along_arc_rad, latitudes_along_arc_rad = _spherical_slerp(
        longitude_start_rad,
        latitude_start_rad,
        longitude_end_rad,
        latitude_end_rad,
        interpolation_parameter,
    )
    gradient_magnitudes_along_arc = _gradient_magnitude_at_points(
        gaussian_process, longitudes_along_arc_rad, latitudes_along_arc_rad
    )

    arc_length = np.arccos(
        np.clip(
            np.sin(latitude_start_rad) * np.sin(latitude_end_rad)
            + np.cos(latitude_start_rad)
            * np.cos(latitude_end_rad)
            * np.cos(longitude_end_rad - longitude_start_rad),
            -1.0,
            1.0,
        )
    )
    segment_arc_length = float(arc_length) / n_segments
    trapezoidal_integrate = getattr(np, "trapezoid", None) or getattr(np, "trapz")
    integral_value = float(
        trapezoidal_integrate(gradient_magnitudes_along_arc, dx=segment_arc_length)
    )
    return integral_value

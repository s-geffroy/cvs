"""Minimal Gaussian Process regressor on the sphere with closed-form Jacobian.

The fit step solves the linear system ``(K + σ_n² I) α = y`` via Cholesky.
Prediction at a new point ``q*`` is ``μ(q*) = k_*(q*) · α`` and the spatial
Jacobian is

    ∂μ/∂(λ, φ)|_{q*} = ∂k_* / ∂(λ, φ) · α

both computed without sampling. The kernel is fixed (Matérn 3/2 on
great-circle distance, length_scale + signal_variance + noise_variance
as hyperparameters). Hyperparameter optimisation can be added later via
maximum marginal likelihood; for the prototype we use sensible defaults
documented in `docs/17_continuous_field.md`.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.linalg import cho_factor, cho_solve

from .kernels import (
    matern_3_2_sphere,
    matern_3_2_sphere_gradient,
)


@dataclass
class SphericalGaussianProcess:
    """Univariate GP on the unit sphere with Matérn 3/2 kernel.

    For multi-output regression (e.g. all 19 coordinates of (x_viz, x_score,
    affinity)), fit one ``SphericalGaussianProcess`` per output; ``α`` is the
    only per-output quantity, the Cholesky factor of ``(K + σ_n² I)`` is
    shared across outputs and can be reused.
    """

    longitudes_train: np.ndarray  # shape (N,), radians
    latitudes_train: np.ndarray  # shape (N,)
    target_values_train: np.ndarray  # shape (N,)
    length_scale: float = 0.5  # radians on the unit sphere (≈ 32° of arc)
    signal_variance: float = 1.0
    noise_variance: float = 0.05
    cholesky_factor: tuple | None = None
    alpha: np.ndarray | None = None

    def fit(self) -> "SphericalGaussianProcess":
        n_samples = len(self.longitudes_train)
        longitude_matrix = self.longitudes_train[:, None]
        latitude_matrix = self.latitudes_train[:, None]

        kernel_matrix = matern_3_2_sphere(
            longitude_matrix,
            latitude_matrix,
            longitude_matrix.T,
            latitude_matrix.T,
            length_scale=self.length_scale,
            signal_variance=self.signal_variance,
        )
        kernel_matrix_with_noise = kernel_matrix + self.noise_variance * np.eye(
            n_samples
        )
        cholesky_factor_with_lower_flag = cho_factor(
            kernel_matrix_with_noise, lower=True
        )
        alpha_coefficients = cho_solve(
            cholesky_factor_with_lower_flag, self.target_values_train
        )

        self.cholesky_factor = cholesky_factor_with_lower_flag
        self.alpha = alpha_coefficients
        return self

    def _ensure_fitted(self) -> None:
        if self.alpha is None or self.cholesky_factor is None:
            raise RuntimeError("Call .fit() first before predicting.")

    def predict(
        self, longitudes_query: np.ndarray, latitudes_query: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return ``(mean, variance)`` at the query points.

        Both inputs in radians; outputs are arrays of the same shape.
        """
        self._ensure_fitted()
        query_shape = np.asarray(longitudes_query).shape
        flat_longitudes_query = np.asarray(longitudes_query).ravel()
        flat_latitudes_query = np.asarray(latitudes_query).ravel()

        kernel_query_train = matern_3_2_sphere(
            flat_longitudes_query[:, None],
            flat_latitudes_query[:, None],
            self.longitudes_train[None, :],
            self.latitudes_train[None, :],
            length_scale=self.length_scale,
            signal_variance=self.signal_variance,
        )

        predicted_mean = kernel_query_train @ self.alpha

        v_matrix = cho_solve(self.cholesky_factor, kernel_query_train.T)
        predicted_variance = self.signal_variance - np.einsum(
            "ij,ji->i", kernel_query_train, v_matrix
        )
        predicted_variance = np.maximum(predicted_variance, 0.0)

        return (
            predicted_mean.reshape(query_shape),
            predicted_variance.reshape(query_shape),
        )

    def jacobian(
        self, longitudes_query: np.ndarray, latitudes_query: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return ``(∂μ/∂λ, ∂μ/∂φ)`` at the query points.

        Both inputs in radians. Outputs are arrays of the same shape with
        units ``[target] / radian``.
        """
        self._ensure_fitted()
        query_shape = np.asarray(longitudes_query).shape
        flat_longitudes_query = np.asarray(longitudes_query).ravel()
        flat_latitudes_query = np.asarray(latitudes_query).ravel()

        grad_longitude_kernel, grad_latitude_kernel = matern_3_2_sphere_gradient(
            self.longitudes_train[None, :],
            self.latitudes_train[None, :],
            flat_longitudes_query[:, None],
            flat_latitudes_query[:, None],
            length_scale=self.length_scale,
            signal_variance=self.signal_variance,
        )

        grad_longitude_mean = grad_longitude_kernel @ self.alpha
        grad_latitude_mean = grad_latitude_kernel @ self.alpha

        return (
            grad_longitude_mean.reshape(query_shape),
            grad_latitude_mean.reshape(query_shape),
        )

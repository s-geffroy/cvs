"""Gaussian Process regressor on the sphere — multi-output, per-sample noise, ML hyperparameter fit.

Architecture:

- A single Cholesky factorisation of ``K_θ + diag(σ_n²)`` is shared across all
  outputs (the kernel is shared, only the target vector ``y`` and the linear
  weights ``α`` differ per output). For ``N = 237`` sample points and
  ``D = 19`` outputs, this gives a ~19× speed-up over running ``D``
  independent univariate fits.
- The noise term ``σ_n²`` is **per-sample**: each training point carries its
  own variance which propagates the cascade provenance (an `observed` state
  has ``σ_n² ≈ 0.05`` while a `centroid_prior` state has ``σ_n² ≈ 1.0`` —
  the GP trusts the former and treats the latter as a softly-pinned anchor).
- Hyperparameter optimisation maximises the **negative log marginal
  likelihood** summed over outputs (``log p(Y | θ)``) via
  ``scipy.optimize.minimize`` with L-BFGS-B. Bounds are imposed on
  ``length_scale`` and a shared noise multiplier to keep the optimisation
  well-conditioned.

For prediction at ``Q`` query points:
- ``mean.shape = (Q, D)`` (or ``(Q,)`` if a single output)
- ``variance.shape = (Q,)`` (kernel-determined, independent of output)
- ``jacobian.shape = (Q, D)`` per spatial direction
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
from scipy.linalg import cho_factor, cho_solve, solve_triangular
from scipy.optimize import minimize

from .kernels import (
    matern_3_2_sphere,
    matern_3_2_sphere_gradient,
)


@dataclass
class SphericalGaussianProcess:
    """Multi-output GP on the unit sphere with Matérn 3/2 kernel.

    Targets can be 1-D ``(N,)`` for a single output or 2-D ``(N, D)`` for D
    outputs sharing the same kernel. Noise can be a scalar (uniform) or a
    1-D vector ``(N,)`` (per-sample, used to weight observations by
    cascade provenance).
    """

    longitudes_train: np.ndarray  # shape (N,), radians
    latitudes_train: np.ndarray  # shape (N,)
    target_values_train: np.ndarray  # shape (N,) or (N, D)
    length_scale: float = 0.5  # radians on the unit sphere (≈ 32° of arc)
    signal_variance: float = 1.0
    noise_variance: float | np.ndarray = 0.05  # scalar or shape (N,)
    cholesky_factor: tuple | None = None
    alpha: np.ndarray | None = None  # shape (N,) or (N, D)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def n_samples(self) -> int:
        return self.longitudes_train.shape[0]

    @property
    def is_multi_output(self) -> bool:
        return self.target_values_train.ndim == 2

    @property
    def n_outputs(self) -> int:
        if self.is_multi_output:
            return self.target_values_train.shape[1]
        return 1

    def _noise_diagonal(self) -> np.ndarray:
        if np.isscalar(self.noise_variance):
            return np.full(self.n_samples, float(self.noise_variance))
        noise_array = np.asarray(self.noise_variance, dtype=float)
        if noise_array.shape != (self.n_samples,):
            raise ValueError(
                f"noise_variance must be scalar or shape ({self.n_samples},), "
                f"got {noise_array.shape}"
            )
        return noise_array

    def _kernel_matrix(self, length_scale: float, signal_variance: float) -> np.ndarray:
        longitude_matrix = self.longitudes_train[:, None]
        latitude_matrix = self.latitudes_train[:, None]
        return matern_3_2_sphere(
            longitude_matrix,
            latitude_matrix,
            longitude_matrix.T,
            latitude_matrix.T,
            length_scale=length_scale,
            signal_variance=signal_variance,
        )

    def fit(self) -> "SphericalGaussianProcess":
        kernel_matrix = self._kernel_matrix(self.length_scale, self.signal_variance)
        noise_diagonal = self._noise_diagonal()
        kernel_matrix_with_noise = kernel_matrix + np.diag(noise_diagonal)
        cholesky_factor_with_lower_flag = cho_factor(
            kernel_matrix_with_noise, lower=True
        )
        alpha_coefficients = cho_solve(
            cholesky_factor_with_lower_flag, self.target_values_train
        )
        self.cholesky_factor = cholesky_factor_with_lower_flag
        self.alpha = alpha_coefficients
        return self

    def fit_hyperparameters(
        self,
        length_scale_bounds: tuple[float, float] = (0.05, 2.0),
        noise_scale_bounds: tuple[float, float] = (0.01, 5.0),
        n_restarts: int = 3,
        random_seed: int = 11,
    ) -> "SphericalGaussianProcess":
        """Maximise the marginal likelihood over ``(length_scale, noise_scale)``.

        ``noise_scale`` is a multiplicative factor applied to the *base* noise
        vector — preserves the relative noise pattern (provenance weighting)
        while letting the optimiser pick the right absolute level.
        """
        base_noise_diagonal = self._noise_diagonal().copy()

        def negative_log_marginal_likelihood(parameters: np.ndarray) -> float:
            log_length_scale, log_noise_scale = parameters
            length_scale_candidate = float(np.exp(log_length_scale))
            noise_scale_candidate = float(np.exp(log_noise_scale))
            kernel_matrix_candidate = self._kernel_matrix(
                length_scale_candidate, self.signal_variance
            )
            kernel_with_noise = kernel_matrix_candidate + np.diag(
                noise_scale_candidate * base_noise_diagonal
            )
            try:
                cholesky_factor_with_flag = cho_factor(kernel_with_noise, lower=True)
            except Exception:  # noqa: BLE001 — fallback for numerically singular Σ
                return 1e15
            alpha_candidate = cho_solve(
                cholesky_factor_with_flag, self.target_values_train
            )

            if self.is_multi_output:
                quadratic_form = float(
                    np.sum(self.target_values_train * alpha_candidate)
                )
                n_outputs = self.target_values_train.shape[1]
            else:
                quadratic_form = float(self.target_values_train @ alpha_candidate)
                n_outputs = 1

            cholesky_lower_triangular, _ = cholesky_factor_with_flag
            log_determinant_kernel = 2.0 * float(
                np.sum(np.log(np.diag(cholesky_lower_triangular)))
            )

            nlml = 0.5 * quadratic_form + 0.5 * n_outputs * (
                log_determinant_kernel + self.n_samples * np.log(2.0 * np.pi)
            )
            return float(nlml)

        rng = np.random.default_rng(random_seed)
        log_length_lower, log_length_upper = (
            np.log(length_scale_bounds[0]),
            np.log(length_scale_bounds[1]),
        )
        log_noise_lower, log_noise_upper = (
            np.log(noise_scale_bounds[0]),
            np.log(noise_scale_bounds[1]),
        )

        best_result = None
        for restart_index in range(n_restarts):
            initial_log_length = rng.uniform(log_length_lower, log_length_upper)
            initial_log_noise = rng.uniform(log_noise_lower, log_noise_upper)
            try:
                result = minimize(
                    negative_log_marginal_likelihood,
                    x0=np.array([initial_log_length, initial_log_noise]),
                    method="L-BFGS-B",
                    bounds=[
                        (log_length_lower, log_length_upper),
                        (log_noise_lower, log_noise_upper),
                    ],
                    options={"maxiter": 200, "ftol": 1e-7},
                )
            except Exception:  # noqa: BLE001
                continue
            if best_result is None or result.fun < best_result.fun:
                best_result = result

        if best_result is None:
            raise RuntimeError("Hyperparameter optimisation failed in all restarts.")

        self.length_scale = float(np.exp(best_result.x[0]))
        optimised_noise_scale = float(np.exp(best_result.x[1]))
        self.noise_variance = optimised_noise_scale * base_noise_diagonal

        self.metadata.update(
            {
                "ml_optimised_length_scale_rad": self.length_scale,
                "ml_optimised_noise_scale": optimised_noise_scale,
                "negative_log_marginal_likelihood": float(best_result.fun),
                "n_restarts": n_restarts,
            }
        )

        return self.fit()

    def _ensure_fitted(self) -> None:
        if self.alpha is None or self.cholesky_factor is None:
            raise RuntimeError("Call .fit() (or .fit_hyperparameters()) first.")

    def _kernel_query_train(
        self,
        longitudes_query: np.ndarray,
        latitudes_query: np.ndarray,
    ) -> np.ndarray:
        flat_longitudes_query = np.asarray(longitudes_query).ravel()
        flat_latitudes_query = np.asarray(latitudes_query).ravel()
        return matern_3_2_sphere(
            flat_longitudes_query[:, None],
            flat_latitudes_query[:, None],
            self.longitudes_train[None, :],
            self.latitudes_train[None, :],
            length_scale=self.length_scale,
            signal_variance=self.signal_variance,
        )

    def predict(
        self, longitudes_query: np.ndarray, latitudes_query: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return ``(mean, variance)`` at the query points.

        - ``mean.shape`` is ``query_shape + (D,)`` for multi-output, otherwise
          ``query_shape``.
        - ``variance.shape`` is always ``query_shape`` (kernel-only, single
          predictive variance independent of the output).
        """
        self._ensure_fitted()
        query_shape = np.asarray(longitudes_query).shape
        kernel_query_train = self._kernel_query_train(
            longitudes_query, latitudes_query
        )

        predicted_mean_flat = kernel_query_train @ self.alpha
        v_matrix = cho_solve(self.cholesky_factor, kernel_query_train.T)
        predicted_variance_flat = self.signal_variance - np.einsum(
            "ij,ji->i", kernel_query_train, v_matrix
        )
        predicted_variance_flat = np.maximum(predicted_variance_flat, 0.0)

        if self.is_multi_output:
            mean_shape = query_shape + (self.n_outputs,)
            return (
                predicted_mean_flat.reshape(mean_shape),
                predicted_variance_flat.reshape(query_shape),
            )
        return (
            predicted_mean_flat.reshape(query_shape),
            predicted_variance_flat.reshape(query_shape),
        )

    def jacobian(
        self, longitudes_query: np.ndarray, latitudes_query: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return ``(∂μ/∂λ, ∂μ/∂φ)`` at the query points.

        For multi-output, both gradients have shape ``query_shape + (D,)``.
        Single-output keeps the original ``query_shape``.
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

        if self.is_multi_output:
            output_shape = query_shape + (self.n_outputs,)
            return (
                grad_longitude_mean.reshape(output_shape),
                grad_latitude_mean.reshape(output_shape),
            )
        return (
            grad_longitude_mean.reshape(query_shape),
            grad_latitude_mean.reshape(query_shape),
        )

"""Optimal transport on the civilization simplex (Sinkhorn, NumPy-only)."""
from __future__ import annotations

import numpy as np


def sinkhorn_wasserstein_squared(
    weights_source: np.ndarray,
    weights_target: np.ndarray,
    ground_cost_squared: np.ndarray,
    entropic_reg: float = 0.05,
    max_iter: int = 500,
    tol: float = 1e-9,
) -> float:
    """Return the entropic-regularised squared Wasserstein-2 cost.

    Parameters
    ----------
    weights_source : (n,) probability vector on the simplex
    weights_target : (n,) probability vector on the simplex
    ground_cost_squared : (n, n) squared ground distances D_ij^2
    entropic_reg : Sinkhorn regularisation parameter (lambda)
    """
    weights_source = np.asarray(weights_source, dtype=float)
    weights_target = np.asarray(weights_target, dtype=float)
    if weights_source.shape != weights_target.shape:
        raise ValueError("weights_source and weights_target must have the same shape")
    cost_squared = np.asarray(ground_cost_squared, dtype=float)
    if cost_squared.shape != (weights_source.size, weights_target.size):
        raise ValueError("ground_cost_squared must be (n, n)")

    kernel = np.exp(-cost_squared / entropic_reg)
    kernel = np.maximum(kernel, 1e-300)

    log_u = np.zeros_like(weights_source)
    log_v = np.zeros_like(weights_target)
    log_a = np.log(np.maximum(weights_source, 1e-300))
    log_b = np.log(np.maximum(weights_target, 1e-300))
    log_kernel = np.log(kernel)

    for _ in range(max_iter):
        log_u_new = log_a - _log_sum_exp(log_kernel + log_v[None, :], axis=1)
        log_v_new = log_b - _log_sum_exp(log_kernel + log_u_new[:, None], axis=0)
        if (
            np.max(np.abs(log_u_new - log_u)) < tol
            and np.max(np.abs(log_v_new - log_v)) < tol
        ):
            log_u = log_u_new
            log_v = log_v_new
            break
        log_u = log_u_new
        log_v = log_v_new

    log_plan = log_u[:, None] + log_kernel + log_v[None, :]
    plan = np.exp(log_plan)
    transport_cost = float(np.sum(plan * cost_squared))
    return max(transport_cost, 0.0)


def _log_sum_exp(matrix: np.ndarray, axis: int) -> np.ndarray:
    max_val = np.max(matrix, axis=axis, keepdims=True)
    return (max_val + np.log(np.sum(np.exp(matrix - max_val), axis=axis, keepdims=True))).squeeze(
        axis=axis
    )

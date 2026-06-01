"""External validation of w_s against three independent indicators (doc 12).

The three indicators chosen are all public, with stable identifiers:

- **Pew Religious Composition** : religious-majority share per country
  (Pew Research Center, 2020 update of the 2010 global landscape study).
  We aggregate to a single proxy: ``share_dominant_religion``.
- **WGI** (Worldwide Governance Indicators, World Bank) : six aggregate
  scores per country. We use ``rule_of_law`` (zscore, 2022) as the
  governance proxy.
- **FSI** (Fragility States Index, Fund For Peace, 2024) : aggregate
  fragility score, 0 (stable) to 120 (alert).

For each external indicator we compute Spearman correlations between
the indicator and **each civilization weight** ``w_s[i]`` across the
panel of states with both signals available, plus bootstrap 95% CIs.

Bundled datasets (small, public): committed under data_sources/ so the
analysis is reproducible offline. The fetcher functions are kept here
for reference but are NOT executed at site build time.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from apps.basis_builder.centroids import compute_centroids
from apps.basis_builder.paths import DATA_SOURCES_DIR, EMPIRICAL_DIR
from apps.basis_builder.projector import project_states

PEW_RELIGIOUS_PATH = DATA_SOURCES_DIR / "pew" / "religious_composition_2020.json"
WGI_PATH = DATA_SOURCES_DIR / "wgi" / "rule_of_law_2022.json"
FSI_PATH = DATA_SOURCES_DIR / "fsi" / "fragility_states_index_2024.json"


def _spearman_correlation(values_a: np.ndarray, values_b: np.ndarray) -> float:
    if values_a.shape != values_b.shape or values_a.size < 3:
        return float("nan")
    rank_a = np.argsort(np.argsort(values_a)).astype(float)
    rank_b = np.argsort(np.argsort(values_b)).astype(float)
    rank_a -= rank_a.mean()
    rank_b -= rank_b.mean()
    denominator = float(np.sqrt(float(rank_a @ rank_a) * float(rank_b @ rank_b)))
    if denominator < 1e-12:
        return float("nan")
    return float(rank_a @ rank_b / denominator)


def _bootstrap_confidence_interval(
    values_a: np.ndarray,
    values_b: np.ndarray,
    n_bootstrap: int = 1000,
    seed: int = 42,
    confidence_level: float = 0.95,
) -> tuple[float, float]:
    if values_a.size < 4:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    n_samples = values_a.size
    bootstrap_estimates: list[float] = []
    for _ in range(n_bootstrap):
        indices = rng.integers(0, n_samples, size=n_samples)
        bootstrap_estimates.append(_spearman_correlation(values_a[indices], values_b[indices]))
    bootstrap_estimates_array = np.asarray(bootstrap_estimates, dtype=float)
    finite_estimates = bootstrap_estimates_array[np.isfinite(bootstrap_estimates_array)]
    if finite_estimates.size < 10:
        return (float("nan"), float("nan"))
    lower_percentile = (1.0 - confidence_level) / 2.0 * 100
    upper_percentile = (1.0 + confidence_level) / 2.0 * 100
    return (
        float(np.percentile(finite_estimates, lower_percentile)),
        float(np.percentile(finite_estimates, upper_percentile)),
    )


def _load_external_indicator(indicator_path: Path) -> dict[str, float]:
    if not indicator_path.exists():
        return {}
    payload = json.loads(indicator_path.read_text())
    return {entry["iso3"]: float(entry["value"]) for entry in payload.get("values", [])}


def correlate_affinity_with_indicator(
    affinity_matrix: np.ndarray,
    iso3_order: list[str],
    civilization_ids: list[str],
    indicator_by_iso3: dict[str, float],
) -> list[dict]:
    indicator_values = np.array(
        [indicator_by_iso3.get(iso3, np.nan) for iso3 in iso3_order], dtype=float
    )
    valid_mask = ~np.isnan(indicator_values)
    n_valid = int(valid_mask.sum())
    correlation_records: list[dict] = []
    if n_valid < 3:
        return correlation_records
    for civilization_index, civilization_id in enumerate(civilization_ids):
        weight_values = affinity_matrix[valid_mask, civilization_index]
        indicator_subset = indicator_values[valid_mask]
        spearman_rho = _spearman_correlation(weight_values, indicator_subset)
        ci_lower, ci_upper = _bootstrap_confidence_interval(weight_values, indicator_subset)
        correlation_records.append(
            {
                "civilization_id": civilization_id,
                "n_states_paired": n_valid,
                "spearman_rho": spearman_rho,
                "bootstrap_ci_95_lower": ci_lower,
                "bootstrap_ci_95_upper": ci_upper,
            }
        )
    correlation_records.sort(
        key=lambda record: abs(record["spearman_rho"])
        if not np.isnan(record["spearman_rho"]) else -1.0,
        reverse=True,
    )
    return correlation_records


def run_external_validation() -> dict:
    centroids = compute_centroids()
    state_coordinates = project_states(centroids)
    civilization_ids = list(centroids.keys())

    iso3_order: list[str] = []
    affinity_rows: list[np.ndarray] = []
    for iso3, state in state_coordinates.items():
        if not state.affinity_vector:
            continue
        weight_array = np.array(
            [state.affinity_vector.get(civilization_id, 0.0)
             for civilization_id in civilization_ids],
            dtype=float,
        )
        iso3_order.append(iso3)
        affinity_rows.append(weight_array)
    affinity_matrix = np.asarray(affinity_rows, dtype=float)

    indicators = {
        "pew_dominant_religion_share_2020": _load_external_indicator(PEW_RELIGIOUS_PATH),
        "wgi_rule_of_law_2022": _load_external_indicator(WGI_PATH),
        "fsi_total_2024": _load_external_indicator(FSI_PATH),
    }

    per_indicator_correlations: dict[str, dict] = {}
    for indicator_id, indicator_data in indicators.items():
        correlations = correlate_affinity_with_indicator(
            affinity_matrix, iso3_order, civilization_ids, indicator_data
        )
        per_indicator_correlations[indicator_id] = {
            "indicator_id": indicator_id,
            "n_states_with_indicator_value": len(indicator_data),
            "correlations_per_civilization": correlations,
        }

    return {
        "_meta": {
            "method": "spearman_correlation_w_s_vs_external",
            "indicators_used": list(indicators.keys()),
            "civilization_id_order": civilization_ids,
            "iso3_order": iso3_order,
        },
        "indicators": per_indicator_correlations,
    }


def run_external_validation_and_write() -> str:
    EMPIRICAL_DIR.mkdir(parents=True, exist_ok=True)
    payload = run_external_validation()
    output_path = EMPIRICAL_DIR / "external_validation.json"
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return str(output_path)

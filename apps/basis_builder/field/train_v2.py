"""V2 training: multi-output GP on 19 components, 1° grid, ML-optimised hyperparameters.

Components fitted simultaneously (sharing the Cholesky factorisation):
- ``x_viz`` : ``ts``, ``se``
- ``x_score`` : ``pdi``, ``idv``, ``mas``, ``uai``, ``lto``, ``ivr``
- ``affinity_vector`` : 11 civilisations (western, orthodox, islamic, sinic,
  hindic, japanese, buddhist, latin_american, african, indigenous, oceanian)

Per-sample noise reflects the cascade provenance: ``observed`` states get a
low base noise (clear signal), ``imputed_*`` states get progressively
higher noise (the GP is allowed to interpolate around them), and
``centroid_prior`` states act as soft anchors only.

The noise multiplier is learned by maximum marginal likelihood within
``[noise_scale_bounds]``, jointly with the length scale.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from apps.basis_builder.paths import BASIS_DIR, STATE_COORDINATES_PATH
from packages.civvec_core.continuous_field.gp import SphericalGaussianProcess
from packages.civvec_core.continuous_field.sample_points import (
    SAMPLE_POINTS_PATH,
    generate_sample_points_per_state,
)

CONTINUOUS_FIELD_V2_META_PATH = BASIS_DIR / "continuous_field_v2_meta.json"
CONTINUOUS_FIELD_V2_ARRAYS_PATH = BASIS_DIR / "continuous_field_v2_arrays.npz"

X_VIZ_COMPONENT_NAMES: tuple[str, ...] = ("ts", "se")
X_SCORE_COMPONENT_NAMES: tuple[str, ...] = ("pdi", "idv", "mas", "uai", "lto", "ivr")
CIVILIZATION_IDS_ORDER: tuple[str, ...] = (
    "western",
    "orthodox",
    "islamic",
    "sinic",
    "hindic",
    "japanese",
    "buddhist",
    "latin_american",
    "african",
    "indigenous",
    "oceanian",
)

COMPONENT_NAMES: tuple[str, ...] = (
    *(f"x_viz_{name}" for name in X_VIZ_COMPONENT_NAMES),
    *(f"x_score_{name}" for name in X_SCORE_COMPONENT_NAMES),
    *(f"affinity_{civ}" for civ in CIVILIZATION_IDS_ORDER),
)


PROVENANCE_BASE_NOISE: dict[str, float] = {
    "observed": 0.05,
    "observed_with_dim_imputation": 0.10,
    "imputed_wvs_items": 0.25,
    "imputed_pew": 0.45,
    "imputed_governance": 0.45,
    "centroid_prior": 1.20,
    "unresolved": 1.50,
}


@dataclass
class V2FieldArtefacts:
    grid_longitudes_deg: np.ndarray
    grid_latitudes_deg: np.ndarray
    predicted_mean_per_component: dict[str, np.ndarray]
    predicted_variance_grid: np.ndarray
    gradient_longitude_per_component: dict[str, np.ndarray]
    gradient_latitude_per_component: dict[str, np.ndarray]
    gradient_magnitude_per_component: dict[str, np.ndarray]
    z_score_means: dict[str, float]
    z_score_stds: dict[str, float]
    n_training_points: int
    hyperparameters: dict
    component_names: tuple[str, ...]


def _load_sample_points() -> list[dict]:
    if not SAMPLE_POINTS_PATH.exists():
        generate_sample_points_per_state()
    payload = json.loads(SAMPLE_POINTS_PATH.read_text())
    return payload["sample_points"]


def _state_records_by_iso3() -> dict[str, dict]:
    payload = json.loads(STATE_COORDINATES_PATH.read_text())
    return {state["iso3"]: state for state in payload["states"]}


def _component_targets_from_state(state: dict) -> np.ndarray:
    """Return a (n_components,) vector for the state, NaN where missing."""
    components: list[float] = []
    for value in state["x_viz"]:
        components.append(float(value) if value is not None else float("nan"))
    for value in state["x_score"]:
        components.append(float(value) if value is not None else float("nan"))
    affinity_vector = state.get("affinity_vector", {})
    for civilization_id in CIVILIZATION_IDS_ORDER:
        components.append(float(affinity_vector.get(civilization_id, 0.0)))
    return np.array(components, dtype=float)


def _noise_for_state(state: dict) -> float:
    """Combine x_viz and x_score provenance into a single per-state base noise."""
    viz_provenance = state["data_quality"].get("x_viz_provenance", "unresolved")
    score_provenance = state["data_quality"].get("x_score_provenance", "unresolved")
    viz_noise = PROVENANCE_BASE_NOISE.get(viz_provenance, 1.5)
    score_noise = PROVENANCE_BASE_NOISE.get(score_provenance, 1.5)
    return 0.5 * (viz_noise + score_noise)


def _build_training_arrays(
    sample_points: list[dict],
    states_by_iso3: dict[str, dict],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    longitudes_train_rad: list[float] = []
    latitudes_train_rad: list[float] = []
    target_rows: list[np.ndarray] = []
    noise_rows: list[float] = []
    for sample_point in sample_points:
        iso3 = sample_point["iso3"]
        state = states_by_iso3.get(iso3)
        if state is None:
            continue
        target_vector = _component_targets_from_state(state)
        if np.any(np.isnan(target_vector)):
            continue
        longitudes_train_rad.append(np.deg2rad(sample_point["longitude_deg"]))
        latitudes_train_rad.append(np.deg2rad(sample_point["latitude_deg"]))
        target_rows.append(target_vector)
        cluster_weight = float(sample_point.get("weight", 1.0))
        base_noise = _noise_for_state(state)
        # Smaller weight (less population in this cluster) → larger noise so the
        # GP relies less on minor clusters of a country.
        effective_noise = base_noise / max(cluster_weight, 0.05)
        noise_rows.append(effective_noise)
    return (
        np.array(longitudes_train_rad),
        np.array(latitudes_train_rad),
        np.array(target_rows),
        np.array(noise_rows),
    )


def train_v2_field(
    grid_step_deg: float = 1.0,
    optimise_hyperparameters: bool = True,
) -> V2FieldArtefacts:
    sample_points = _load_sample_points()
    states_by_iso3 = _state_records_by_iso3()

    (
        longitudes_train_rad,
        latitudes_train_rad,
        target_matrix_raw,
        noise_vector,
    ) = _build_training_arrays(sample_points, states_by_iso3)

    z_score_means_per_component = {
        component_name: float(target_matrix_raw[:, component_index].mean())
        for component_index, component_name in enumerate(COMPONENT_NAMES)
    }
    z_score_stds_per_component = {
        component_name: float(target_matrix_raw[:, component_index].std() + 1e-9)
        for component_index, component_name in enumerate(COMPONENT_NAMES)
    }

    target_matrix_normalised = np.array(
        [
            (target_matrix_raw[:, component_index] - z_score_means_per_component[component_name])
            / z_score_stds_per_component[component_name]
            for component_index, component_name in enumerate(COMPONENT_NAMES)
        ]
    ).T

    gp_multi = SphericalGaussianProcess(
        longitudes_train=longitudes_train_rad,
        latitudes_train=latitudes_train_rad,
        target_values_train=target_matrix_normalised,
        length_scale=0.4,
        signal_variance=1.0,
        noise_variance=noise_vector,
    )

    if optimise_hyperparameters:
        gp_multi.fit_hyperparameters(
            length_scale_bounds=(0.1, 1.5),
            noise_scale_bounds=(0.02, 5.0),
            n_restarts=3,
        )
    else:
        gp_multi.fit()

    grid_longitudes_deg = np.arange(-180.0, 180.0, grid_step_deg)
    grid_latitudes_deg = np.arange(-90.0, 90.0 + grid_step_deg / 2, grid_step_deg)
    longitudes_grid, latitudes_grid = np.meshgrid(
        grid_longitudes_deg, grid_latitudes_deg
    )
    longitudes_grid_rad = np.deg2rad(longitudes_grid)
    latitudes_grid_rad = np.deg2rad(latitudes_grid)

    predicted_mean_normalised, predicted_variance_normalised = gp_multi.predict(
        longitudes_grid_rad, latitudes_grid_rad
    )
    grad_longitude_normalised, grad_latitude_normalised = gp_multi.jacobian(
        longitudes_grid_rad, latitudes_grid_rad
    )

    predicted_mean_per_component: dict[str, np.ndarray] = {}
    gradient_longitude_per_component: dict[str, np.ndarray] = {}
    gradient_latitude_per_component: dict[str, np.ndarray] = {}
    gradient_magnitude_per_component: dict[str, np.ndarray] = {}

    metric_factor_per_radian_longitude = np.cos(latitudes_grid_rad)
    polar_mask = np.abs(latitudes_grid) >= 75.0
    safe_metric_factor = np.where(
        polar_mask, np.nan, np.maximum(metric_factor_per_radian_longitude, 1e-3)
    )

    for component_index, component_name in enumerate(COMPONENT_NAMES):
        std = z_score_stds_per_component[component_name]
        mean = z_score_means_per_component[component_name]
        predicted_mean_per_component[component_name] = (
            predicted_mean_normalised[..., component_index] * std + mean
        )
        gradient_longitude_per_component[component_name] = (
            grad_longitude_normalised[..., component_index] * std
        )
        gradient_latitude_per_component[component_name] = (
            grad_latitude_normalised[..., component_index] * std
        )
        gradient_magnitude_per_component[component_name] = np.sqrt(
            (gradient_longitude_per_component[component_name] / safe_metric_factor) ** 2
            + gradient_latitude_per_component[component_name] ** 2
        )

    return V2FieldArtefacts(
        grid_longitudes_deg=longitudes_grid,
        grid_latitudes_deg=latitudes_grid,
        predicted_mean_per_component=predicted_mean_per_component,
        predicted_variance_grid=predicted_variance_normalised,
        gradient_longitude_per_component=gradient_longitude_per_component,
        gradient_latitude_per_component=gradient_latitude_per_component,
        gradient_magnitude_per_component=gradient_magnitude_per_component,
        z_score_means=z_score_means_per_component,
        z_score_stds=z_score_stds_per_component,
        n_training_points=len(longitudes_train_rad),
        hyperparameters={
            "length_scale_rad": gp_multi.length_scale,
            "length_scale_km_earth": gp_multi.length_scale * 6371.0,
            "noise_variance_mean": float(np.mean(gp_multi.noise_variance)),
            **gp_multi.metadata,
        },
        component_names=COMPONENT_NAMES,
    )


def write_v2_artefacts(artefacts: V2FieldArtefacts) -> tuple[Path, Path]:
    """Persist a small JSON metadata sidecar + a compressed numpy archive.

    The arrays (~6 floats × 19 components × 65 000 cells) are ~50 MB raw but
    compress to ~10 MB via ``np.savez_compressed``. The JSON sidecar keeps
    the hyperparameters, grid, and z-score stats human-readable and small
    enough to commit. Callers load the archive lazily via ``np.load``.
    """
    array_names_per_component = (
        "predicted_mean",
        "gradient_longitude",
        "gradient_latitude",
        "gradient_magnitude",
    )

    arrays_payload: dict[str, np.ndarray] = {
        "predicted_variance": artefacts.predicted_variance_grid.astype(np.float32),
    }
    for component_name in artefacts.component_names:
        arrays_payload[f"{component_name}__predicted_mean"] = (
            artefacts.predicted_mean_per_component[component_name].astype(np.float32)
        )
        arrays_payload[f"{component_name}__gradient_longitude"] = (
            artefacts.gradient_longitude_per_component[component_name].astype(np.float32)
        )
        arrays_payload[f"{component_name}__gradient_latitude"] = (
            artefacts.gradient_latitude_per_component[component_name].astype(np.float32)
        )
        arrays_payload[f"{component_name}__gradient_magnitude"] = (
            artefacts.gradient_magnitude_per_component[component_name].astype(np.float32)
        )

    CONTINUOUS_FIELD_V2_ARRAYS_PATH.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(CONTINUOUS_FIELD_V2_ARRAYS_PATH, **arrays_payload)

    metadata_payload = {
        "_meta": {
            "schema": "continuous_field_v2_meta.schema.json",
            "n_training_points": artefacts.n_training_points,
            "n_components": len(artefacts.component_names),
            "component_names": list(artefacts.component_names),
            "hyperparameters": artefacts.hyperparameters,
            "grid_step_deg": float(
                artefacts.grid_longitudes_deg[0, 1]
                - artefacts.grid_longitudes_deg[0, 0]
            ),
            "z_score_means": artefacts.z_score_means,
            "z_score_stds": artefacts.z_score_stds,
            "array_names_per_component": list(array_names_per_component),
            "documentation": "docs/17_continuous_field.md",
            "provenance_base_noise": PROVENANCE_BASE_NOISE,
            "arrays_archive_path": str(
                CONTINUOUS_FIELD_V2_ARRAYS_PATH.relative_to(BASIS_DIR.parents[2])
            ),
        },
        "grid": {
            "longitudes_deg": artefacts.grid_longitudes_deg[0, :].tolist(),
            "latitudes_deg": artefacts.grid_latitudes_deg[:, 0].tolist(),
        },
    }
    CONTINUOUS_FIELD_V2_META_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTINUOUS_FIELD_V2_META_PATH.write_text(
        json.dumps(metadata_payload, indent=2, ensure_ascii=False)
    )
    return CONTINUOUS_FIELD_V2_META_PATH, CONTINUOUS_FIELD_V2_ARRAYS_PATH


if __name__ == "__main__":
    import os

    trained_artefacts = train_v2_field()
    metadata_path, arrays_path = write_v2_artefacts(trained_artefacts)
    print(
        f"Wrote {metadata_path.name} ({os.path.getsize(metadata_path) // 1024} KB) + "
        f"{arrays_path.name} ({os.path.getsize(arrays_path) // (1024 * 1024)} MB): "
        f"{trained_artefacts.n_training_points} training points × "
        f"{len(trained_artefacts.component_names)} components → "
        f"{trained_artefacts.predicted_variance_grid.size} grid cells "
        f"(length_scale={trained_artefacts.hyperparameters['length_scale_rad']:.3f} rad)."
    )

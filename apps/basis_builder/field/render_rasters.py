"""Generate PNG rasters of the continuous field for MapLibre image overlays.

For each (component, metric) couple we render one PNG covering the world
in equirectangular projection (the MapLibre raster source then warps it
to Mercator). The PNG dimensions match the grid (360 × 181 for the V2
1°-spaced grid).

Metrics rendered per component:
- ``mean`` — predicted value ``μ`` (signed colormap RdBu_r)
- ``grad_magnitude`` — fault lines ``‖∇μ‖`` (perceptual colormap Plasma)

Output: ``site_src/docs/assets/data/continuous_field/<component>_<metric>.png``
+ a small ``site_src/docs/assets/data/continuous_field/index.json`` listing
the available rasters with their min/max for legend rendering.

The PNG vertical axis is flipped so latitude 90° (north) is at the top —
standard image convention required by MapLibre.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from matplotlib import colormaps as matplotlib_colormaps
from matplotlib.colors import Normalize
from PIL import Image

from apps.basis_builder.field.train_v2 import (
    CONTINUOUS_FIELD_V2_ARRAYS_PATH,
    CONTINUOUS_FIELD_V2_META_PATH,
)
from apps.basis_builder.paths import REPO_ROOT

RASTERS_OUTPUT_DIR = (
    REPO_ROOT / "site_src" / "docs" / "assets" / "data" / "continuous_field"
)

COMPONENTS_TO_RENDER: tuple[str, ...] = (
    "x_viz_ts",
    "x_viz_se",
    "x_score_pdi",
    "x_score_idv",
    "x_score_mas",
    "x_score_uai",
    "x_score_lto",
    "x_score_ivr",
)


@dataclass
class RasterRecord:
    component_name: str
    metric_name: str
    filename: str
    colormap_name: str
    value_min: float
    value_max: float
    physical_units: str
    description_fr: str


def _flip_for_image(grid_array: np.ndarray) -> np.ndarray:
    """MapLibre expects raster origin top-left → flip latitude axis."""
    return np.flipud(grid_array)


def _array_to_png_with_colormap(
    grid_array: np.ndarray,
    output_path: Path,
    colormap_name: str,
    value_range: tuple[float, float],
) -> None:
    normalisation = Normalize(vmin=value_range[0], vmax=value_range[1], clip=True)
    colormap = matplotlib_colormaps[colormap_name]
    normalised_array = normalisation(_flip_for_image(grid_array))
    rgba_float = colormap(normalised_array.filled(0.5) if hasattr(normalised_array, "filled") else normalised_array)

    nan_mask = ~np.isfinite(_flip_for_image(grid_array))
    rgba_byte = (rgba_float * 255.0).astype(np.uint8)
    rgba_byte[..., 3] = np.where(nan_mask, 0, rgba_byte[..., 3])

    Image.fromarray(rgba_byte, mode="RGBA").save(output_path, format="PNG")


def _value_range_robust(
    grid_array: np.ndarray, lower_quantile: float, upper_quantile: float
) -> tuple[float, float]:
    finite_values = grid_array[np.isfinite(grid_array)]
    if finite_values.size == 0:
        return 0.0, 1.0
    return (
        float(np.quantile(finite_values, lower_quantile)),
        float(np.quantile(finite_values, upper_quantile)),
    )


def render_rasters_for_field() -> list[RasterRecord]:
    if not CONTINUOUS_FIELD_V2_ARRAYS_PATH.exists():
        raise FileNotFoundError(
            "Run `python -m apps.basis_builder.field.train_v2` first to produce "
            f"{CONTINUOUS_FIELD_V2_ARRAYS_PATH}."
        )
    metadata = json.loads(CONTINUOUS_FIELD_V2_META_PATH.read_text())
    arrays = np.load(CONTINUOUS_FIELD_V2_ARRAYS_PATH)
    RASTERS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    records: list[RasterRecord] = []

    metric_specifications = (
        (
            "mean",
            "predicted_mean",
            "RdBu_r",
            (0.02, 0.98),
            "Valeur prédite μ par le GP, échelle signée centrée sur la moyenne globale.",
        ),
        (
            "grad_magnitude",
            "gradient_magnitude",
            "plasma",
            (0.0, 0.98),
            "Magnitude du gradient ‖∇μ‖ — fault lines civilisationnelles.",
        ),
    )

    for component_name in COMPONENTS_TO_RENDER:
        for (
            metric_short,
            array_suffix,
            colormap_name,
            quantile_range,
            description_fr,
        ) in metric_specifications:
            array_key = f"{component_name}__{array_suffix}"
            if array_key not in arrays.files:
                continue
            grid_array = np.array(arrays[array_key])
            value_range = _value_range_robust(grid_array, *quantile_range)
            output_filename = f"{component_name}_{metric_short}.png"
            output_path = RASTERS_OUTPUT_DIR / output_filename
            _array_to_png_with_colormap(
                grid_array, output_path, colormap_name, value_range
            )
            records.append(
                RasterRecord(
                    component_name=component_name,
                    metric_name=metric_short,
                    filename=output_filename,
                    colormap_name=colormap_name,
                    value_min=value_range[0],
                    value_max=value_range[1],
                    physical_units=metadata["_meta"]
                    .get("z_score_stds", {})
                    .get(component_name, ""),
                    description_fr=description_fr,
                )
            )

    grid_longitudes_deg = metadata["grid"]["longitudes_deg"]
    grid_latitudes_deg = metadata["grid"]["latitudes_deg"]
    index_payload = {
        "_meta": {
            "schema": "continuous_field_rasters_index.schema.json",
            "n_rasters": len(records),
            "grid_step_deg": metadata["_meta"]["grid_step_deg"],
            "documentation": "docs/17_continuous_field.md",
        },
        "bbox": {
            "longitude_min_deg": float(min(grid_longitudes_deg)),
            "longitude_max_deg": float(max(grid_longitudes_deg)),
            "latitude_min_deg": float(min(grid_latitudes_deg)),
            "latitude_max_deg": float(max(grid_latitudes_deg)),
        },
        "rasters": [
            {
                "component": record.component_name,
                "metric": record.metric_name,
                "filename": record.filename,
                "colormap": record.colormap_name,
                "value_min": record.value_min,
                "value_max": record.value_max,
                "description_fr": record.description_fr,
            }
            for record in records
        ],
    }
    (RASTERS_OUTPUT_DIR / "index.json").write_text(
        json.dumps(index_payload, indent=2, ensure_ascii=False)
    )
    return records


if __name__ == "__main__":
    rendered_records = render_rasters_for_field()
    print(f"Rendered {len(rendered_records)} rasters to {RASTERS_OUTPUT_DIR}")
    for record in rendered_records:
        print(
            f"  {record.filename}: [{record.value_min:.3f}, {record.value_max:.3f}] "
            f"colormap={record.colormap_name}"
        )

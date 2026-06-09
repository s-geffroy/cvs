"""Render the Plates & Faults artefacts (3 PNG rasters + 4 GeoJSON layers).

Reads the V2 GP outputs (``continuous_field_v2_arrays.npz`` +
``continuous_field_v2_meta.json``) and emits a Huntington-style cartography
without any GP refit:

- ``civ_plates_argmax.png`` — categorical raster, one of 11 civilisation colours per cell.
- ``civ_plates_contested_margin.png`` — choropleth of ``top1 − top2`` of the affinity simplex.
- ``civ_plates_uncertainty_mask.png`` — gray hatched mask over high-variance cells.
- ``civ_plates_faults.geojson`` — fault LineStrings, properties: ``civ_pair``, ``friction``, ``confidence``.
- ``civ_plates_faults_chevrons.geojson`` — direction markers along faults.
- ``civ_plates_triple_junctions.geojson`` — points where 3+ civilisations meet.
- ``civ_plates_enclaves.geojson`` — diaspora-like cells argmax-different from all 8 neighbours.

The output bundle is registered alongside the existing rasters in
``site_src/docs/assets/data/continuous_field/index.json`` under a new
``plates_and_faults`` key, so the existing MapLibre wiring can discover
the new layers without breaking the legacy raster discovery.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from matplotlib import colormaps as matplotlib_colormaps
from matplotlib.colors import Normalize
from PIL import Image

from apps.basis_builder.field.render_rasters import (
    CIVILIZATION_IDS_ORDER,
    RASTERS_OUTPUT_DIR,
)
from apps.basis_builder.field.train_v2 import (
    CONTINUOUS_FIELD_V2_ARRAYS_PATH,
    CONTINUOUS_FIELD_V2_META_PATH,
)
from apps.basis_builder.paths import CIVILIZATION_CENTROIDS_PATH
from packages.civvec_core.algebra.distances import (
    intra_civilizational_covariance_inverse,
)
from packages.civvec_core.continuous_field.plates_and_faults import (
    chevrons_to_geojson,
    compute_argmax_plates,
    compute_top2_margin,
    compute_uncertainty_mask,
    detect_enclaves,
    detect_triple_junctions,
    extract_fault_segments,
    merge_segments_by_civ_pair,
    merged_faults_to_geojson,
    points_to_geojson,
    sample_chevrons,
)

PLATES_AND_FAULTS_SUBDIRECTORY: str = "plates_and_faults"
# Quantile threshold for the uncertainty mask. Set to 0.6 to also mask the
# vast oceanic zones (far from any training point, hence high GP variance),
# which otherwise produce visually meaningless fault lines like
# "african__oceanian" running through the open Pacific.
UNCERTAINTY_QUANTILE_THRESHOLD: float = 0.6

CIVILIZATION_COLOR_PALETTE: dict[str, str] = {
    "western": "#1f77b4",
    "orthodox": "#9467bd",
    "islamic": "#2ca02c",
    "sinic": "#d62728",
    "hindic": "#ff7f0e",
    "japanese": "#e377c2",
    "buddhist": "#bcbd22",
    "latin_american": "#17becf",
    "african": "#8c564b",
    "indigenous": "#7f7f7f",
    "oceanian": "#aec7e8",
}


@dataclass
class PlatesAndFaultsArtefacts:
    plates_png_filename: str
    margin_png_filename: str
    uncertainty_mask_png_filename: str
    faults_geojson_filename: str
    chevrons_geojson_filename: str
    triple_junctions_geojson_filename: str
    enclaves_geojson_filename: str
    legend_entries: list[dict]
    margin_value_range: tuple[float, float]
    uncertainty_variance_threshold: float
    fault_friction_range: tuple[float, float]


def _hex_to_rgb_tuple(hex_color: str) -> tuple[int, int, int]:
    cleaned = hex_color.lstrip("#")
    return (
        int(cleaned[0:2], 16),
        int(cleaned[2:4], 16),
        int(cleaned[4:6], 16),
    )


def _flip_for_image(grid_array: np.ndarray) -> np.ndarray:
    return np.flipud(grid_array)


def _save_categorical_plates_png(
    plates_grid: np.ndarray,
    civilization_ids_ordered: list[str],
    output_path: Path,
) -> list[dict]:
    """Encode each cell as a colour from CIVILIZATION_COLOR_PALETTE."""
    height, width = plates_grid.shape
    rgba_image = np.zeros((height, width, 4), dtype=np.uint8)
    legend_entries: list[dict] = []
    for civilization_index, civilization_id in enumerate(civilization_ids_ordered):
        red, green, blue = _hex_to_rgb_tuple(
            CIVILIZATION_COLOR_PALETTE.get(civilization_id, "#cccccc")
        )
        mask_for_civilization = plates_grid == civilization_index
        rgba_image[mask_for_civilization, 0] = red
        rgba_image[mask_for_civilization, 1] = green
        rgba_image[mask_for_civilization, 2] = blue
        rgba_image[mask_for_civilization, 3] = 220
        legend_entries.append(
            {
                "civilization_id": civilization_id,
                "color_hex": CIVILIZATION_COLOR_PALETTE.get(civilization_id, "#cccccc"),
                "cell_count": int(mask_for_civilization.sum()),
            }
        )
    Image.fromarray(_flip_for_image(rgba_image), mode="RGBA").save(
        output_path, format="PNG"
    )
    return legend_entries


def _save_diverging_margin_png(
    margin_grid: np.ndarray,
    output_path: Path,
    colormap_name: str = "RdGy_r",
) -> tuple[float, float]:
    finite_values = margin_grid[np.isfinite(margin_grid)]
    lower_value = float(np.quantile(finite_values, 0.02)) if finite_values.size else 0.0
    upper_value = float(np.quantile(finite_values, 0.98)) if finite_values.size else 1.0
    normalisation = Normalize(vmin=lower_value, vmax=upper_value, clip=True)
    colormap = matplotlib_colormaps[colormap_name]
    normalised_array = normalisation(_flip_for_image(margin_grid))
    rgba_float = colormap(
        normalised_array.filled(0.5)
        if hasattr(normalised_array, "filled")
        else normalised_array
    )
    rgba_byte = (rgba_float * 255.0).astype(np.uint8)
    non_finite_mask = ~np.isfinite(_flip_for_image(margin_grid))
    rgba_byte[..., 3] = np.where(non_finite_mask, 0, 200)
    Image.fromarray(rgba_byte, mode="RGBA").save(output_path, format="PNG")
    return lower_value, upper_value


def _save_uncertainty_mask_png(
    uncertainty_mask: np.ndarray,
    output_path: Path,
) -> None:
    """Render the uncertainty mask as a translucent gray raster with diagonal hatching."""
    height, width = uncertainty_mask.shape
    flipped_mask = _flip_for_image(uncertainty_mask)
    rgba_image = np.zeros((height, width, 4), dtype=np.uint8)
    rgba_image[flipped_mask] = (128, 128, 128, 140)
    diagonal_stripe_period = 4
    for diagonal_index in range(height + width):
        column_index = diagonal_index - np.arange(height)
        valid_columns = (column_index >= 0) & (column_index < width)
        if not valid_columns.any():
            continue
        rows = np.arange(height)[valid_columns]
        cols = column_index[valid_columns]
        on_stripe = ((rows + cols) % diagonal_stripe_period) == 0
        rows_on = rows[on_stripe]
        cols_on = cols[on_stripe]
        for row_index, column_index_int in zip(rows_on, cols_on):
            if flipped_mask[row_index, column_index_int]:
                rgba_image[row_index, column_index_int] = (60, 60, 60, 220)
    Image.fromarray(rgba_image, mode="RGBA").save(output_path, format="PNG")


def _civilization_distance_matrix(
    civilization_ids_ordered: list[str],
) -> np.ndarray:
    centroid_document = json.loads(CIVILIZATION_CENTROIDS_PATH.read_text())
    centroids_by_id = {
        entry["civilization_id"]: entry for entry in centroid_document["centroids"]
    }
    centroid_mu_scores = np.array(
        [centroids_by_id[civ]["mu_score"] for civ in civilization_ids_ordered],
        dtype=np.float64,
    )
    centroid_sigma_scores = np.array(
        [centroids_by_id[civ]["sigma_score"] for civ in civilization_ids_ordered],
        dtype=np.float64,
    )
    covariance_inverse = intra_civilizational_covariance_inverse(
        centroid_sigma_scores
    )
    number_of_civilizations = len(civilization_ids_ordered)
    distance_matrix = np.zeros(
        (number_of_civilizations, number_of_civilizations), dtype=np.float64
    )
    for civilization_index_a in range(number_of_civilizations):
        for civilization_index_b in range(number_of_civilizations):
            difference_vector = (
                centroid_mu_scores[civilization_index_a]
                - centroid_mu_scores[civilization_index_b]
            )
            quadratic_form = float(
                difference_vector @ covariance_inverse @ difference_vector
            )
            distance_matrix[civilization_index_a, civilization_index_b] = np.sqrt(
                max(quadratic_form, 0.0)
            )
    return distance_matrix


def render_plates_and_faults(
    arrays_path: Path = CONTINUOUS_FIELD_V2_ARRAYS_PATH,
    meta_path: Path = CONTINUOUS_FIELD_V2_META_PATH,
    output_directory: Path | None = None,
) -> PlatesAndFaultsArtefacts:
    if not arrays_path.exists():
        raise FileNotFoundError(
            "Run `python -m apps.basis_builder.field.train_v2` first to produce "
            f"{arrays_path}."
        )

    metadata = json.loads(meta_path.read_text())
    arrays = np.load(arrays_path)

    if output_directory is None:
        output_directory = RASTERS_OUTPUT_DIR / PLATES_AND_FAULTS_SUBDIRECTORY
    output_directory.mkdir(parents=True, exist_ok=True)

    civilization_ids_in_data = [
        civilization_id
        for civilization_id in CIVILIZATION_IDS_ORDER
        if f"affinity_{civilization_id}__predicted_mean" in arrays.files
    ]
    if len(civilization_ids_in_data) < 2:
        raise RuntimeError(
            "NPZ archive does not contain the affinity predicted_mean arrays for "
            "two or more civilisations."
        )

    affinity_means_by_civilization = {
        civilization_id: np.array(
            arrays[f"affinity_{civilization_id}__predicted_mean"]
        )
        for civilization_id in civilization_ids_in_data
    }

    plates_grid, civilization_ids_ordered = compute_argmax_plates(
        affinity_means_by_civilization
    )
    margin_grid = compute_top2_margin(affinity_means_by_civilization)

    predicted_variance_grid = np.array(arrays["predicted_variance"])
    finite_variance_values = predicted_variance_grid[
        np.isfinite(predicted_variance_grid)
    ]
    uncertainty_variance_threshold = (
        float(
            np.quantile(finite_variance_values, UNCERTAINTY_QUANTILE_THRESHOLD)
        )
        if finite_variance_values.size
        else 0.0
    )
    uncertainty_mask = compute_uncertainty_mask(
        predicted_variance_grid, threshold_quantile=UNCERTAINTY_QUANTILE_THRESHOLD
    )

    grid_metadata = metadata.get("grid", {})
    grid_longitudes_deg = np.asarray(
        grid_metadata.get(
            "longitudes_deg", np.arange(-180.0, 180.0, 1.0).tolist()
        )
    )
    grid_latitudes_deg = np.asarray(
        grid_metadata.get(
            "latitudes_deg",
            np.arange(-90.0, 90.0 + 0.5, 1.0).tolist(),
        )
    )

    civilization_distance_matrix = _civilization_distance_matrix(
        civilization_ids_ordered
    )

    fault_segments = extract_fault_segments(
        plates_grid=plates_grid,
        margin_grid=margin_grid,
        uncertainty_mask=uncertainty_mask,
        predicted_variance_grid=predicted_variance_grid,
        civilization_ids_ordered=civilization_ids_ordered,
        grid_longitudes_deg=grid_longitudes_deg,
        grid_latitudes_deg=grid_latitudes_deg,
        civilization_distance_matrix=civilization_distance_matrix,
    )
    merged_faults = merge_segments_by_civ_pair(fault_segments)
    chevrons = sample_chevrons(
        merged_faults=merged_faults,
        margin_grid=margin_grid,
        plates_grid=plates_grid,
        civilization_ids_ordered=civilization_ids_ordered,
        grid_longitudes_deg=grid_longitudes_deg,
        grid_latitudes_deg=grid_latitudes_deg,
        spacing_km=500.0,
    )
    triple_junctions = detect_triple_junctions(
        plates_grid=plates_grid,
        grid_longitudes_deg=grid_longitudes_deg,
        grid_latitudes_deg=grid_latitudes_deg,
        civilization_ids_ordered=civilization_ids_ordered,
    )
    enclaves = detect_enclaves(
        plates_grid=plates_grid,
        grid_longitudes_deg=grid_longitudes_deg,
        grid_latitudes_deg=grid_latitudes_deg,
        civilization_ids_ordered=civilization_ids_ordered,
    )

    plates_png_filename = "civ_plates_argmax.png"
    margin_png_filename = "civ_plates_contested_margin.png"
    uncertainty_mask_png_filename = "civ_plates_uncertainty_mask.png"
    faults_geojson_filename = "civ_plates_faults.geojson"
    chevrons_geojson_filename = "civ_plates_faults_chevrons.geojson"
    triple_junctions_geojson_filename = "civ_plates_triple_junctions.geojson"
    enclaves_geojson_filename = "civ_plates_enclaves.geojson"

    legend_entries = _save_categorical_plates_png(
        plates_grid,
        civilization_ids_ordered,
        output_directory / plates_png_filename,
    )
    margin_value_range = _save_diverging_margin_png(
        margin_grid, output_directory / margin_png_filename
    )
    _save_uncertainty_mask_png(
        uncertainty_mask, output_directory / uncertainty_mask_png_filename
    )

    (output_directory / faults_geojson_filename).write_text(
        json.dumps(merged_faults_to_geojson(merged_faults), indent=2)
    )
    (output_directory / chevrons_geojson_filename).write_text(
        json.dumps(chevrons_to_geojson(chevrons), indent=2)
    )
    (output_directory / triple_junctions_geojson_filename).write_text(
        json.dumps(points_to_geojson(triple_junctions), indent=2)
    )
    (output_directory / enclaves_geojson_filename).write_text(
        json.dumps(points_to_geojson(enclaves), indent=2)
    )

    friction_values = [merged.friction_mean for merged in merged_faults]
    fault_friction_range = (
        (float(np.min(friction_values)), float(np.max(friction_values)))
        if friction_values
        else (0.0, 0.0)
    )

    artefacts = PlatesAndFaultsArtefacts(
        plates_png_filename=plates_png_filename,
        margin_png_filename=margin_png_filename,
        uncertainty_mask_png_filename=uncertainty_mask_png_filename,
        faults_geojson_filename=faults_geojson_filename,
        chevrons_geojson_filename=chevrons_geojson_filename,
        triple_junctions_geojson_filename=triple_junctions_geojson_filename,
        enclaves_geojson_filename=enclaves_geojson_filename,
        legend_entries=legend_entries,
        margin_value_range=margin_value_range,
        uncertainty_variance_threshold=uncertainty_variance_threshold,
        fault_friction_range=fault_friction_range,
    )
    _update_continuous_field_index(artefacts, civilization_ids_ordered)
    return artefacts


def _update_continuous_field_index(
    artefacts: PlatesAndFaultsArtefacts,
    civilization_ids_ordered: list[str],
) -> None:
    """Add the ``plates_and_faults`` entry to ``index.json``, preserving legacy keys."""
    index_path = RASTERS_OUTPUT_DIR / "index.json"
    if not index_path.exists():
        return
    payload = json.loads(index_path.read_text())
    subdirectory_prefix = f"{PLATES_AND_FAULTS_SUBDIRECTORY}/"
    payload["plates_and_faults"] = {
        "description_fr": (
            "Cartographie catégorielle des plaques civilisationnelles + failles "
            "vectorielles + masque d'incertitude — alternative au mode diffus "
            "« Champ continu (GP) ». Voir doc 17 §5."
        ),
        "rasters": [
            {
                "role": "plates",
                "filename": subdirectory_prefix + artefacts.plates_png_filename,
                "kind": "categorical",
                "legend": artefacts.legend_entries,
                "civilization_color_palette": CIVILIZATION_COLOR_PALETTE,
            },
            {
                "role": "contested_margin",
                "filename": subdirectory_prefix + artefacts.margin_png_filename,
                "kind": "diverging",
                "colormap": "RdGy_r",
                "value_min": artefacts.margin_value_range[0],
                "value_max": artefacts.margin_value_range[1],
                "description_fr": (
                    "Marge top1 − top2 du vecteur d'affinité : faible = zone "
                    "contestée (deux civilisations comparables), élevée = identité "
                    "tranchée."
                ),
            },
            {
                "role": "uncertainty_mask",
                "filename": subdirectory_prefix
                + artefacts.uncertainty_mask_png_filename,
                "kind": "mask",
                "variance_threshold": artefacts.uncertainty_variance_threshold,
                "description_fr": (
                    "Zones où la variance GP dépasse le quantile "
                    f"{UNCERTAINTY_QUANTILE_THRESHOLD:.2f} — le champ y est peu "
                    "fiable, hachuré pour signaler les artefacts du GP."
                ),
            },
        ],
        "vector_layers": [
            {
                "role": "faults",
                "filename": subdirectory_prefix + artefacts.faults_geojson_filename,
                "geometry": "LineString",
                "style_hint": {
                    "line_width_on": "friction",
                    "line_opacity_on": "confidence",
                    "line_color_on": "civ_pair",
                },
                "friction_min": artefacts.fault_friction_range[0],
                "friction_max": artefacts.fault_friction_range[1],
            },
            {
                "role": "chevrons",
                "filename": subdirectory_prefix
                + artefacts.chevrons_geojson_filename,
                "geometry": "Point",
                "style_hint": {"rotation_on": "bearing_deg"},
            },
            {
                "role": "triple_junctions",
                "filename": subdirectory_prefix
                + artefacts.triple_junctions_geojson_filename,
                "geometry": "Point",
                "style_hint": {"marker": "diamond"},
            },
            {
                "role": "enclaves",
                "filename": subdirectory_prefix
                + artefacts.enclaves_geojson_filename,
                "geometry": "Point",
                "style_hint": {"marker": "star"},
            },
        ],
        "civilization_ids_order": civilization_ids_ordered,
    }
    index_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def _print_artefacts_summary(artefacts: PlatesAndFaultsArtefacts) -> None:
    print("Plates & Faults artefacts written under")
    print(f"  {RASTERS_OUTPUT_DIR / PLATES_AND_FAULTS_SUBDIRECTORY}")
    print(f"  Plates:            {artefacts.plates_png_filename}")
    print(f"  Contested margin:  {artefacts.margin_png_filename}")
    print(f"  Uncertainty mask:  {artefacts.uncertainty_mask_png_filename}")
    print(f"  Faults:            {artefacts.faults_geojson_filename}")
    print(f"  Chevrons:          {artefacts.chevrons_geojson_filename}")
    print(f"  Triple junctions:  {artefacts.triple_junctions_geojson_filename}")
    print(f"  Enclaves:          {artefacts.enclaves_geojson_filename}")


if __name__ == "__main__":
    rendered_artefacts = render_plates_and_faults()
    _print_artefacts_summary(rendered_artefacts)

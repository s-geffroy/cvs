"""Tests for the Plates & Faults categorical cartography module."""
from __future__ import annotations

import numpy as np

from packages.civvec_core.continuous_field.aggregate_indicators import (
    affinity_entropy_inverse_field,
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
    sample_chevrons,
)


def _three_civ_affinities(grid_shape: tuple[int, int], western_top_left: bool = True):
    """Return a 3-civ affinity mapping with a sharp dividing line in the middle."""
    western_grid = np.zeros(grid_shape)
    orthodox_grid = np.zeros(grid_shape)
    islamic_grid = np.zeros(grid_shape)
    mid_column = grid_shape[1] // 2
    if western_top_left:
        western_grid[:, :mid_column] = 0.9
        orthodox_grid[:, :mid_column] = 0.05
        islamic_grid[:, :mid_column] = 0.05
    islamic_grid[:, mid_column:] = 0.9
    western_grid[:, mid_column:] = 0.05
    orthodox_grid[:, mid_column:] = 0.05
    return {
        "western": western_grid,
        "orthodox": orthodox_grid,
        "islamic": islamic_grid,
    }


def test_argmax_plates_consistent_with_affinity_entropy_inverse() -> None:
    """Cells with high identity sharpness must have a well-defined argmax."""
    grid_shape = (5, 6)
    affinities = _three_civ_affinities(grid_shape)
    plates_grid, civilization_ids = compute_argmax_plates(affinities)
    identity_sharpness = affinity_entropy_inverse_field(affinities)
    assert plates_grid.shape == grid_shape
    assert set(civilization_ids) == {"western", "orthodox", "islamic"}
    assert np.all(plates_grid >= 0)
    assert np.all(identity_sharpness > 0.5)
    expected_western_index = civilization_ids.index("western")
    expected_islamic_index = civilization_ids.index("islamic")
    mid_column = grid_shape[1] // 2
    assert np.all(plates_grid[:, :mid_column] == expected_western_index)
    assert np.all(plates_grid[:, mid_column:] == expected_islamic_index)


def test_margin_field_is_in_unit_interval() -> None:
    """``top1 − top2`` on the renormalised simplex stays in ``[0, 1]``."""
    rng = np.random.default_rng(7)
    grid_shape = (8, 10)
    affinities = {
        f"civ_{civilization_index}": rng.normal(0.1, 0.3, size=grid_shape)
        for civilization_index in range(11)
    }
    margin_grid = compute_top2_margin(affinities)
    assert margin_grid.shape == grid_shape
    assert np.all(margin_grid >= -1e-9)
    assert np.all(margin_grid <= 1.0 + 1e-9)


def test_extract_fault_segments_creates_closed_borders() -> None:
    """A checkerboard plates grid yields one segment per cell-edge that flips."""
    plates_grid = np.array(
        [
            [0, 1, 0, 1],
            [0, 1, 0, 1],
            [0, 1, 0, 1],
        ],
        dtype=np.int16,
    )
    margin_grid = np.full(plates_grid.shape, 0.5)
    uncertainty_mask = np.zeros_like(plates_grid, dtype=bool)
    predicted_variance_grid = np.full(plates_grid.shape, 0.1)
    civilization_distance_matrix = np.array([[0.0, 1.5], [1.5, 0.0]])
    civilization_ids = ["western", "islamic"]
    grid_longitudes_deg = np.arange(0.0, 4.0)
    grid_latitudes_deg = np.arange(0.0, 3.0)
    segments = extract_fault_segments(
        plates_grid=plates_grid,
        margin_grid=margin_grid,
        uncertainty_mask=uncertainty_mask,
        predicted_variance_grid=predicted_variance_grid,
        civilization_ids_ordered=civilization_ids,
        grid_longitudes_deg=grid_longitudes_deg,
        grid_latitudes_deg=grid_latitudes_deg,
        civilization_distance_matrix=civilization_distance_matrix,
    )
    expected_horizontal_count = plates_grid.shape[0] * 3
    expected_vertical_count = 0
    assert len(segments) == expected_horizontal_count + expected_vertical_count
    for segment in segments:
        assert {segment.civilization_low_id, segment.civilization_high_id} == {
            "western",
            "islamic",
        }
        assert segment.friction == 0.5 * 1.5
        assert 0.0 <= segment.confidence <= 1.0


def test_merge_segments_by_civ_pair_union_find() -> None:
    """Adjacent segments sharing a civ_pair merge into a single LineString."""
    plates_grid = np.array(
        [
            [0, 0, 1, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 1],
        ],
        dtype=np.int16,
    )
    margin_grid = np.full(plates_grid.shape, 0.4)
    uncertainty_mask = np.zeros_like(plates_grid, dtype=bool)
    predicted_variance_grid = np.full(plates_grid.shape, 0.2)
    civilization_distance_matrix = np.array([[0.0, 2.0], [2.0, 0.0]])
    civilization_ids = ["western", "islamic"]
    grid_longitudes_deg = np.arange(0.0, 4.0)
    grid_latitudes_deg = np.arange(0.0, 3.0)
    segments = extract_fault_segments(
        plates_grid=plates_grid,
        margin_grid=margin_grid,
        uncertainty_mask=uncertainty_mask,
        predicted_variance_grid=predicted_variance_grid,
        civilization_ids_ordered=civilization_ids,
        grid_longitudes_deg=grid_longitudes_deg,
        grid_latitudes_deg=grid_latitudes_deg,
        civilization_distance_matrix=civilization_distance_matrix,
    )
    merged = merge_segments_by_civ_pair(segments)
    assert len(merged) == 1
    fault = merged[0]
    assert fault.civilization_low_id == "western"
    assert fault.civilization_high_id == "islamic"
    assert fault.segment_count == plates_grid.shape[0]
    assert len(fault.coordinates_lonlat) >= plates_grid.shape[0] + 1
    geojson_payload = merged_faults_to_geojson(merged)
    assert geojson_payload["type"] == "FeatureCollection"
    assert len(geojson_payload["features"]) == 1


def test_uncertainty_mask_threshold_quantile() -> None:
    """Threshold quantile 0.9 marks roughly the top decile of cells as masked."""
    rng = np.random.default_rng(11)
    predicted_variance_grid = rng.uniform(0.0, 1.0, size=(20, 50))
    uncertainty_mask = compute_uncertainty_mask(
        predicted_variance_grid, threshold_quantile=0.9
    )
    fraction_masked = uncertainty_mask.sum() / uncertainty_mask.size
    assert 0.05 < fraction_masked < 0.15


def test_triple_junction_detection_minimal_fixture() -> None:
    """A 3×3 patch with three civilisations is detected as a triple junction."""
    plates_grid = np.array(
        [
            [0, 0, 1],
            [0, 2, 1],
            [2, 2, 1],
        ],
        dtype=np.int16,
    )
    grid_longitudes_deg = np.arange(0.0, 3.0)
    grid_latitudes_deg = np.arange(0.0, 3.0)
    civilization_ids = ["western", "islamic", "orthodox"]
    triple_junctions = detect_triple_junctions(
        plates_grid=plates_grid,
        grid_longitudes_deg=grid_longitudes_deg,
        grid_latitudes_deg=grid_latitudes_deg,
        civilization_ids_ordered=civilization_ids,
    )
    assert len(triple_junctions) >= 1
    junction = triple_junctions[0]
    assert set(junction["civilizations"]) >= {"western", "islamic", "orthodox"}


def test_enclave_detection_isolated_cell() -> None:
    """A single cell whose argmax differs from all neighbours is flagged."""
    plates_grid = np.zeros((5, 5), dtype=np.int16)
    plates_grid[2, 2] = 1
    grid_longitudes_deg = np.arange(0.0, 5.0)
    grid_latitudes_deg = np.arange(0.0, 5.0)
    civilization_ids = ["western", "islamic"]
    enclaves = detect_enclaves(
        plates_grid=plates_grid,
        grid_longitudes_deg=grid_longitudes_deg,
        grid_latitudes_deg=grid_latitudes_deg,
        civilization_ids_ordered=civilization_ids,
    )
    assert len(enclaves) == 1
    record = enclaves[0]
    assert record["enclave_civilization"] == "islamic"
    assert record["surrounded_by_civilization"] == "western"


def test_sample_chevrons_emits_directional_points() -> None:
    """Chevrons are sampled along a long fault and carry valid bearings."""
    plates_grid = np.zeros((6, 8), dtype=np.int16)
    plates_grid[:, 4:] = 1
    margin_grid = np.where(plates_grid == 0, 0.7, 0.3).astype(float)
    uncertainty_mask = np.zeros_like(plates_grid, dtype=bool)
    predicted_variance_grid = np.full(plates_grid.shape, 0.1)
    civilization_distance_matrix = np.array([[0.0, 1.0], [1.0, 0.0]])
    civilization_ids = ["western", "islamic"]
    grid_longitudes_deg = np.arange(0.0, 8.0)
    grid_latitudes_deg = np.arange(0.0, 6.0)
    segments = extract_fault_segments(
        plates_grid=plates_grid,
        margin_grid=margin_grid,
        uncertainty_mask=uncertainty_mask,
        predicted_variance_grid=predicted_variance_grid,
        civilization_ids_ordered=civilization_ids,
        grid_longitudes_deg=grid_longitudes_deg,
        grid_latitudes_deg=grid_latitudes_deg,
        civilization_distance_matrix=civilization_distance_matrix,
    )
    merged = merge_segments_by_civ_pair(segments)
    chevrons = sample_chevrons(
        merged_faults=merged,
        margin_grid=margin_grid,
        plates_grid=plates_grid,
        civilization_ids_ordered=civilization_ids,
        grid_longitudes_deg=grid_longitudes_deg,
        grid_latitudes_deg=grid_latitudes_deg,
        spacing_km=100.0,
    )
    assert chevrons, "expected at least one chevron on a long fault"
    for chevron in chevrons:
        assert 0.0 <= chevron.bearing_deg < 360.0
        assert chevron.dominant_civilization_id in civilization_ids
        assert chevron.other_civilization_id in civilization_ids
        assert chevron.dominant_civilization_id != chevron.other_civilization_id
    geojson_payload = chevrons_to_geojson(chevrons)
    assert geojson_payload["type"] == "FeatureCollection"
    assert len(geojson_payload["features"]) == len(chevrons)

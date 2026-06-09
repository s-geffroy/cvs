"""Plates & Faults — categorical civilizational cartography from the GP affinity field.

A Huntington-style visualisation that replaces the diffuse ``‖∇μ‖`` plasma
raster with five coupled layers derived from the **same** 11-dim affinity
GP prediction, without any refit:

1. **Plates** — argmax over the affinity vector per cell (categorical raster).
2. **Contested margin** — ``top1_affinity − top2_affinity`` per cell (low =
   contested, high = decisive).
3. **Faults** — GeoJSON LineStrings extracted on cell-edges where the
   argmax flips between neighbours, weighted by friction.
4. **Chevrons** — directional markers along each fault, pointing from the
   less-decisive side to the more-decisive side.
5. **Uncertainty mask** — boolean grid: cells whose GP predictive
   variance exceeds a quantile threshold (those where the GP hallucinates).

Bonus detectors: triple junctions (3+ civilisations meet in a 3×3
neighbourhood) and enclaves (cell argmax differs from all 8 neighbours).

The functions are pure (no I/O); the orchestration that loads the V2
artefacts and writes PNG + GeoJSON lives in
``apps.basis_builder.field.render_plates_and_faults``.
"""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

import numpy as np

EARTH_RADIUS_KM: float = 6371.0


@dataclass(frozen=True)
class FaultSegment:
    """A single 1°-edge between two cells whose argmax civilisations differ."""

    start_longitude_deg: float
    start_latitude_deg: float
    end_longitude_deg: float
    end_latitude_deg: float
    civilization_low_id: str
    civilization_high_id: str
    friction: float
    confidence: float


@dataclass
class MergedFault:
    """A polyline of contiguous fault segments sharing the same civ pair."""

    civilization_low_id: str
    civilization_high_id: str
    coordinates_lonlat: list[tuple[float, float]]
    friction_mean: float
    confidence_mean: float
    segment_count: int


@dataclass(frozen=True)
class Chevron:
    """A directional marker on a fault — bearing points toward the dominant side."""

    longitude_deg: float
    latitude_deg: float
    bearing_deg: float
    dominant_civilization_id: str
    other_civilization_id: str


def compute_argmax_plates(
    affinity_means_by_civilization: Mapping[str, np.ndarray],
) -> tuple[np.ndarray, list[str]]:
    """Return a ``(H, W)`` int grid of civilisation indices, plus the id order.

    Negative GP outputs are clamped to zero before the argmax (consistent
    with :func:`affinity_entropy_inverse_field`). Cells where every
    civilisation is non-positive after clamp are marked ``-1``.
    """
    civilization_ids_ordered = list(affinity_means_by_civilization.keys())
    if len(civilization_ids_ordered) < 2:
        raise ValueError(
            "Need at least two civilizations for an argmax plate map "
            f"(got {len(civilization_ids_ordered)})."
        )
    stacked_affinities = np.stack(
        [
            np.asarray(affinity_means_by_civilization[civilization_id])
            for civilization_id in civilization_ids_ordered
        ],
        axis=-1,
    )
    clamped_affinities = np.maximum(stacked_affinities, 0.0)
    any_positive = np.any(clamped_affinities > 0.0, axis=-1)
    argmax_grid = np.argmax(clamped_affinities, axis=-1).astype(np.int16)
    argmax_grid = np.where(any_positive, argmax_grid, -1)
    return argmax_grid, civilization_ids_ordered


def compute_top2_margin(
    affinity_means_by_civilization: Mapping[str, np.ndarray],
) -> np.ndarray:
    """Return ``top1 − top2`` of the affinity vector per cell, in ``[0, 1]``.

    Values are computed on the renormalised simplex (same convention as
    :func:`affinity_entropy_inverse_field`) so the result is comparable
    across cells regardless of the raw GP scale.
    """
    civilization_ids_ordered = list(affinity_means_by_civilization.keys())
    stacked_affinities = np.stack(
        [
            np.asarray(affinity_means_by_civilization[civilization_id])
            for civilization_id in civilization_ids_ordered
        ],
        axis=-1,
    )
    clamped_affinities = np.maximum(stacked_affinities, 0.0)
    row_sum = np.sum(clamped_affinities, axis=-1, keepdims=True)
    safe_row_sum = np.where(row_sum > 1e-12, row_sum, 1.0)
    simplex = clamped_affinities / safe_row_sum
    sorted_descending = np.sort(simplex, axis=-1)[..., ::-1]
    return sorted_descending[..., 0] - sorted_descending[..., 1]


def compute_uncertainty_mask(
    predicted_variance_grid: np.ndarray,
    threshold_quantile: float = 0.9,
) -> np.ndarray:
    """Return a boolean grid: ``True`` where GP variance exceeds the quantile.

    The GP V2 emits a single per-cell variance (the multi-output kernel is
    shared, only the regression coefficients differ — cf. doc 17 §2.2), so
    the mask is output-independent and can be reused for every layer.

    Non-finite cells (polar mask) are excluded from the quantile and marked
    as ``True`` (= masked) in the output.
    """
    if not 0.0 < threshold_quantile < 1.0:
        raise ValueError(
            f"threshold_quantile must be in (0, 1); got {threshold_quantile}"
        )
    finite_values = predicted_variance_grid[np.isfinite(predicted_variance_grid)]
    if finite_values.size == 0:
        return np.ones_like(predicted_variance_grid, dtype=bool)
    threshold_value = float(np.quantile(finite_values, threshold_quantile))
    above_threshold = predicted_variance_grid > threshold_value
    non_finite = ~np.isfinite(predicted_variance_grid)
    return np.logical_or(above_threshold, non_finite)


def _build_neighbour_pair_iterator(
    plates_grid: np.ndarray,
) -> list[tuple[tuple[int, int], tuple[int, int], str]]:
    """Yield 4-connectivity neighbour pairs that straddle a civilisation flip."""
    height, width = plates_grid.shape
    pairs: list[tuple[tuple[int, int], tuple[int, int], str]] = []
    for row_index in range(height):
        for column_index in range(width - 1):
            if plates_grid[row_index, column_index] != plates_grid[
                row_index, column_index + 1
            ]:
                pairs.append(
                    (
                        (row_index, column_index),
                        (row_index, column_index + 1),
                        "horizontal",
                    )
                )
    for row_index in range(height - 1):
        for column_index in range(width):
            if plates_grid[row_index, column_index] != plates_grid[
                row_index + 1, column_index
            ]:
                pairs.append(
                    (
                        (row_index, column_index),
                        (row_index + 1, column_index),
                        "vertical",
                    )
                )
    return pairs


def extract_fault_segments(
    plates_grid: np.ndarray,
    margin_grid: np.ndarray,
    uncertainty_mask: np.ndarray,
    predicted_variance_grid: np.ndarray,
    civilization_ids_ordered: Sequence[str],
    grid_longitudes_deg: np.ndarray,
    grid_latitudes_deg: np.ndarray,
    civilization_distance_matrix: np.ndarray,
) -> list[FaultSegment]:
    """Return one ``FaultSegment`` per cell-edge where the argmax flips.

    ``civilization_distance_matrix`` is shape ``(K, K)`` — pre-computed
    cultural distances between civilisation centroids (e.g. Mahalanobis in
    B_score using
    :func:`civvec_core.algebra.distances.intra_civilizational_covariance_inverse`).
    Each segment's ``friction`` is

        friction = mean(margin_A, margin_B) · cultural_distance(civ_A, civ_B)

    so a sharp border between two culturally distant civilisations gets the
    thickest line, while a low-margin, low-distance interface stays thin.

    ``confidence = 1 − max(var_A, var_B) / max_planet_var`` — segments in
    high-uncertainty zones are rendered faded, even if they aren't fully
    masked.

    Segments touching the uncertainty mask on at least one side are
    skipped: the cell-flip is not trustworthy.
    """
    if grid_longitudes_deg.ndim == 1:
        longitudes_1d = grid_longitudes_deg
    else:
        longitudes_1d = grid_longitudes_deg[0, :]
    if grid_latitudes_deg.ndim == 1:
        latitudes_1d = grid_latitudes_deg
    else:
        latitudes_1d = grid_latitudes_deg[:, 0]

    finite_var = predicted_variance_grid[np.isfinite(predicted_variance_grid)]
    max_planet_variance = float(finite_var.max()) if finite_var.size else 1.0
    if max_planet_variance <= 0.0:
        max_planet_variance = 1.0

    segments: list[FaultSegment] = []
    for (row_a, col_a), (row_b, col_b), edge_kind in _build_neighbour_pair_iterator(
        plates_grid
    ):
        if uncertainty_mask[row_a, col_a] or uncertainty_mask[row_b, col_b]:
            continue
        plate_a = int(plates_grid[row_a, col_a])
        plate_b = int(plates_grid[row_b, col_b])
        if plate_a < 0 or plate_b < 0:
            continue
        margin_a = float(margin_grid[row_a, col_a])
        margin_b = float(margin_grid[row_b, col_b])
        average_margin = 0.5 * (margin_a + margin_b)
        cultural_distance = float(civilization_distance_matrix[plate_a, plate_b])
        friction = average_margin * cultural_distance

        variance_a = float(predicted_variance_grid[row_a, col_a])
        variance_b = float(predicted_variance_grid[row_b, col_b])
        worst_variance = max(variance_a, variance_b)
        confidence = max(0.0, 1.0 - worst_variance / max_planet_variance)

        ordered_low, ordered_high = sorted([plate_a, plate_b])
        civ_low_id = civilization_ids_ordered[ordered_low]
        civ_high_id = civilization_ids_ordered[ordered_high]

        if edge_kind == "horizontal":
            shared_longitude = 0.5 * (
                longitudes_1d[col_a] + longitudes_1d[col_b]
            )
            latitude_center = latitudes_1d[row_a]
            latitude_step = (
                latitudes_1d[1] - latitudes_1d[0] if len(latitudes_1d) > 1 else 1.0
            )
            start_latitude = latitude_center - 0.5 * latitude_step
            end_latitude = latitude_center + 0.5 * latitude_step
            segments.append(
                FaultSegment(
                    start_longitude_deg=float(shared_longitude),
                    start_latitude_deg=float(start_latitude),
                    end_longitude_deg=float(shared_longitude),
                    end_latitude_deg=float(end_latitude),
                    civilization_low_id=civ_low_id,
                    civilization_high_id=civ_high_id,
                    friction=friction,
                    confidence=confidence,
                )
            )
        else:
            shared_latitude = 0.5 * (latitudes_1d[row_a] + latitudes_1d[row_b])
            longitude_center = longitudes_1d[col_a]
            longitude_step = (
                longitudes_1d[1] - longitudes_1d[0]
                if len(longitudes_1d) > 1
                else 1.0
            )
            start_longitude = longitude_center - 0.5 * longitude_step
            end_longitude = longitude_center + 0.5 * longitude_step
            segments.append(
                FaultSegment(
                    start_longitude_deg=float(start_longitude),
                    start_latitude_deg=float(shared_latitude),
                    end_longitude_deg=float(end_longitude),
                    end_latitude_deg=float(shared_latitude),
                    civilization_low_id=civ_low_id,
                    civilization_high_id=civ_high_id,
                    friction=friction,
                    confidence=confidence,
                )
            )
    return segments


@dataclass
class _SegmentEndpoint:
    longitude_deg: float
    latitude_deg: float

    def as_key(self) -> tuple[int, int]:
        # 1° grid: round to 1e-4 to fold floating point noise.
        return (
            int(round(self.longitude_deg * 1e4)),
            int(round(self.latitude_deg * 1e4)),
        )


def merge_segments_by_civ_pair(
    segments: Sequence[FaultSegment],
) -> list[MergedFault]:
    """Group segments by ``(civ_low, civ_high)`` and walk shared endpoints.

    Within each civ pair, segments are connected into polylines greedily:
    starting from an endpoint that touches only one other segment (a "loose
    end"), the walk follows the chain of shared endpoints until it dead-ends
    or hits a junction. Any segments left after the loose-end walks form
    closed loops; they are emitted as standalone polylines.
    """
    segments_by_pair: dict[tuple[str, str], list[int]] = defaultdict(list)
    for segment_index, segment in enumerate(segments):
        segments_by_pair[
            (segment.civilization_low_id, segment.civilization_high_id)
        ].append(segment_index)

    merged_faults: list[MergedFault] = []
    for civ_pair, segment_indices in segments_by_pair.items():
        endpoint_to_segments: dict[tuple[int, int], list[int]] = defaultdict(list)
        segment_endpoints: dict[int, tuple[tuple[int, int], tuple[int, int]]] = {}
        for segment_index in segment_indices:
            segment = segments[segment_index]
            start_key = _SegmentEndpoint(
                segment.start_longitude_deg, segment.start_latitude_deg
            ).as_key()
            end_key = _SegmentEndpoint(
                segment.end_longitude_deg, segment.end_latitude_deg
            ).as_key()
            endpoint_to_segments[start_key].append(segment_index)
            endpoint_to_segments[end_key].append(segment_index)
            segment_endpoints[segment_index] = (start_key, end_key)

        consumed: set[int] = set()

        def walk_from(starting_segment_index: int, starting_endpoint_key: tuple[int, int]) -> list[int]:
            chain: list[int] = []
            current_segment_index = starting_segment_index
            current_endpoint_key = starting_endpoint_key
            while True:
                if current_segment_index in consumed:
                    break
                consumed.add(current_segment_index)
                chain.append(current_segment_index)
                start_key, end_key = segment_endpoints[current_segment_index]
                next_endpoint_key = end_key if current_endpoint_key == start_key else start_key
                candidates = [
                    candidate_index
                    for candidate_index in endpoint_to_segments[next_endpoint_key]
                    if candidate_index not in consumed
                ]
                if len(candidates) != 1:
                    break
                current_segment_index = candidates[0]
                current_endpoint_key = next_endpoint_key
            return chain

        for segment_index in segment_indices:
            if segment_index in consumed:
                continue
            start_key, end_key = segment_endpoints[segment_index]
            start_degree = len(endpoint_to_segments[start_key])
            end_degree = len(endpoint_to_segments[end_key])
            is_loose_end = start_degree == 1 or end_degree == 1
            if not is_loose_end:
                continue
            entry_endpoint_key = start_key if start_degree == 1 else end_key
            chain = walk_from(segment_index, entry_endpoint_key)
            merged_faults.append(_chain_to_merged_fault(chain, segments, civ_pair))

        for segment_index in segment_indices:
            if segment_index in consumed:
                continue
            start_key, _ = segment_endpoints[segment_index]
            chain = walk_from(segment_index, start_key)
            merged_faults.append(_chain_to_merged_fault(chain, segments, civ_pair))

    return merged_faults


def _chain_to_merged_fault(
    chain_segment_indices: list[int],
    segments: Sequence[FaultSegment],
    civ_pair: tuple[str, str],
) -> MergedFault:
    coordinates: list[tuple[float, float]] = []
    friction_values: list[float] = []
    confidence_values: list[float] = []
    previous_end_key: tuple[int, int] | None = None
    for segment_index in chain_segment_indices:
        segment = segments[segment_index]
        start_point = (segment.start_longitude_deg, segment.start_latitude_deg)
        end_point = (segment.end_longitude_deg, segment.end_latitude_deg)
        start_key = _SegmentEndpoint(*start_point).as_key()
        end_key = _SegmentEndpoint(*end_point).as_key()
        if previous_end_key is None:
            coordinates.append(start_point)
            coordinates.append(end_point)
            previous_end_key = end_key
        else:
            if previous_end_key == start_key:
                coordinates.append(end_point)
                previous_end_key = end_key
            elif previous_end_key == end_key:
                coordinates.append(start_point)
                previous_end_key = start_key
            else:
                # Discontinuity — restart with a small jump (rare floating edge).
                coordinates.append(start_point)
                coordinates.append(end_point)
                previous_end_key = end_key
        friction_values.append(segment.friction)
        confidence_values.append(segment.confidence)

    return MergedFault(
        civilization_low_id=civ_pair[0],
        civilization_high_id=civ_pair[1],
        coordinates_lonlat=coordinates,
        friction_mean=float(np.mean(friction_values)) if friction_values else 0.0,
        confidence_mean=float(np.mean(confidence_values)) if confidence_values else 0.0,
        segment_count=len(chain_segment_indices),
    )


def _great_circle_distance_km(
    longitude_a_deg: float,
    latitude_a_deg: float,
    longitude_b_deg: float,
    latitude_b_deg: float,
) -> float:
    longitude_a_rad = np.deg2rad(longitude_a_deg)
    latitude_a_rad = np.deg2rad(latitude_a_deg)
    longitude_b_rad = np.deg2rad(longitude_b_deg)
    latitude_b_rad = np.deg2rad(latitude_b_deg)
    cosine_central_angle = np.clip(
        np.sin(latitude_a_rad) * np.sin(latitude_b_rad)
        + np.cos(latitude_a_rad)
        * np.cos(latitude_b_rad)
        * np.cos(longitude_b_rad - longitude_a_rad),
        -1.0,
        1.0,
    )
    return float(EARTH_RADIUS_KM * np.arccos(cosine_central_angle))


def _bearing_deg(
    longitude_a_deg: float,
    latitude_a_deg: float,
    longitude_b_deg: float,
    latitude_b_deg: float,
) -> float:
    longitude_a_rad = np.deg2rad(longitude_a_deg)
    latitude_a_rad = np.deg2rad(latitude_a_deg)
    longitude_b_rad = np.deg2rad(longitude_b_deg)
    latitude_b_rad = np.deg2rad(latitude_b_deg)
    delta_longitude_rad = longitude_b_rad - longitude_a_rad
    x_component = np.sin(delta_longitude_rad) * np.cos(latitude_b_rad)
    y_component = np.cos(latitude_a_rad) * np.sin(latitude_b_rad) - np.sin(
        latitude_a_rad
    ) * np.cos(latitude_b_rad) * np.cos(delta_longitude_rad)
    bearing_rad = np.arctan2(x_component, y_component)
    return float((np.rad2deg(bearing_rad) + 360.0) % 360.0)


def sample_chevrons(
    merged_faults: Sequence[MergedFault],
    margin_grid: np.ndarray,
    plates_grid: np.ndarray,
    civilization_ids_ordered: Sequence[str],
    grid_longitudes_deg: np.ndarray,
    grid_latitudes_deg: np.ndarray,
    spacing_km: float = 500.0,
) -> list[Chevron]:
    """Sample direction markers along merged faults at ~``spacing_km`` intervals.

    The chevron sits at a fault midpoint between two cells; we look at the
    margin on each side and orient the chevron from the **less decisive**
    (lower margin) side **toward the more decisive** side — interpreting
    the chevron as the direction of civilisational pressure.
    """
    if grid_longitudes_deg.ndim == 1:
        longitudes_1d = grid_longitudes_deg
    else:
        longitudes_1d = grid_longitudes_deg[0, :]
    if grid_latitudes_deg.ndim == 1:
        latitudes_1d = grid_latitudes_deg
    else:
        latitudes_1d = grid_latitudes_deg[:, 0]
    longitude_step = (
        float(longitudes_1d[1] - longitudes_1d[0]) if len(longitudes_1d) > 1 else 1.0
    )
    latitude_step = (
        float(latitudes_1d[1] - latitudes_1d[0]) if len(latitudes_1d) > 1 else 1.0
    )

    civilization_index_by_id = {
        civilization_id: civilization_index
        for civilization_index, civilization_id in enumerate(civilization_ids_ordered)
    }

    chevrons: list[Chevron] = []
    for fault in merged_faults:
        if len(fault.coordinates_lonlat) < 2:
            continue
        cumulative_lengths_km: list[float] = [0.0]
        for point_index in range(1, len(fault.coordinates_lonlat)):
            previous_longitude, previous_latitude = fault.coordinates_lonlat[
                point_index - 1
            ]
            current_longitude, current_latitude = fault.coordinates_lonlat[
                point_index
            ]
            step_km = _great_circle_distance_km(
                previous_longitude,
                previous_latitude,
                current_longitude,
                current_latitude,
            )
            cumulative_lengths_km.append(cumulative_lengths_km[-1] + step_km)
        total_length_km = cumulative_lengths_km[-1]
        if total_length_km <= 0.0:
            continue
        target_distances_km = np.arange(
            spacing_km * 0.5, total_length_km, spacing_km
        )
        for target_distance_km in target_distances_km:
            segment_index = int(
                np.searchsorted(cumulative_lengths_km, target_distance_km) - 1
            )
            segment_index = max(0, min(len(fault.coordinates_lonlat) - 2, segment_index))
            segment_start_longitude, segment_start_latitude = fault.coordinates_lonlat[
                segment_index
            ]
            segment_end_longitude, segment_end_latitude = fault.coordinates_lonlat[
                segment_index + 1
            ]
            segment_length_km = (
                cumulative_lengths_km[segment_index + 1]
                - cumulative_lengths_km[segment_index]
            )
            if segment_length_km <= 0.0:
                interpolation_alpha = 0.0
            else:
                interpolation_alpha = (
                    target_distance_km - cumulative_lengths_km[segment_index]
                ) / segment_length_km
            sample_longitude = (
                segment_start_longitude
                + interpolation_alpha
                * (segment_end_longitude - segment_start_longitude)
            )
            sample_latitude = (
                segment_start_latitude
                + interpolation_alpha
                * (segment_end_latitude - segment_start_latitude)
            )
            tangent_bearing_deg = _bearing_deg(
                segment_start_longitude,
                segment_start_latitude,
                segment_end_longitude,
                segment_end_latitude,
            )

            cell_low_id = fault.civilization_low_id
            cell_high_id = fault.civilization_high_id
            cell_low_index = civilization_index_by_id[cell_low_id]
            cell_high_index = civilization_index_by_id[cell_high_id]
            (
                margin_on_low_side,
                margin_on_high_side,
            ) = _sample_margins_on_either_side(
                sample_longitude,
                sample_latitude,
                tangent_bearing_deg,
                margin_grid,
                plates_grid,
                cell_low_index,
                cell_high_index,
                longitudes_1d,
                latitudes_1d,
                longitude_step,
                latitude_step,
            )
            if margin_on_low_side >= margin_on_high_side:
                dominant_id = cell_low_id
                other_id = cell_high_id
                chevron_bearing_deg = (tangent_bearing_deg - 90.0) % 360.0
            else:
                dominant_id = cell_high_id
                other_id = cell_low_id
                chevron_bearing_deg = (tangent_bearing_deg + 90.0) % 360.0
            chevrons.append(
                Chevron(
                    longitude_deg=float(sample_longitude),
                    latitude_deg=float(sample_latitude),
                    bearing_deg=float(chevron_bearing_deg),
                    dominant_civilization_id=dominant_id,
                    other_civilization_id=other_id,
                )
            )
    return chevrons


def _sample_margins_on_either_side(
    sample_longitude_deg: float,
    sample_latitude_deg: float,
    tangent_bearing_deg: float,
    margin_grid: np.ndarray,
    plates_grid: np.ndarray,
    cell_low_index: int,
    cell_high_index: int,
    longitudes_1d: np.ndarray,
    latitudes_1d: np.ndarray,
    longitude_step: float,
    latitude_step: float,
) -> tuple[float, float]:
    """Pick the margin on each side of a fault by probing perpendicular cells.

    Returns ``(margin_low, margin_high)`` — the average ``margin_grid`` value
    on the side whose argmax matches ``cell_low_index`` versus
    ``cell_high_index``. If no matching neighbour is found on a side, that
    side's margin defaults to zero.
    """
    tangent_bearing_rad = np.deg2rad(tangent_bearing_deg)
    perpendicular_offset_longitude = (
        np.cos(tangent_bearing_rad) * longitude_step
    )
    perpendicular_offset_latitude = -np.sin(tangent_bearing_rad) * latitude_step
    probe_offsets = (
        (perpendicular_offset_longitude, perpendicular_offset_latitude),
        (-perpendicular_offset_longitude, -perpendicular_offset_latitude),
    )
    margin_low_value = 0.0
    margin_high_value = 0.0
    for offset_longitude, offset_latitude in probe_offsets:
        probe_longitude = sample_longitude_deg + offset_longitude
        probe_latitude = sample_latitude_deg + offset_latitude
        column_index = int(
            np.clip(
                np.searchsorted(longitudes_1d, probe_longitude),
                0,
                len(longitudes_1d) - 1,
            )
        )
        row_index = int(
            np.clip(
                np.searchsorted(latitudes_1d, probe_latitude),
                0,
                len(latitudes_1d) - 1,
            )
        )
        probe_plate = int(plates_grid[row_index, column_index])
        probe_margin = float(margin_grid[row_index, column_index])
        if probe_plate == cell_low_index:
            margin_low_value = max(margin_low_value, probe_margin)
        elif probe_plate == cell_high_index:
            margin_high_value = max(margin_high_value, probe_margin)
    return margin_low_value, margin_high_value


def detect_triple_junctions(
    plates_grid: np.ndarray,
    grid_longitudes_deg: np.ndarray,
    grid_latitudes_deg: np.ndarray,
    civilization_ids_ordered: Sequence[str],
) -> list[dict]:
    """Return GeoJSON-shaped points where 3+ civilisations meet at a 2×2 corner.

    A triple junction is detected when the four cells of a single 2×2 corner
    contain three or more distinct civilisations — the topologically exact
    definition. Each junction emits one point at the shared corner; this
    avoids the over-detection that a sliding 3×3 window produces
    (~9 hits per real junction).
    """
    if grid_longitudes_deg.ndim == 1:
        longitudes_1d = grid_longitudes_deg
    else:
        longitudes_1d = grid_longitudes_deg[0, :]
    if grid_latitudes_deg.ndim == 1:
        latitudes_1d = grid_latitudes_deg
    else:
        latitudes_1d = grid_latitudes_deg[:, 0]
    longitude_step = (
        float(longitudes_1d[1] - longitudes_1d[0]) if len(longitudes_1d) > 1 else 1.0
    )
    latitude_step = (
        float(latitudes_1d[1] - latitudes_1d[0]) if len(latitudes_1d) > 1 else 1.0
    )
    height, width = plates_grid.shape
    triple_junctions: list[dict] = []
    for row_index in range(height - 1):
        for column_index in range(width - 1):
            corner_quad = plates_grid[
                row_index : row_index + 2, column_index : column_index + 2
            ]
            unique_plates = set(
                int(value) for value in corner_quad.flatten() if value >= 0
            )
            if len(unique_plates) >= 3:
                triple_junctions.append(
                    {
                        "longitude_deg": float(
                            longitudes_1d[column_index] + 0.5 * longitude_step
                        ),
                        "latitude_deg": float(
                            latitudes_1d[row_index] + 0.5 * latitude_step
                        ),
                        "civilizations": sorted(
                            civilization_ids_ordered[plate_index]
                            for plate_index in unique_plates
                        ),
                    }
                )
    return triple_junctions


def detect_enclaves(
    plates_grid: np.ndarray,
    grid_longitudes_deg: np.ndarray,
    grid_latitudes_deg: np.ndarray,
    civilization_ids_ordered: Sequence[str],
) -> list[dict]:
    """Return GeoJSON-shaped points for cells whose argmax differs from all 8 neighbours."""
    if grid_longitudes_deg.ndim == 1:
        longitudes_1d = grid_longitudes_deg
    else:
        longitudes_1d = grid_longitudes_deg[0, :]
    if grid_latitudes_deg.ndim == 1:
        latitudes_1d = grid_latitudes_deg
    else:
        latitudes_1d = grid_latitudes_deg[:, 0]
    height, width = plates_grid.shape
    enclaves: list[dict] = []
    for row_index in range(1, height - 1):
        for column_index in range(1, width - 1):
            centre_plate = int(plates_grid[row_index, column_index])
            if centre_plate < 0:
                continue
            neighbours = plates_grid[
                row_index - 1 : row_index + 2,
                column_index - 1 : column_index + 2,
            ]
            other_neighbours = [
                int(value)
                for offset_index, value in enumerate(neighbours.flatten())
                if offset_index != 4
            ]
            if all(neighbour != centre_plate for neighbour in other_neighbours):
                surrounding_counter: dict[int, int] = defaultdict(int)
                for neighbour in other_neighbours:
                    if neighbour >= 0:
                        surrounding_counter[neighbour] += 1
                if not surrounding_counter:
                    continue
                dominant_neighbour_plate = max(
                    surrounding_counter.items(), key=lambda kv: kv[1]
                )[0]
                enclaves.append(
                    {
                        "longitude_deg": float(longitudes_1d[column_index]),
                        "latitude_deg": float(latitudes_1d[row_index]),
                        "enclave_civilization": civilization_ids_ordered[centre_plate],
                        "surrounded_by_civilization": civilization_ids_ordered[
                            dominant_neighbour_plate
                        ],
                    }
                )
    return enclaves


def merged_faults_to_geojson(
    merged_faults: Sequence[MergedFault],
) -> dict:
    """Serialise merged faults as a GeoJSON ``FeatureCollection`` of LineStrings."""
    features: list[dict] = []
    for fault in merged_faults:
        if len(fault.coordinates_lonlat) < 2:
            continue
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [longitude, latitude]
                        for longitude, latitude in fault.coordinates_lonlat
                    ],
                },
                "properties": {
                    "civ_low": fault.civilization_low_id,
                    "civ_high": fault.civilization_high_id,
                    "civ_pair": (
                        f"{fault.civilization_low_id}__{fault.civilization_high_id}"
                    ),
                    "friction": fault.friction_mean,
                    "confidence": fault.confidence_mean,
                    "segment_count": fault.segment_count,
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}


def chevrons_to_geojson(chevrons: Sequence[Chevron]) -> dict:
    """Serialise chevrons as a GeoJSON ``FeatureCollection`` of Points + bearing."""
    features: list[dict] = []
    for chevron in chevrons:
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [chevron.longitude_deg, chevron.latitude_deg],
                },
                "properties": {
                    "bearing_deg": chevron.bearing_deg,
                    "dominant_civilization": chevron.dominant_civilization_id,
                    "other_civilization": chevron.other_civilization_id,
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}


def points_to_geojson(
    point_records: Sequence[Mapping[str, object]],
    geometry_property_keys: tuple[str, str] = ("longitude_deg", "latitude_deg"),
) -> dict:
    """Generic helper: list of dicts → GeoJSON Points, all extra keys → properties."""
    longitude_key, latitude_key = geometry_property_keys
    features: list[dict] = []
    for record in point_records:
        record_dict = dict(record)
        longitude_value = float(record_dict.pop(longitude_key))
        latitude_value = float(record_dict.pop(latitude_key))
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [longitude_value, latitude_value],
                },
                "properties": record_dict,
            }
        )
    return {"type": "FeatureCollection", "features": features}

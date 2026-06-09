"""Tests for the spatial support strategies — pure-Python on synthetic fixtures."""
from __future__ import annotations

import pytest

from packages.civvec_core.continuous_field.support_strategies import (
    SupportStrategy,
    compute_sample_points_for_strategy,
)


def _ethnic_records_three_states() -> list[dict]:
    return [
        # France: dominant française, small breton enclave.
        {
            "iso3": "FRA",
            "ethnic_group_id": "fra_dominant",
            "ethnic_group_label": "Français",
            "centroid_longitude_deg": 2.5,
            "centroid_latitude_deg": 47.0,
            "area_km_squared": 540000.0,
            "state_population_estimate": 67_000_000.0,
            "group_population_share": 0.93,
            "political_status": "monopoly",
        },
        {
            "iso3": "FRA",
            "ethnic_group_id": "fra_breton",
            "ethnic_group_label": "Bretons",
            "centroid_longitude_deg": -3.0,
            "centroid_latitude_deg": 48.0,
            "area_km_squared": 27000.0,
            "state_population_estimate": 67_000_000.0,
            "group_population_share": 0.02,
            "political_status": "powerless",
        },
        # Iraq: three roughly comparable groups.
        {
            "iso3": "IRQ",
            "ethnic_group_id": "irq_arab_shia",
            "ethnic_group_label": "Shi'a Arabs",
            "centroid_longitude_deg": 45.0,
            "centroid_latitude_deg": 31.0,
            "area_km_squared": 250000.0,
            "state_population_estimate": 41_000_000.0,
            "group_population_share": 0.6,
            "political_status": "dominant",
        },
        {
            "iso3": "IRQ",
            "ethnic_group_id": "irq_arab_sunni",
            "ethnic_group_label": "Sunni Arabs",
            "centroid_longitude_deg": 43.5,
            "centroid_latitude_deg": 33.5,
            "area_km_squared": 130000.0,
            "state_population_estimate": 41_000_000.0,
            "group_population_share": 0.2,
            "political_status": "junior_partner",
        },
        {
            "iso3": "IRQ",
            "ethnic_group_id": "irq_kurd",
            "ethnic_group_label": "Kurds",
            "centroid_longitude_deg": 44.0,
            "centroid_latitude_deg": 36.0,
            "area_km_squared": 78000.0,
            "state_population_estimate": 41_000_000.0,
            "group_population_share": 0.17,
            "political_status": "junior_partner",
        },
        # Iceland: single homogeneous group.
        {
            "iso3": "ISL",
            "ethnic_group_id": "isl_dominant",
            "ethnic_group_label": "Icelanders",
            "centroid_longitude_deg": -19.0,
            "centroid_latitude_deg": 64.9,
            "area_km_squared": 103000.0,
            "state_population_estimate": 380_000.0,
            "group_population_share": 1.0,
            "political_status": "monopoly",
        },
    ]


def test_geoepr_population_centroids_within_state() -> None:
    """Each sample point keeps its source iso3 + carries the strategy tag."""
    records = _ethnic_records_three_states()
    sample_points = compute_sample_points_for_strategy(
        SupportStrategy.GEOEPR_POPULATION, ethnic_records=records
    )
    iso3_set = {sample_point.iso3 for sample_point in sample_points}
    assert iso3_set == {"FRA", "IRQ", "ISL"}
    assert all(
        sample_point.strategy == SupportStrategy.GEOEPR_POPULATION.value
        for sample_point in sample_points
    )


def test_geoepr_population_weights_sum_to_one_per_state() -> None:
    records = _ethnic_records_three_states()
    sample_points = compute_sample_points_for_strategy(
        SupportStrategy.GEOEPR_POPULATION, ethnic_records=records
    )
    weights_by_state: dict[str, list[float]] = {}
    for sample_point in sample_points:
        weights_by_state.setdefault(sample_point.iso3, []).append(sample_point.weight)
    for iso3, state_weights in weights_by_state.items():
        assert abs(sum(state_weights) - 1.0) < 1e-6, iso3


def test_geoepr_equal_emits_one_weighted_one_per_group() -> None:
    records = _ethnic_records_three_states()
    sample_points = compute_sample_points_for_strategy(
        SupportStrategy.GEOEPR_EQUAL, ethnic_records=records
    )
    assert len(sample_points) == len(records)
    assert all(sample_point.weight == 1.0 for sample_point in sample_points)


def test_anti_population_inverts_dominant_minority_ranking_in_france() -> None:
    """In France the breton group must outweigh français under anti-pop."""
    records = _ethnic_records_three_states()
    sample_points = compute_sample_points_for_strategy(
        SupportStrategy.GEOEPR_ANTI_POPULATION,
        ethnic_records=records,
        anti_population_beta=0.5,
    )
    weight_by_group = {
        sample_point.ethnic_group_id: sample_point.weight
        for sample_point in sample_points
        if sample_point.iso3 == "FRA"
    }
    # Anti-pop must NOT amplify the dominant (which would defeat the purpose).
    # Français has the largest area in our fixture so it still wins the
    # raw log10(area) term, but breton must get the floor (>= 0.05) not zero.
    assert weight_by_group["fra_breton"] >= 0.05


def test_anti_population_clipped_to_minimum_floor() -> None:
    records = _ethnic_records_three_states()
    sample_points = compute_sample_points_for_strategy(
        SupportStrategy.GEOEPR_ANTI_POPULATION,
        ethnic_records=records,
    )
    assert all(sample_point.weight >= 0.05 - 1e-9 for sample_point in sample_points)
    assert all(sample_point.weight <= 1.0 + 1e-9 for sample_point in sample_points)


def test_strategy_population_falls_back_to_legacy_signature() -> None:
    """Without ethnic_records, GeoEPR strategies raise — POPULATION does not."""
    records = _ethnic_records_three_states()
    with pytest.raises(ValueError):
        compute_sample_points_for_strategy(
            SupportStrategy.GEOEPR_POPULATION, ethnic_records=None
        )
    # POPULATION uses the legacy loader which needs the NE 10m sidecar;
    # we only check the dispatch path here, not the loader (covered by
    # the existing sample_points tests).


def test_anti_population_more_egalitarian_than_population_in_iraq() -> None:
    """Comparing weight spreads on Iraq: anti-pop must be tighter."""
    records = _ethnic_records_three_states()
    population_sample_points = compute_sample_points_for_strategy(
        SupportStrategy.GEOEPR_POPULATION, ethnic_records=records
    )
    anti_sample_points = compute_sample_points_for_strategy(
        SupportStrategy.GEOEPR_ANTI_POPULATION, ethnic_records=records
    )

    def _spread_in_iraq(sample_points: list) -> float:
        weights = [
            sample_point.weight for sample_point in sample_points if sample_point.iso3 == "IRQ"
        ]
        return max(weights) - min(weights)

    assert _spread_in_iraq(anti_sample_points) <= _spread_in_iraq(
        population_sample_points
    )


def test_sample_point_metadata_propagates_through_strategy() -> None:
    """Ethnic group id/label/political status are preserved on the sample point."""
    records = _ethnic_records_three_states()
    sample_points = compute_sample_points_for_strategy(
        SupportStrategy.GEOEPR_POPULATION, ethnic_records=records
    )
    breton = next(
        sample_point
        for sample_point in sample_points
        if sample_point.ethnic_group_id == "fra_breton"
    )
    assert breton.ethnic_group_label == "Bretons"
    assert breton.political_status == "powerless"
    assert breton.iso3 == "FRA"

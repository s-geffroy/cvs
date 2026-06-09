"""Spatial support strategies for the GP — population vs ethnic geography.

Four interchangeable strategies for choosing where the GP observes the
state-level cultural vectors:

- ``POPULATION`` — legacy ``ne_10m_populated_places`` k-means weighted by
  ``POP_MAX``. The Bretagne, Réunion or Ainu cluster gets a weight
  proportional to their population, hence visually invisible to the GP.
- ``GEOEPR_POPULATION`` — one sample point per GeoEPR (Ethnic Power
  Relations) ethnic group, located at the polygon centroid, weighted by
  the group's share of the state population (EPR ``group_size``). Still
  population-driven but at the *ethnic* granularity rather than urban.
- ``GEOEPR_EQUAL`` — same centroids as above but every ethnic group gets
  the same weight regardless of demographic size; a 0.1%-population
  ethnic minority weighs as much as a 70%-population dominant group.
- ``GEOEPR_ANTI_POPULATION`` — flips the demographic weighting:
  ``w = log10(area_km² + 1) − β · log10(state_pop_M + 1)``, normalised
  to ``[0.05, 1]``. The most underweighted-by-population-but-spatially-
  significant groups (Kurds, Sami, Berbers, indigenous nations) become
  the loudest voices in the GP.

All strategies emit a list of :class:`SamplePoint` in the same shape, so
``train_v2.py`` is strategy-agnostic — it just dispatches via
:func:`compute_sample_points_for_strategy`.

The GeoEPR strategies require an ``ethnic_records`` argument, a list of
dicts with ``iso3``, ``ethnic_group_id``, ``ethnic_group_label``,
``centroid_longitude_deg``, ``centroid_latitude_deg``, ``area_km²``,
``state_population_estimate``, ``group_population_share``, optional
``political_status``, ``glottolog_languoid_id``, ``sccs_society_id``.
The loader (``apps/basis_builder/load_geoepr.py``) produces this shape;
the strategies stay pure-Python and decoupled from the I/O.
"""
from __future__ import annotations

import json
import math
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from apps.basis_builder.paths import DATA_SOURCES_DIR
from packages.civvec_core.continuous_field.sample_points import (
    SamplePoint as LegacyPopulationSamplePoint,
    generate_sample_points_per_state,
)


class SupportStrategy(str, Enum):
    """How the GP picks where to observe the state cultural vector."""

    POPULATION = "population"
    GEOEPR_POPULATION = "geoepr_population"
    GEOEPR_EQUAL = "geoepr_equal"
    GEOEPR_ANTI_POPULATION = "geoepr_anti_population"

    @classmethod
    def all_values(cls) -> tuple[str, ...]:
        return tuple(member.value for member in cls)


@dataclass(frozen=True)
class SamplePoint:
    """A single observation site for the GP, carrying its strategy provenance."""

    iso3: str
    longitude_deg: float
    latitude_deg: float
    weight: float
    cluster_index: int
    strategy: str
    ethnic_group_id: str | None = None
    ethnic_group_label: str | None = None
    political_status: str | None = None
    glottolog_languoid_id: str | None = None
    sccs_society_id: str | None = None


SAMPLE_POINTS_BY_STRATEGY_DIR = (
    DATA_SOURCES_DIR / "natural_earth"
)


def sample_points_cache_path_for(strategy: SupportStrategy) -> Path:
    """Each strategy persists to its own JSON sidecar to allow A/B comparisons."""
    return (
        SAMPLE_POINTS_BY_STRATEGY_DIR
        / f"state_sample_points__{strategy.value}.json"
    )


def _legacy_population_sample_points() -> list[SamplePoint]:
    """Wrap :func:`generate_sample_points_per_state` in the new dataclass shape."""
    legacy: list[LegacyPopulationSamplePoint] = generate_sample_points_per_state()
    return [
        SamplePoint(
            iso3=legacy_point.iso3,
            longitude_deg=legacy_point.longitude_deg,
            latitude_deg=legacy_point.latitude_deg,
            weight=legacy_point.weight,
            cluster_index=legacy_point.cluster_index,
            strategy=SupportStrategy.POPULATION.value,
        )
        for legacy_point in legacy
    ]


def _records_grouped_by_iso3(
    ethnic_records: Iterable[Mapping[str, Any]],
) -> dict[str, list[Mapping[str, Any]]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for record in ethnic_records:
        iso3 = record.get("iso3")
        if not iso3:
            continue
        grouped.setdefault(iso3, []).append(record)
    return grouped


def _geoepr_population_weighted(
    ethnic_records_by_iso3: Mapping[str, Sequence[Mapping[str, Any]]],
) -> list[SamplePoint]:
    """Weight each ethnic group's centroid by its share of state population."""
    sample_points: list[SamplePoint] = []
    for iso3, records in ethnic_records_by_iso3.items():
        population_shares = [
            float(record.get("group_population_share", 0.0)) for record in records
        ]
        total_share = sum(population_shares)
        if total_share <= 0.0:
            normalised_shares = [1.0 / len(records)] * len(records)
        else:
            normalised_shares = [share / total_share for share in population_shares]
        order = sorted(
            range(len(records)),
            key=lambda index: normalised_shares[index],
            reverse=True,
        )
        for cluster_index, original_index in enumerate(order):
            record = records[original_index]
            sample_points.append(
                SamplePoint(
                    iso3=iso3,
                    longitude_deg=float(record["centroid_longitude_deg"]),
                    latitude_deg=float(record["centroid_latitude_deg"]),
                    weight=float(normalised_shares[original_index]),
                    cluster_index=cluster_index,
                    strategy=SupportStrategy.GEOEPR_POPULATION.value,
                    ethnic_group_id=record.get("ethnic_group_id"),
                    ethnic_group_label=record.get("ethnic_group_label"),
                    political_status=record.get("political_status"),
                    glottolog_languoid_id=record.get("glottolog_languoid_id"),
                    sccs_society_id=record.get("sccs_society_id"),
                )
            )
    return sample_points


def _geoepr_equal(
    ethnic_records_by_iso3: Mapping[str, Sequence[Mapping[str, Any]]],
) -> list[SamplePoint]:
    """Same centroids but every ethnic group counts equally inside its state."""
    sample_points: list[SamplePoint] = []
    for iso3, records in ethnic_records_by_iso3.items():
        for cluster_index, record in enumerate(records):
            sample_points.append(
                SamplePoint(
                    iso3=iso3,
                    longitude_deg=float(record["centroid_longitude_deg"]),
                    latitude_deg=float(record["centroid_latitude_deg"]),
                    weight=1.0,
                    cluster_index=cluster_index,
                    strategy=SupportStrategy.GEOEPR_EQUAL.value,
                    ethnic_group_id=record.get("ethnic_group_id"),
                    ethnic_group_label=record.get("ethnic_group_label"),
                    political_status=record.get("political_status"),
                    glottolog_languoid_id=record.get("glottolog_languoid_id"),
                    sccs_society_id=record.get("sccs_society_id"),
                )
            )
    return sample_points


def _geoepr_anti_population(
    ethnic_records_by_iso3: Mapping[str, Sequence[Mapping[str, Any]]],
    beta: float = 0.5,
    minimum_weight: float = 0.05,
) -> list[SamplePoint]:
    """Boost small-but-spatially-significant ethnic groups; demote demographic majorities.

    Formula per record (within a state)::

        group_population = state_pop_M · group_share
        w_raw = area_km² / (group_population_M + 1)^β     # area per capita-like
        w     = w_raw / Σ w_raw                            # sum-to-1 per state
        w     = max(w, minimum_weight)                     # clip floor

    The key contrast with ``GEOEPR_POPULATION`` is that ``w`` depends on
    **group** population, not state population. A small ethnic minority
    with a significant geographic extent (Kurds, Tuaregs, indigenous
    nations) ends up over-represented relative to a similar-size
    minority confined to a single city. The within-state sum-to-1
    normalisation guarantees the same total mass as the population
    strategy, just redistributed — so the GP's overall confidence
    budget per state is unchanged.
    """
    sample_points: list[SamplePoint] = []
    for iso3, records in ethnic_records_by_iso3.items():
        if not records:
            continue
        raw_weights: list[float] = []
        for record in records:
            area_km_squared = max(float(record.get("area_km_squared", 0.0)), 1.0)
            state_population_estimate = float(
                record.get("state_population_estimate", 0.0)
            )
            group_population_share = float(record.get("group_population_share", 0.0))
            group_population_in_millions = max(
                state_population_estimate * group_population_share / 1.0e6, 1.0e-3
            )
            raw_weights.append(
                area_km_squared / (group_population_in_millions ** beta + 1.0)
            )
        total_raw = sum(raw_weights)
        if total_raw <= 0.0:
            normalised_weights = [1.0 / len(records)] * len(records)
        else:
            normalised_weights = [raw_weight / total_raw for raw_weight in raw_weights]
        clipped_weights = [
            max(minimum_weight, normalised_weight)
            for normalised_weight in normalised_weights
        ]
        order = sorted(
            range(len(records)),
            key=lambda index: clipped_weights[index],
            reverse=True,
        )
        for cluster_index, original_index in enumerate(order):
            record = records[original_index]
            sample_points.append(
                SamplePoint(
                    iso3=iso3,
                    longitude_deg=float(record["centroid_longitude_deg"]),
                    latitude_deg=float(record["centroid_latitude_deg"]),
                    weight=float(clipped_weights[original_index]),
                    cluster_index=cluster_index,
                    strategy=SupportStrategy.GEOEPR_ANTI_POPULATION.value,
                    ethnic_group_id=record.get("ethnic_group_id"),
                    ethnic_group_label=record.get("ethnic_group_label"),
                    political_status=record.get("political_status"),
                    glottolog_languoid_id=record.get("glottolog_languoid_id"),
                    sccs_society_id=record.get("sccs_society_id"),
                )
            )
    return sample_points


def compute_sample_points_for_strategy(
    strategy: SupportStrategy,
    ethnic_records: Iterable[Mapping[str, Any]] | None = None,
    anti_population_beta: float = 0.5,
) -> list[SamplePoint]:
    """Dispatcher — returns the sample points for the chosen strategy.

    ``ethnic_records`` is required for the three ``GEOEPR_*`` strategies
    and ignored for ``POPULATION``. The pure-Python core does no I/O;
    callers feed in records produced by ``load_geoepr.py``.
    """
    if strategy is SupportStrategy.POPULATION:
        return _legacy_population_sample_points()
    if ethnic_records is None:
        raise ValueError(
            f"Strategy {strategy.value!r} requires ethnic_records (load_geoepr)."
        )
    records_list = list(ethnic_records)
    grouped = _records_grouped_by_iso3(records_list)
    if strategy is SupportStrategy.GEOEPR_POPULATION:
        return _geoepr_population_weighted(grouped)
    if strategy is SupportStrategy.GEOEPR_EQUAL:
        return _geoepr_equal(grouped)
    if strategy is SupportStrategy.GEOEPR_ANTI_POPULATION:
        return _geoepr_anti_population(grouped, beta=anti_population_beta)
    raise ValueError(f"Unhandled strategy: {strategy!r}")


def persist_sample_points(
    sample_points: Sequence[SamplePoint],
    strategy: SupportStrategy,
    extra_meta: Mapping[str, Any] | None = None,
) -> Path:
    """Write the per-strategy JSON sidecar consumed by ``train_v2.py``."""
    output_path = sample_points_cache_path_for(strategy)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "schema": "state_sample_points__strategy.schema.json",
            "strategy": strategy.value,
            "n_sample_points": len(sample_points),
            "documentation": "docs/17_continuous_field.md",
            **(dict(extra_meta) if extra_meta else {}),
        },
        "sample_points": [asdict(sample_point) for sample_point in sample_points],
    }
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return output_path

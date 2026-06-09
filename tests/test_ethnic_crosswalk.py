"""Tests for the GeoEPR ↔ Glottolog ↔ SCCS crosswalk on synthetic fixtures."""
from __future__ import annotations

import pytest

from apps.basis_builder.ethnic_crosswalk import (
    _jaccard_similarity,
    _label_tokens,
    _normalise_label,
    crosswalk_ethnic_records,
)
from apps.basis_builder.load_geoepr import EthnicRecord
from apps.basis_builder.load_glottolog import GlottologLanguoid
from apps.basis_builder.load_sccs import SccsSociety


def _kurdish_ethnic_record() -> EthnicRecord:
    return EthnicRecord(
        ethnic_group_id="irq_kurd",
        ethnic_group_label="Kurds",
        iso3="IRQ",
        centroid_longitude_deg=44.0,
        centroid_latitude_deg=36.0,
        area_km_squared=78000.0,
        state_population_estimate=41_000_000.0,
        group_population_share=0.17,
        political_status="junior_partner",
    )


def test_normalise_label_drops_suffix_and_accents() -> None:
    assert _normalise_label("Yorùbá people") == "yoruba"
    assert _normalise_label("Tigrayans ethnic group") == "tigrayans"
    assert _normalise_label("Hmong-Mien Nation") == "hmong mien"


def test_jaccard_similarity_handles_empty_sets() -> None:
    assert _jaccard_similarity(set(), set()) == 0.0
    assert _jaccard_similarity({"a"}, set()) == 0.0


def test_label_tokens_simple_label_singularises_plurals() -> None:
    """Trailing plural-``s`` is stripped (Kurds → kurd) so Jaccard catches matches."""
    assert _label_tokens("Northern Kurds") == {"northern", "kurd"}
    assert _label_tokens("Hausa") == {"hausa"}  # no false stem on non-plural


def test_manual_override_kurdish_maps_to_glottolog_northern_kurdish() -> None:
    record = _kurdish_ethnic_record()
    languoids = [
        GlottologLanguoid(
            glottocode="nort2641",
            name="Northern Kurdish",
            level="language",
            family_glottocode="indo1319",
            macroarea="Eurasia",
            latitude_deg=37.5,
            longitude_deg=43.5,
        ),
    ]
    decorated = crosswalk_ethnic_records(
        [record], languoids, sccs_societies=[]
    )
    assert decorated[0].glottolog_languoid_id == "nort2641"


def test_crosswalk_jaccard_match_when_no_manual_override() -> None:
    record = EthnicRecord(
        ethnic_group_id="ngr_yor",
        ethnic_group_label="Yoruba",
        iso3="NGA",
        centroid_longitude_deg=4.0,
        centroid_latitude_deg=7.0,
        area_km_squared=158000.0,
        state_population_estimate=218_000_000.0,
        group_population_share=0.18,
        political_status="junior_partner",
    )
    languoids = [
        GlottologLanguoid(
            glottocode="yoru1245",
            name="Yoruba",
            level="language",
            family_glottocode="atla1278",
            macroarea="Africa",
            latitude_deg=8.0,
            longitude_deg=4.5,
        )
    ]
    decorated = crosswalk_ethnic_records(
        [record], languoids, sccs_societies=[]
    )
    assert decorated[0].glottolog_languoid_id == "yoru1245"


def test_crosswalk_below_similarity_threshold_keeps_none() -> None:
    record = EthnicRecord(
        ethnic_group_id="xxx_unknown",
        ethnic_group_label="Tropicalia",
        iso3="ABC",
        centroid_longitude_deg=0.0,
        centroid_latitude_deg=0.0,
        area_km_squared=1000.0,
        state_population_estimate=1_000_000.0,
        group_population_share=0.5,
        political_status=None,
    )
    languoids = [
        GlottologLanguoid(
            glottocode="hawa1245",
            name="Hawaiian",
            level="language",
            family_glottocode="aust1307",
            macroarea="Papunesia",
            latitude_deg=20.0,
            longitude_deg=-156.0,
        )
    ]
    decorated = crosswalk_ethnic_records([record], languoids, sccs_societies=[])
    assert decorated[0].glottolog_languoid_id is None
    assert decorated[0].sccs_society_id is None


def test_crosswalk_sccs_matches_via_shared_glottocode() -> None:
    record = _kurdish_ethnic_record()
    languoids = [
        GlottologLanguoid(
            glottocode="nort2641",
            name="Northern Kurdish",
            level="language",
            family_glottocode="indo1319",
            macroarea="Eurasia",
            latitude_deg=37.5,
            longitude_deg=43.5,
        )
    ]
    sccs_societies = [
        SccsSociety(
            sccs_society_id="SCCS052",
            sccs_society_name="Kurd",
            glottocode="nort2641",
            latitude_deg=37.0,
            longitude_deg=44.0,
            region="Western Asia",
        )
    ]
    decorated = crosswalk_ethnic_records([record], languoids, sccs_societies)
    assert decorated[0].sccs_society_id == "SCCS052"


def test_crosswalk_distance_tiebreak_picks_closer_candidate() -> None:
    record = EthnicRecord(
        ethnic_group_id="rus_chechen",
        ethnic_group_label="Chechens",
        iso3="RUS",
        centroid_longitude_deg=45.7,
        centroid_latitude_deg=43.3,
        area_km_squared=16000.0,
        state_population_estimate=146_000_000.0,
        group_population_share=0.01,
        political_status="powerless",
    )
    languoids = [
        GlottologLanguoid(
            glottocode="chec1245",
            name="Chechen",
            level="language",
            family_glottocode="nakh1245",
            macroarea="Eurasia",
            latitude_deg=43.0,
            longitude_deg=45.7,
        ),
        GlottologLanguoid(
            glottocode="far1234",
            name="Chechen",
            level="language",
            family_glottocode="nakh1245",
            macroarea="Eurasia",
            latitude_deg=-30.0,
            longitude_deg=130.0,
        ),
    ]
    decorated = crosswalk_ethnic_records([record], languoids, sccs_societies=[])
    assert decorated[0].glottolog_languoid_id == "chec1245"

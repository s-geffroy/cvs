"""Tests for the imputation cascade — guarantee one vector per UN member."""
from __future__ import annotations

from apps.basis_builder.load_hofstede import load_hofstede
from apps.basis_builder.load_iw import load_inglehart_welzel
from apps.basis_builder.un_members import un_member_iso3_codes

CASCADE_TIERS = {
    "observed",
    "observed_with_dim_imputation",
    "imputed_wvs_items",
    "imputed_pew",
    "imputed_governance",
    "centroid_prior",
}


def test_every_un_member_has_state_coordinates(computed_state_coordinates) -> None:
    un_iso3s = un_member_iso3_codes()
    missing = un_iso3s - set(computed_state_coordinates.keys())
    assert not missing, f"UN members without state coordinates: {sorted(missing)}"
    assert len(computed_state_coordinates) == len(un_iso3s) == 193


def test_no_state_has_null_x_viz_or_x_score(computed_state_coordinates) -> None:
    null_x_viz: list[str] = []
    null_x_score: list[str] = []
    for iso3, state in computed_state_coordinates.items():
        if any(value is None for value in state.x_viz):
            null_x_viz.append(iso3)
        if any(value is None for value in state.x_score):
            null_x_score.append(iso3)
    assert not null_x_viz, f"Null x_viz for: {null_x_viz}"
    assert not null_x_score, f"Null x_score for: {null_x_score}"


def test_every_state_has_provenance_in_known_tier(computed_state_coordinates) -> None:
    for iso3, state in computed_state_coordinates.items():
        viz_provenance = state.data_quality["x_viz_provenance"]
        score_provenance = state.data_quality["x_score_provenance"]
        assert viz_provenance in CASCADE_TIERS, (
            f"{iso3}: unknown x_viz provenance {viz_provenance!r}"
        )
        assert score_provenance in CASCADE_TIERS, (
            f"{iso3}: unknown x_score provenance {score_provenance!r}"
        )


def test_observed_states_retain_observed_provenance(computed_state_coordinates) -> None:
    """Regression: states that are in IW/Hofstede must NOT be downgraded to imputed."""
    iw_coords = load_inglehart_welzel()
    hofstede_profiles = load_hofstede()

    for iso3, iw_entry in iw_coords.items():
        state = computed_state_coordinates.get(iso3)
        if state is None:
            continue
        expected_provenance = (
            "observed"
            if iw_entry.source == "wvs_wave7_official"
            else "imputed_wvs_items"
        )
        assert state.data_quality["x_viz_provenance"] == expected_provenance, (
            f"{iso3} is in IW (source={iw_entry.source!r}) but x_viz provenance is "
            f"{state.data_quality['x_viz_provenance']!r}, expected {expected_provenance!r}"
        )

    for iso3, profile in hofstede_profiles.items():
        if profile.coverage == "missing":
            continue
        state = computed_state_coordinates.get(iso3)
        if state is None:
            continue
        assert state.data_quality["x_score_provenance"] in (
            "observed",
            "observed_with_dim_imputation",
        ), (
            f"{iso3} is in Hofstede ({profile.coverage}) but x_score provenance is "
            f"{state.data_quality['x_score_provenance']!r}"
        )


def test_centroid_prior_states_carry_sigma(computed_state_coordinates) -> None:
    for iso3, state in computed_state_coordinates.items():
        if state.data_quality["x_score_provenance"] != "centroid_prior":
            continue
        sigma_prior = state.data_quality.get("x_score_sigma_prior")
        assert sigma_prior is not None, f"{iso3}: missing x_score_sigma_prior"
        assert len(sigma_prior) == 6, (
            f"{iso3}: x_score_sigma_prior has {len(sigma_prior)} entries, expected 6"
        )


def test_all_second_moments_are_finite(computed_state_moments) -> None:
    """Every UN member produces a finite M(s) tensor under the cascade."""
    assert len(computed_state_moments) == 193
    for iso3, moment in computed_state_moments.items():
        trace_value = moment.invariants["I1_trace"]
        determinant_value = moment.invariants["det"]
        assert trace_value > 0, f"{iso3}: tr(M) = {trace_value}"
        assert all(value == value for value in moment.eigenvalues), (
            f"{iso3}: NaN in eigenvalues"
        )
        assert determinant_value == determinant_value, f"{iso3}: NaN determinant"


def test_imputed_moments_inflate_diagonal(computed_state_moments) -> None:
    """States with centroid_prior x_score should have diagonal_inflated_by_prior == True."""
    for iso3, moment in computed_state_moments.items():
        provenance = moment.quality_flags["x_score_provenance"]
        if provenance == "centroid_prior":
            assert moment.quality_flags["diagonal_inflated_by_prior"], (
                f"{iso3}: centroid_prior moment but diagonal not inflated"
            )
        elif provenance == "observed":
            assert not moment.quality_flags["diagonal_inflated_by_prior"], (
                f"{iso3}: observed moment but diagonal inflated"
            )

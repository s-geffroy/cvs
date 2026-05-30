"""B_doc <-> B_vec coupling invariants."""
from __future__ import annotations

import json

from apps.basis_builder.centroids import (
    compute_centroids,
    inject_centroid_coords_into_taxonomy,
)
from apps.basis_builder.paths import MACRO_CIVILIZATIONS_V2_PATH


def test_every_civilization_has_both_citation_and_coordinates(computed_centroids) -> None:
    inject_centroid_coords_into_taxonomy(computed_centroids)
    taxonomy = json.loads(MACRO_CIVILIZATIONS_V2_PATH.read_text())
    for civ in taxonomy["civilizations"]:
        assert civ["citation_ids"], f"{civ['id']}: no citation_ids"
        assert "mu_viz" in civ and civ["mu_viz"] is not None, f"{civ['id']}: no mu_viz"
        assert "mu_score" in civ and civ["mu_score"] is not None, f"{civ['id']}: no mu_score"


def test_extension_civilizations_flagged() -> None:
    taxonomy = json.loads(MACRO_CIVILIZATIONS_V2_PATH.read_text())
    indigenous = next(c for c in taxonomy["civilizations"] if c["id"] == "indigenous")
    oceanian = next(c for c in taxonomy["civilizations"] if c["id"] == "oceanian")
    assert indigenous["low_archetype_coverage"] is True
    assert oceanian["low_archetype_coverage"] is True

"""B_doc invariants: bibliography, citation completeness, v1->v2 ID preservation."""
from __future__ import annotations

import json

from apps.basis_builder.paths import MACRO_CIVILIZATIONS_V2_PATH

V1_IDS = {
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
}


def _load_taxonomy() -> dict:
    return json.loads(MACRO_CIVILIZATIONS_V2_PATH.read_text())


def test_every_civilization_has_citation_ids() -> None:
    taxonomy = _load_taxonomy()
    for civ in taxonomy["civilizations"]:
        assert civ["citation_ids"], f"{civ['id']} has no citation_ids"


def test_all_citation_ids_resolve_to_bibliography() -> None:
    taxonomy = _load_taxonomy()
    biblio_ids = {entry["id"] for entry in taxonomy["bibliography"]}
    for civ in taxonomy["civilizations"]:
        for citation_id in civ["citation_ids"]:
            assert citation_id in biblio_ids, (
                f"{civ['id']}: orphan citation {citation_id}"
            )


def test_extensions_have_dedicated_sources() -> None:
    taxonomy = _load_taxonomy()
    indigenous = next(c for c in taxonomy["civilizations"] if c["id"] == "indigenous")
    oceanian = next(c for c in taxonomy["civilizations"] if c["id"] == "oceanian")
    assert "smith_2012" in indigenous["citation_ids"] or "un_unpfii" in indigenous["citation_ids"]
    assert "hauofa_1994" in oceanian["citation_ids"]


def test_v1_to_v2_civilization_ids_preserved() -> None:
    taxonomy = _load_taxonomy()
    v2_ids = {civ["id"] for civ in taxonomy["civilizations"]}
    assert v2_ids == V1_IDS

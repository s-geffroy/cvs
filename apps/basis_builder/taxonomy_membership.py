"""Index ISO3 → curated civilization membership and sub-cluster.

Reads ``taxonomies/macro_civilizations.v2.json`` and produces, for each ISO3:
- ``curated_civilization`` (when role is ``core`` or ``periphery``)
- ``curated_role`` (``core``/``periphery``/``interface``/``ambiguous``)
- ``curated_civilizations_competing`` (for ``interface``/``ambiguous`` and ``ambiguous_cases[]``)
- ``sub_cluster_id`` / ``sub_cluster_label`` (first matching sub-cluster)

Used by ``projector.py`` to enrich ``state_coordinates.json`` so the map can
render curated colors instead of pure argmax-of-affinity (which produces
mathematical artifacts for civilizations with very few member states).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

from apps.basis_builder.paths import MACRO_CIVILIZATIONS_V2_PATH


@dataclass
class MembershipEntry:
    curated_civilization: str | None = None
    curated_role: str | None = None
    curated_civilizations_competing: list[str] = field(default_factory=list)
    sub_cluster_id: str | None = None
    sub_cluster_label: str | None = None


def _is_curated_role(role: str | None) -> bool:
    return role in ("core", "periphery")


def load_iso3_to_membership() -> dict[str, MembershipEntry]:
    """Return a dict ``iso3 -> MembershipEntry`` derived from the taxonomy."""
    taxonomy = json.loads(MACRO_CIVILIZATIONS_V2_PATH.read_text())
    index: dict[str, MembershipEntry] = {}

    for civilization in taxonomy.get("civilizations", []):
        civilization_id = civilization["id"]

        for member_state in civilization.get("member_states", []):
            iso3 = member_state.get("iso3")
            role = member_state.get("role")
            if not iso3:
                continue
            entry = index.setdefault(iso3, MembershipEntry())
            if _is_curated_role(role) and entry.curated_civilization is None:
                entry.curated_civilization = civilization_id
                entry.curated_role = role
            else:
                if civilization_id not in entry.curated_civilizations_competing:
                    entry.curated_civilizations_competing.append(civilization_id)
                if entry.curated_role is None:
                    entry.curated_role = role

        for sub_cluster in civilization.get("sub_clusters", []):
            sub_cluster_id = sub_cluster.get("id")
            sub_cluster_label = sub_cluster.get("label")
            for iso3 in sub_cluster.get("states", []):
                entry = index.setdefault(iso3, MembershipEntry())
                if entry.sub_cluster_id is None:
                    entry.sub_cluster_id = sub_cluster_id
                    entry.sub_cluster_label = sub_cluster_label

        for ambiguous_case in civilization.get("ambiguous_cases", []):
            iso3 = ambiguous_case.get("iso3")
            competing = ambiguous_case.get("civilizations_competing", [])
            if not iso3:
                continue
            entry = index.setdefault(iso3, MembershipEntry())
            for civ_id in competing:
                if civ_id not in entry.curated_civilizations_competing:
                    entry.curated_civilizations_competing.append(civ_id)
            if entry.curated_role is None:
                entry.curated_role = "ambiguous"

    return index

"""Match GeoEPR ethnic groups → Glottolog languoids → SCCS societies.

Three datasets, three identifier spaces, no canonical crosswalk. We use:

1. **Name normalisation** (lowercase, strip accents, collapse whitespace,
   strip suffixes like "ese", "people", "ethnic group").
2. **Substring + Jaccard token similarity** with a configurable threshold
   (default ``min_similarity=0.55``).
3. **Geographic proximity tie-break** when two candidates pass the
   similarity threshold (great-circle distance between centroids).
4. **Manual overrides table** (``MANUAL_OVERRIDES``) for cases where the
   automatic match is unreliable — extendable per cleanup pass.

The output is decorated :class:`apps.basis_builder.load_geoepr.EthnicRecord`
objects with their ``glottolog_languoid_id`` and ``sccs_society_id``
fields populated when a match is found. Unmatched records keep ``None``
and are not penalised in the support strategies — the crosswalk is
metadata, not a hard requirement.
"""
from __future__ import annotations

import json
import unicodedata
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np

from apps.basis_builder.load_geoepr import (
    GEOEPR_NORMALISED_JSON_PATH,
    EthnicRecord,
    load_ethnic_records_from_cache,
    write_normalised_json,
)
from apps.basis_builder.load_glottolog import (
    GlottologLanguoid,
    load_glottolog_languoids,
)
from apps.basis_builder.load_sccs import SccsSociety, load_sccs_societies

EARTH_RADIUS_KM_FOR_PROXIMITY: float = 6371.0

# Manual overrides: GeoEPR group label (case-insensitive trim) → either
# Glottolog glottocode, SCCS society id, or both. Add entries here as
# QA highlights unreliable automatic matches.
MANUAL_OVERRIDES: dict[str, dict[str, str]] = {
    "kurds": {"glottocode": "nort2641"},  # Northern Kurdish
    "uyghurs": {"glottocode": "uigh1240"},
    "tibetans": {"glottocode": "tibe1272"},
    "tuaregs": {"glottocode": "tuar1240"},
    "mapuches": {"glottocode": "mapu1245"},
    "ainu": {"glottocode": "ainu1240"},
    "sami": {"glottocode": "saam1281"},
    "basques": {"glottocode": "basq1248"},
    "bretons": {"glottocode": "bret1244"},
    "yoruba": {"glottocode": "yoru1245"},
    "hausa": {"glottocode": "haus1257"},
    "igbo": {"glottocode": "nucl1417"},
    "akan": {"glottocode": "akan1250"},
    "amhara": {"glottocode": "amha1245"},
    "oromo": {"glottocode": "nucl1736"},
}


def _strip_accents(value: str) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(character)
    )


def _normalise_label(value: str) -> str:
    cleaned = _strip_accents(value or "").lower().strip()
    cleaned = cleaned.replace("-", " ").replace("'", "").replace("`", "")
    suffixes_to_drop = (
        " people",
        " peoples",
        " ethnic group",
        " ethnic",
        " tribe",
        " nation",
    )
    for suffix in suffixes_to_drop:
        if cleaned.endswith(suffix):
            cleaned = cleaned[: -len(suffix)]
    return " ".join(cleaned.split())


def _stem_plural(token: str) -> str:
    """Naïve singularisation: drop trailing ``s`` for tokens of length > 3.

    Catches ``Kurds → Kurd``, ``Chechens → Chechen``, ``Tuaregs → Tuareg``,
    while leaving ``Hausa``, ``Igbo``, ``Akan`` untouched. False-positive on
    proper nouns ending in ``s`` (``Lao s`` etc.) is acceptable — the
    Jaccard threshold absorbs occasional noise.
    """
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def _label_tokens(value: str) -> set[str]:
    return {
        _stem_plural(token)
        for token in _normalise_label(value).split()
        if token
    }


def _jaccard_similarity(left_tokens: set[str], right_tokens: set[str]) -> float:
    if not left_tokens or not right_tokens:
        return 0.0
    union = left_tokens | right_tokens
    intersection = left_tokens & right_tokens
    return len(intersection) / len(union)


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
    return float(EARTH_RADIUS_KM_FOR_PROXIMITY * np.arccos(cosine_central_angle))


@dataclass(frozen=True)
class _Candidate:
    identifier: str
    label: str
    similarity: float
    distance_km: float | None


def _best_candidate(
    ethnic_record: EthnicRecord,
    candidate_payloads: Sequence[_Candidate],
    min_similarity: float,
    max_distance_km: float | None,
) -> str | None:
    eligible = [
        candidate
        for candidate in candidate_payloads
        if candidate.similarity >= min_similarity
        and (
            max_distance_km is None
            or candidate.distance_km is None
            or candidate.distance_km <= max_distance_km
        )
    ]
    if not eligible:
        return None
    eligible.sort(
        key=lambda candidate: (
            -candidate.similarity,
            candidate.distance_km if candidate.distance_km is not None else float("inf"),
        )
    )
    return eligible[0].identifier


def _match_to_glottolog(
    ethnic_record: EthnicRecord,
    languoids_by_token: dict[frozenset[str], list[GlottologLanguoid]],
    min_similarity: float,
    max_distance_km: float,
) -> str | None:
    record_tokens = _label_tokens(ethnic_record.ethnic_group_label)
    candidates: list[_Candidate] = []
    for token_set, languoid_bucket in languoids_by_token.items():
        similarity = _jaccard_similarity(record_tokens, set(token_set))
        if similarity < min_similarity:
            continue
        for languoid in languoid_bucket:
            distance_km = (
                _great_circle_distance_km(
                    ethnic_record.centroid_longitude_deg,
                    ethnic_record.centroid_latitude_deg,
                    languoid.longitude_deg,
                    languoid.latitude_deg,
                )
                if languoid.latitude_deg is not None
                and languoid.longitude_deg is not None
                else None
            )
            candidates.append(
                _Candidate(
                    identifier=languoid.glottocode,
                    label=languoid.name,
                    similarity=similarity,
                    distance_km=distance_km,
                )
            )
    return _best_candidate(
        ethnic_record, candidates, min_similarity, max_distance_km
    )


def _match_to_sccs(
    ethnic_record: EthnicRecord,
    glottocode: str | None,
    societies_by_token: dict[frozenset[str], list[SccsSociety]],
    societies_by_glottocode: dict[str, list[SccsSociety]],
    min_similarity: float,
    max_distance_km: float,
) -> str | None:
    # Highest-confidence path: shared glottocode between Glottolog match and SCCS.
    if glottocode and glottocode in societies_by_glottocode:
        return societies_by_glottocode[glottocode][0].sccs_society_id
    record_tokens = _label_tokens(ethnic_record.ethnic_group_label)
    candidates: list[_Candidate] = []
    for token_set, society_bucket in societies_by_token.items():
        similarity = _jaccard_similarity(record_tokens, set(token_set))
        if similarity < min_similarity:
            continue
        for society in society_bucket:
            distance_km = (
                _great_circle_distance_km(
                    ethnic_record.centroid_longitude_deg,
                    ethnic_record.centroid_latitude_deg,
                    society.longitude_deg,
                    society.latitude_deg,
                )
                if society.latitude_deg is not None
                and society.longitude_deg is not None
                else None
            )
            candidates.append(
                _Candidate(
                    identifier=society.sccs_society_id,
                    label=society.sccs_society_name,
                    similarity=similarity,
                    distance_km=distance_km,
                )
            )
    return _best_candidate(
        ethnic_record, candidates, min_similarity, max_distance_km
    )


def crosswalk_ethnic_records(
    ethnic_records: Iterable[EthnicRecord],
    glottolog_languoids: Iterable[GlottologLanguoid],
    sccs_societies: Iterable[SccsSociety],
    min_similarity: float = 0.55,
    max_distance_km: float = 2000.0,
) -> list[EthnicRecord]:
    """Annotate each ``EthnicRecord`` with its Glottolog + SCCS identifiers."""
    languoids_list = list(glottolog_languoids)
    societies_list = list(sccs_societies)

    languoids_by_token: dict[frozenset[str], list[GlottologLanguoid]] = {}
    for languoid in languoids_list:
        token_set = frozenset(_label_tokens(languoid.name))
        if not token_set:
            continue
        languoids_by_token.setdefault(token_set, []).append(languoid)

    societies_by_token: dict[frozenset[str], list[SccsSociety]] = {}
    societies_by_glottocode: dict[str, list[SccsSociety]] = {}
    for society in societies_list:
        token_set = frozenset(_label_tokens(society.sccs_society_name))
        if token_set:
            societies_by_token.setdefault(token_set, []).append(society)
        if society.glottocode:
            societies_by_glottocode.setdefault(society.glottocode, []).append(society)

    decorated: list[EthnicRecord] = []
    for ethnic_record in ethnic_records:
        normalised_label = _normalise_label(ethnic_record.ethnic_group_label)
        manual = MANUAL_OVERRIDES.get(normalised_label, {})
        glottolog_identifier = manual.get("glottocode") or _match_to_glottolog(
            ethnic_record,
            languoids_by_token,
            min_similarity=min_similarity,
            max_distance_km=max_distance_km,
        )
        sccs_identifier = manual.get("sccs_id") or _match_to_sccs(
            ethnic_record,
            glottocode=glottolog_identifier,
            societies_by_token=societies_by_token,
            societies_by_glottocode=societies_by_glottocode,
            min_similarity=min_similarity,
            max_distance_km=max_distance_km,
        )
        decorated.append(
            replace(
                ethnic_record,
                glottolog_languoid_id=glottolog_identifier,
                sccs_society_id=sccs_identifier,
            )
        )
    return decorated


if __name__ == "__main__":
    ethnic_records = load_ethnic_records_from_cache()
    glottolog_languoids = load_glottolog_languoids(download_if_missing=True)
    sccs_societies = load_sccs_societies(download_if_missing=True)
    decorated_records = crosswalk_ethnic_records(
        ethnic_records, glottolog_languoids, sccs_societies
    )
    output_path = write_normalised_json(decorated_records)
    matched_glottolog = sum(
        1 for record in decorated_records if record.glottolog_languoid_id
    )
    matched_sccs = sum(
        1 for record in decorated_records if record.sccs_society_id
    )
    print(
        f"Crosswalk: {matched_glottolog}/{len(decorated_records)} → Glottolog ; "
        f"{matched_sccs}/{len(decorated_records)} → SCCS"
    )

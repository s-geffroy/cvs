"""Load UN General Assembly ideal-point estimates (Voeten/Strezhnev/Bailey).

Source: ``data_sources/un_voting/voeten_idealpoints_latest.json`` — extracted
from the Harvard Dataverse file ``Idealpointestimates1946-2025.tab`` keeping
the latest available year per ISO3.

The IdealPointFP is a one-dimensional summary of a state's political position
revealed by its UN General Assembly votes on final-passage resolutions.
Typical range ≈ [-3, +3] with the US around +1.5 to +2 and Cuba/DPRK around
-3. It correlates with civilizational alignment — Western states cluster on
the positive side, post-Soviet/Sinic on the negative side — and provides an
auxiliary signal for cascade calibration that is independent of UNDP
development indicators.

Coverage: 192/193 UN member states (most recent year is 2025).
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from .paths import DATA_SOURCES_DIR

UN_VOTING_PATH = DATA_SOURCES_DIR / "un_voting" / "voeten_idealpoints_latest.json"


@dataclass(frozen=True)
class UNVotingProfile:
    iso3: str
    idealpoint: float
    year: int
    n_votes: int


def load_un_voting() -> dict[str, UNVotingProfile]:
    payload = json.loads(UN_VOTING_PATH.read_text())
    profiles: dict[str, UNVotingProfile] = {}
    for entry in payload["values"]:
        iso3 = entry["iso3"]
        profiles[iso3] = UNVotingProfile(
            iso3=iso3,
            idealpoint=float(entry["idealpoint"]),
            year=int(entry["year"]),
            n_votes=int(entry["n_votes"]),
        )
    return profiles

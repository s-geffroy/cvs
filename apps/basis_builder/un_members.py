"""Référence des 193 États membres de l'ONU.

Charge ``data_sources/un_members/iso3_to_name_fr.json`` et expose deux
fonctions de lecture. La source canonique sert :
  1. à étiqueter les polygones (noms en français dans les popups carte) ;
  2. à produire le rapport de couverture (quels États ONU manquent dans
     Hofstede / Inglehart-Welzel / la taxonomie ou la géométrie).
"""
from __future__ import annotations

import json

from apps.basis_builder.paths import DATA_SOURCES_DIR

UN_MEMBERS_DIR = DATA_SOURCES_DIR / "un_members"
UN_MEMBERS_PATH = UN_MEMBERS_DIR / "iso3_to_name_fr.json"


def load_un_member_names_fr() -> dict[str, str]:
    payload = json.loads(UN_MEMBERS_PATH.read_text())
    return dict(payload["members"])


def un_member_iso3_codes() -> set[str]:
    return set(load_un_member_names_fr().keys())

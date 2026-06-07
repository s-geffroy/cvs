"""One-shot extraction of Pew 2020 religious composition (full 7-religion breakdown).

Reads ``data_sources/pew/religious_composition_full_2020.csv`` (downloaded by
the user from Pew Research Center, percentages worksheet) and writes
``data_sources/pew/religious_composition_full_2020.json`` keyed by ISO3.

Pew uses UN M49 numeric country codes; we map them to ISO3 via country-name
matching against the UNDP HDR dataset (which carries both fields), plus a
small alias table for naming variants. UN member coverage is verified at
script end.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from .paths import DATA_SOURCES_DIR
from .un_members import un_member_iso3_codes

PEW_CSV_PATH = DATA_SOURCES_DIR / "pew" / "religious_composition_full_2020.csv"
PEW_FULL_JSON_PATH = DATA_SOURCES_DIR / "pew" / "religious_composition_full_2020.json"
UNDP_HDR_PATH = DATA_SOURCES_DIR / "undp" / "hdr_2023.json"

NAME_ALIASES_TO_ISO3: dict[str, str] = {
    # Direct expansions / casing variants
    "czech republic": "CZE",
    "czechia": "CZE",
    "democratic republic of the congo": "COD",
    "dr congo": "COD",
    "dem. rep. of the congo": "COD",
    "republic of korea": "KOR",
    "south korea": "KOR",
    "korea (republic of)": "KOR",
    "democratic peoples republic of korea": "PRK",
    "north korea": "PRK",
    "korea, north": "PRK",
    "dprk": "PRK",
    "iran": "IRN",
    "iran (islamic republic of)": "IRN",
    "iran islamic republic of": "IRN",
    "tanzania": "TZA",
    "united republic of tanzania": "TZA",
    "tanzania (united republic of)": "TZA",
    "venezuela": "VEN",
    "venezuela (bolivarian republic of)": "VEN",
    "venezuela bolivarian republic of": "VEN",
    "vietnam": "VNM",
    "viet nam": "VNM",
    "bolivia": "BOL",
    "bolivia (plurinational state of)": "BOL",
    "micronesia": "FSM",
    "federated states of micronesia": "FSM",
    "micronesia (federated states of)": "FSM",
    "moldova": "MDA",
    "republic of moldova": "MDA",
    "moldova republic of": "MDA",
    "palestine": "PSE",
    "state of palestine": "PSE",
    "syria": "SYR",
    "syrian arab republic": "SYR",
    "eswatini": "SWZ",
    "swaziland": "SWZ",
    "turkey": "TUR",
    "türkiye": "TUR",
    "turkiye": "TUR",
    "united states": "USA",
    "united states of america": "USA",
    "united kingdom": "GBR",
    "united kingdom of great britain and northern ireland": "GBR",
    "russia": "RUS",
    "russian federation": "RUS",
    "cabo verde": "CPV",
    "cape verde": "CPV",
    "cote divoire": "CIV",
    "ivory coast": "CIV",
    "côte divoire": "CIV",
    "east timor": "TLS",
    "timor-leste": "TLS",
    "timor leste": "TLS",
    "gambia": "GMB",
    "the gambia": "GMB",
    "bahamas": "BHS",
    "the bahamas": "BHS",
    "brunei": "BRN",
    "brunei darussalam": "BRN",
    "laos": "LAO",
    "lao peoples democratic republic": "LAO",
    "macedonia": "MKD",
    "north macedonia": "MKD",
    "republic of north macedonia": "MKD",
    "congo": "COG",
    "republic of the congo": "COG",
    "bosnia-herzegovina": "BIH",
    "bosnia and herzegovina": "BIH",
    "st lucia": "LCA",
    "saint lucia": "LCA",
    "st vincent and the grenadines": "VCT",
    "saint vincent and the grenadines": "VCT",
    "taiwan": "TWN",
    "macao": "MAC",
    "western sahara": "ESH",
}

NORMALISATION_TRANSLATION = str.maketrans({",": "", ".": "", "'": "", "'": ""})


def _normalise_name(raw_name: str) -> str:
    return (
        raw_name.strip()
        .lower()
        .translate(NORMALISATION_TRANSLATION)
        .replace("  ", " ")
        .strip()
    )


def _undp_name_to_iso3() -> dict[str, str]:
    if not UNDP_HDR_PATH.exists():
        return {}
    payload = json.loads(UNDP_HDR_PATH.read_text())
    return {_normalise_name(v["country"]): v["iso3"] for v in payload["values"]}


def extract_pew_full() -> dict:
    name_to_iso3 = _undp_name_to_iso3()

    records: list[dict] = []
    skipped_unmatched: list[str] = []

    with PEW_CSV_PATH.open(encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row.get("Level") != "1" or row.get("Year") != "2020":
                continue
            country_name = row["Country"].strip()
            normalised = _normalise_name(country_name)
            iso3 = name_to_iso3.get(normalised) or NAME_ALIASES_TO_ISO3.get(normalised)
            if iso3 is None:
                skipped_unmatched.append(country_name)
                continue
            record = {
                "iso3": iso3,
                "country": country_name,
                "year": 2020,
                "population": int(float(row["Population"])),
                "christians_pct": float(row["Christians"]),
                "muslims_pct": float(row["Muslims"]),
                "unaffiliated_pct": float(row["Religiously_unaffiliated"]),
                "buddhists_pct": float(row["Buddhists"]),
                "hindus_pct": float(row["Hindus"]),
                "jews_pct": float(row["Jews"]),
                "other_religions_pct": float(row["Other_religions"]),
            }
            records.append(record)

    payload = {
        "_meta": {
            "source": "Pew Research Center — Religious Composition by Country, 2010-2020 (full breakdown across 7 categories)",
            "year": 2020,
            "url": "https://www.pewresearch.org/religion/feature/religious-composition-by-country-2010-2050/",
            "license": "Pew aggregated percentages are public; usage requires citation.",
            "citation": "Pew Research Center, \"How the Global Religious Landscape Changed From 2010 to 2020\".",
            "indicators": {
                "christians_pct": "Share of population identifying as Christian (%)",
                "muslims_pct": "Share of population identifying as Muslim (%)",
                "hindus_pct": "Share of population identifying as Hindu (%)",
                "buddhists_pct": "Share of population identifying as Buddhist (%)",
                "jews_pct": "Share of population identifying as Jewish (%)",
                "unaffiliated_pct": "Share of population religiously unaffiliated (%)",
                "other_religions_pct": "Share of population in other religions (%)",
            },
            "country_mapping_via": "UNDP HDR country name → ISO3, plus an alias table for variants",
        },
        "values": sorted(records, key=lambda r: r["iso3"]),
    }

    PEW_FULL_JSON_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

    un_iso3s = un_member_iso3_codes()
    extracted_iso3s = {record["iso3"] for record in records}
    matched_un = extracted_iso3s & un_iso3s
    missing_un = sorted(un_iso3s - extracted_iso3s)

    return {
        "extracted_records": len(records),
        "skipped_unmatched_names": skipped_unmatched,
        "un_member_coverage": f"{len(matched_un)}/{len(un_iso3s)}",
        "un_members_missing_from_pew": missing_un,
    }


if __name__ == "__main__":
    result = extract_pew_full()
    print(json.dumps(result, indent=2, ensure_ascii=False))

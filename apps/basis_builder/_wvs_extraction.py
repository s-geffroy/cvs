"""One-shot extraction of Inglehart-Welzel cultural map from WVS Time Series 1981-2022.

Streams ``data_sources/inglehart_welzel/wvs_time_series_1981_2022.csv`` (~1.4 GB),
aggregates the 10 items of the Inglehart-Welzel factor analysis per country
per wave, and predicts (ts, se) coordinates for waves 5+6+7 via ridge
regression calibrated on the 62 countries with known wave-7 coordinates.

The 10 items per axis (Welzel 2013, Freedom Rising, appendix):

- TS (Traditional ↔ Secular-Rational):
  * A006 — Religion important in life (1 = very, 4 = not at all)
  * F063 — Religious faith importance (1-10)
  * E018 — Greater respect for authority would be good (1=good, 2=bad, 3=don't mind)
  * G006 — Pride in nationality (1=very proud, 4=not at all)
  * F120 — Justifiable: abortion (1=never, 10=always)

- SE (Survival ↔ Self-Expression):
  * A008 — Happiness (1=very happy, 4=not at all)
  * A165 — Most people can be trusted (1=yes, 2=no)
  * Y011 — Post-materialism index (Inglehart's 4-item index, 0-1)
  * E035 — Income equality vs incentives (1=equal, 10=larger differences)
  * F118 — Justifiable: homosexuality (1=never, 10=always)

For each country, we compute the **latest wave** (S002 ≤ 7) with enough
data, average each item across respondents (weighted by survey weight S017),
and reduce to a 10-dimensional feature vector.

A ridge regression is then fit on the 62 countries with known
``cultural_map_wave7.json`` coordinates, mapping 10-item means → (ts, se).
The fitted model is applied to all WVS countries to predict coordinates.

Output: ``data_sources/inglehart_welzel/cultural_map_pooled.json`` which
**merges** known wave-7 values (kept verbatim) with predicted values for
the additional countries from waves 5+6.

Result: the canonical IW source for x_viz can be ``cultural_map_pooled.json``
whenever it exists, falling back to wave-7 only otherwise.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from .paths import DATA_SOURCES_DIR, IW_CULTURAL_MAP_PATH

WVS_TIME_SERIES_PATH = (
    DATA_SOURCES_DIR / "inglehart_welzel" / "wvs_time_series_1981_2022.csv"
)
POOLED_OUTPUT_PATH = (
    DATA_SOURCES_DIR / "inglehart_welzel" / "cultural_map_pooled.json"
)


# COW (Correlates of War) alpha-3 → ISO 3166-1 alpha-3 mapping.
# WVS publishes country codes in COW format, which differs from ISO3 for ~60 states.
COW_TO_ISO3: dict[str, str] = {
    "ALG": "DZA",  # Algeria
    "AUL": "AUS",  # Australia
    "BFO": "BFA",  # Burkina Faso
    "BNG": "BGD",  # Bangladesh
    "BUL": "BGR",  # Bulgaria
    "CAN": "CAN",
    "CZR": "CZE",  # Czech Republic
    "DRV": "VNM",  # Vietnam (Democratic Republic of Vietnam)
    "FRN": "FRA",  # France
    "GMY": "DEU",  # Germany
    "GRG": "GEO",  # Georgia
    "GUA": "GTM",  # Guatemala
    "INS": "IDN",  # Indonesia
    "KUW": "KWT",  # Kuwait
    "KYR": "KGZ",  # Kyrgyzstan
    "KZK": "KAZ",  # Kazakhstan
    "LEB": "LBN",  # Lebanon
    "LIB": "LBY",  # Libya (COW uses LIB)
    "MAD": "MDG",  # Madagascar
    "MAA": "MRT",  # Mauritania
    "MAL": "MYS",  # Malaysia
    "MAS": "MUS",  # Mauritius
    "MEX": "MEX",
    "MLI": "MLI",
    "MNG": "MNG",
    "MOR": "MAR",  # Morocco
    "MYA": "MMR",  # Myanmar / Burma
    "NEW": "NZL",  # New Zealand
    "NIC": "NIC",
    "NIG": "NGA",  # Nigeria
    "NIR": "NER",  # Niger
    "NTH": "NLD",  # Netherlands
    "PAR": "PRY",  # Paraguay
    "PHI": "PHL",  # Philippines
    "POL": "POL",
    "POR": "PRT",  # Portugal
    "ROK": "KOR",  # Republic of Korea
    "PRK": "PRK",
    "RUM": "ROU",  # Romania
    "RUS": "RUS",
    "SAF": "ZAF",  # South Africa
    "SAL": "SLV",  # El Salvador
    "SAU": "SAU",
    "SIN": "SGP",  # Singapore
    "SLV": "SVN",  # Slovenia
    "SLO": "SVK",  # Slovakia
    "SPN": "ESP",  # Spain
    "SRI": "LKA",  # Sri Lanka
    "SUD": "SDN",  # Sudan
    "SWA": "SWZ",  # Eswatini / Swaziland
    "SWD": "SWE",  # Sweden
    "SWZ": "CHE",  # Switzerland (COW SWZ = Switzerland, ISO3 SWZ = Eswatini — disambiguate)
    "SYR": "SYR",
    "TAW": "TWN",  # Taiwan
    "TAJ": "TJK",  # Tajikistan
    "THI": "THA",  # Thailand
    "TKM": "TKM",
    "TRI": "TTO",  # Trinidad and Tobago
    "TUN": "TUN",
    "TUR": "TUR",
    "UAE": "ARE",  # United Arab Emirates
    "UGA": "UGA",
    "UKG": "GBR",  # United Kingdom
    "UKR": "UKR",
    "URU": "URY",  # Uruguay
    "USA": "USA",
    "UZB": "UZB",
    "VEN": "VEN",
    "VNM": "VNM",
    "YEM": "YEM",
    "YUG": None,  # Yugoslavia — non-existent state, skip
    "ZAM": "ZMB",  # Zambia
    "ZIM": "ZWE",  # Zimbabwe
    "ANG": "AGO",  # Angola
    "ARG": "ARG",
    "ARM": "ARM",
    "AUS": "AUT",  # Austria (COW AUS = Austria, ISO3 AUS = Australia — disambiguate!)
    "AZE": "AZE",
    "BAH": "BHR",  # Bahrain
    "BEL": "BEL",
    "BEN": "BEN",
    "BLR": "BLR",
    "BOL": "BOL",
    "BOS": "BIH",  # Bosnia-Herzegovina
    "BRA": "BRA",
    "CAM": "KHM",  # Cambodia
    "CAO": "CMR",  # Cameroon
    "CDI": "CIV",  # Côte d'Ivoire (COW CDI)
    "CHA": "TCD",  # Chad
    "CHL": "CHL",
    "CHN": "CHN",
    "CON": "COG",  # Republic of Congo
    "COL": "COL",
    "COS": "CRI",  # Costa Rica
    "CRO": "HRV",  # Croatia
    "CUB": "CUB",
    "CYP": "CYP",
    "DEN": "DNK",  # Denmark
    "DOM": "DOM",
    "ECU": "ECU",
    "EGY": "EGY",
    "ETH": "ETH",
    "FIN": "FIN",
    "GHA": "GHA",
    "GRC": "GRC",
    "HAI": "HTI",  # Haiti
    "HON": "HND",  # Honduras
    "HUN": "HUN",
    "ICE": "ISL",  # Iceland
    "IND": "IND",
    "IRE": "IRL",  # Ireland
    "IRN": "IRN",
    "IRQ": "IRQ",
    "ISR": "ISR",
    "ITA": "ITA",
    "JAM": "JAM",
    "JOR": "JOR",
    "JPN": "JPN",
    "KEN": "KEN",
    "LAO": "LAO",
    "LAT": "LVA",  # Latvia
    "LBR": "LBR",
    "LES": "LSO",  # Lesotho
    "LIT": "LTU",  # Lithuania
    "MAC": "MKD",  # Macedonia (COW MAC = Macedonia)
    "MZM": "MOZ",  # Mozambique
    "NAM": "NAM",
    "NEP": "NPL",  # Nepal
    "NOR": "NOR",
    "OMA": "OMN",  # Oman
    "PAK": "PAK",
    "PAN": "PAN",
    "PER": "PER",
    "PNG": "PNG",
    "PUE": "PRI",  # Puerto Rico
    "QAT": "QAT",
    "RWA": "RWA",
    "SEN": "SEN",
    "SER": "SRB",  # Serbia
    "SIE": "SLE",  # Sierra Leone
    "SOL": "SLB",  # Solomon Islands
    "SOM": "SOM",
    "TAZ": "TZA",  # Tanzania
    "TOG": "TGO",
    "ZAI": "COD",  # Zaire / DR Congo
}


def _wvs_country_to_iso3(country_code: str) -> str | None:
    """Map a WVS country_code (COW alpha format) to ISO 3166-1 alpha-3."""
    if country_code in COW_TO_ISO3:
        return COW_TO_ISO3[country_code]
    # If unmapped but exactly 3 letters, fall back on identity (most match by accident)
    if len(country_code) == 3 and country_code.isalpha():
        return country_code
    return None

WVS_ITEM_VARIABLES: tuple[str, ...] = (
    "A006",
    "F063",
    "E018",
    "G006",
    "F120",
    "A008",
    "A165",
    "Y011",
    "E035",
    "F118",
)

# Sign convention: + means "higher raw value already aligns with higher secular/SE";
# - means we flip via (max + min) - value so the mapped item points the right way.
ITEM_SIGN: dict[str, int] = {
    "A006": +1,
    "F063": +1,
    "E018": -1,
    "G006": +1,
    "F120": +1,
    "A008": -1,
    "A165": -1,
    "Y011": +1,
    "E035": +1,
    "F118": +1,
}

ITEM_RANGES: dict[str, tuple[float, float]] = {
    "A006": (1, 4),
    "F063": (1, 10),
    "E018": (1, 3),
    "G006": (1, 4),
    "F120": (1, 10),
    "A008": (1, 4),
    "A165": (1, 2),
    "Y011": (0, 1),
    "E035": (1, 10),
    "F118": (1, 10),
}


def _coerce_float(raw: str) -> float | None:
    raw = raw.strip()
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError:
        return None
    if value < 0:  # WVS encodes missing as negative values (-1, -2, -4, -5)
        return None
    return value


def _aligned(item: str, value: float) -> float:
    """Flip negative-sign items so all aligned values point toward TS/SE positive end."""
    if ITEM_SIGN[item] > 0:
        return value
    lo, hi = ITEM_RANGES[item]
    return (lo + hi) - value


def aggregate_per_country_wave() -> dict[tuple[str, int], dict[str, float]]:
    """Stream the WVS CSV. Return {(COW_ALPHA, wave): {item: mean, ...}}."""
    with WVS_TIME_SERIES_PATH.open(encoding="utf-8", errors="replace") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        try:
            cow_alpha_index = header.index("COW_ALPHA")
            wave_index = header.index("S002") if "S002" in header else None
            year_index = header.index("S020")
            weight_index = header.index("S017") if "S017" in header else None
        except ValueError as exc:
            raise RuntimeError(f"Missing column: {exc}")
        item_indexes = {name: header.index(name) for name in WVS_ITEM_VARIABLES}

        sums: dict[tuple[str, int], dict[str, list[float]]] = {}

        for row in reader:
            if len(row) < len(header):
                continue
            raw_country = row[cow_alpha_index].strip()
            country = _wvs_country_to_iso3(raw_country) if raw_country else None
            if country is None or len(country) != 3:
                continue
            year_raw = _coerce_float(row[year_index])
            if year_raw is None:
                continue
            year_value = int(year_raw)
            wave_value = _coerce_wave(year_value, wave_index, row)
            if wave_value is None or wave_value < 5 or wave_value > 7:
                continue
            weight_value = (
                _coerce_float(row[weight_index]) if weight_index is not None else 1.0
            )
            if weight_value is None or weight_value <= 0:
                weight_value = 1.0
            key = (country, wave_value)
            bucket = sums.setdefault(key, {item: [] for item in WVS_ITEM_VARIABLES})
            for item in WVS_ITEM_VARIABLES:
                raw_value = _coerce_float(row[item_indexes[item]])
                if raw_value is None:
                    continue
                bucket[item].append(_aligned(item, raw_value) * weight_value)

        means_per_country_wave: dict[tuple[str, int], dict[str, float]] = {}
        for key, item_buckets in sums.items():
            item_means: dict[str, float] = {}
            for item, values in item_buckets.items():
                if len(values) >= 50:
                    item_means[item] = float(np.mean(values))
            if len(item_means) >= 8:  # need at least 8/10 items
                means_per_country_wave[key] = item_means

        return means_per_country_wave


def _coerce_wave(year_value: int, wave_index: int | None, row: list[str]) -> int | None:
    """Resolve wave: prefer S002 column, fall back on year-based mapping."""
    if wave_index is not None:
        wave_candidate = _coerce_float(row[wave_index])
        if wave_candidate is not None:
            return int(wave_candidate)
    if 1981 <= year_value <= 1984:
        return 1
    if 1989 <= year_value <= 1993:
        return 2
    if 1994 <= year_value <= 1998:
        return 3
    if 1999 <= year_value <= 2004:
        return 4
    if 2005 <= year_value <= 2009:
        return 5
    if 2010 <= year_value <= 2014:
        return 6
    if 2017 <= year_value <= 2022:
        return 7
    return None


def _select_latest_wave_per_country(
    means_per_country_wave: dict[tuple[str, int], dict[str, float]],
) -> dict[str, tuple[int, dict[str, float]]]:
    latest_per_country: dict[str, tuple[int, dict[str, float]]] = {}
    for (country, wave), item_means in means_per_country_wave.items():
        previous = latest_per_country.get(country)
        if previous is None or wave > previous[0]:
            latest_per_country[country] = (wave, item_means)
    return latest_per_country


def _ridge_fit(features: np.ndarray, targets: np.ndarray, alpha: float = 1.0) -> np.ndarray:
    n_features = features.shape[1]
    sqrt_alpha = np.sqrt(alpha)
    penalty = sqrt_alpha * np.eye(n_features)
    penalty[-1, -1] = 0.0  # do not regularise the intercept (last column)
    augmented_features = np.vstack([features, penalty])
    augmented_targets = np.concatenate([targets, np.zeros(n_features)])
    solution, *_ = np.linalg.lstsq(augmented_features, augmented_targets, rcond=None)
    return solution


def calibrate_and_predict(
    latest_per_country: dict[str, tuple[int, dict[str, float]]],
) -> tuple[dict[str, dict], dict[str, float]]:
    known_wave7 = json.loads(IW_CULTURAL_MAP_PATH.read_text())
    iw_known_by_iso3: dict[str, tuple[float, float]] = {
        entry["iso3"]: (float(entry["ts"]), float(entry["se"]))
        for entry in known_wave7["countries"]
    }

    training_iso3s = sorted(
        iso3 for iso3 in iw_known_by_iso3 if iso3 in latest_per_country
    )
    if len(training_iso3s) < 20:
        raise RuntimeError(
            f"Only {len(training_iso3s)} countries overlap between WVS items and known IW. "
            "Need at least 20 to fit a defensible calibration."
        )

    item_means_per_iso3: dict[str, dict[str, float]] = {}
    for iso3, (_, item_means) in latest_per_country.items():
        item_means_per_iso3[iso3] = item_means

    overall_means_per_item: dict[str, float] = {}
    for item in WVS_ITEM_VARIABLES:
        observed_values = [
            means[item]
            for means in item_means_per_iso3.values()
            if item in means
        ]
        overall_means_per_item[item] = (
            float(np.mean(observed_values)) if observed_values else 0.0
        )

    def feature_vector(item_means: dict[str, float]) -> np.ndarray:
        return np.array(
            [
                item_means.get(item, overall_means_per_item[item])
                for item in WVS_ITEM_VARIABLES
            ]
            + [1.0],
            dtype=float,
        )

    feature_matrix = np.array(
        [feature_vector(item_means_per_iso3[iso3]) for iso3 in training_iso3s]
    )
    targets_ts = np.array([iw_known_by_iso3[iso3][0] for iso3 in training_iso3s])
    targets_se = np.array([iw_known_by_iso3[iso3][1] for iso3 in training_iso3s])

    weights_ts = _ridge_fit(feature_matrix, targets_ts)
    weights_se = _ridge_fit(feature_matrix, targets_se)

    loo_residuals_ts: list[float] = []
    loo_residuals_se: list[float] = []
    for hold_out_index in range(len(training_iso3s)):
        mask = np.ones(len(training_iso3s), dtype=bool)
        mask[hold_out_index] = False
        weights_ts_loo = _ridge_fit(feature_matrix[mask], targets_ts[mask])
        weights_se_loo = _ridge_fit(feature_matrix[mask], targets_se[mask])
        loo_residuals_ts.append(
            targets_ts[hold_out_index]
            - float(feature_matrix[hold_out_index] @ weights_ts_loo)
        )
        loo_residuals_se.append(
            targets_se[hold_out_index]
            - float(feature_matrix[hold_out_index] @ weights_se_loo)
        )
    rmse_ts = float(np.sqrt(np.mean(np.square(loo_residuals_ts))))
    rmse_se = float(np.sqrt(np.mean(np.square(loo_residuals_se))))

    pooled_records: dict[str, dict] = {}
    for entry in known_wave7["countries"]:
        iso3 = entry["iso3"]
        pooled_records[iso3] = {
            "iso3": iso3,
            "ts": float(entry["ts"]),
            "se": float(entry["se"]),
            "ts_ci": float(entry.get("ts_ci", 0.15)),
            "se_ci": float(entry.get("se_ci", 0.15)),
            "n": entry.get("n"),
            "wave": 7,
            "source": "wvs_wave7_official",
        }

    for iso3, (wave, item_means) in latest_per_country.items():
        if iso3 in pooled_records:
            continue
        x_vector = feature_vector(item_means)
        ts_predicted = float(x_vector @ weights_ts)
        se_predicted = float(x_vector @ weights_se)
        pooled_records[iso3] = {
            "iso3": iso3,
            "ts": ts_predicted,
            "se": se_predicted,
            "ts_ci": rmse_ts,
            "se_ci": rmse_se,
            "n": None,
            "wave": wave,
            "source": f"wvs_wave{wave}_predicted_from_items",
        }

    metadata = {
        "training_n": len(training_iso3s),
        "rmse_ts_loo": rmse_ts,
        "rmse_se_loo": rmse_se,
        "items_used": list(WVS_ITEM_VARIABLES),
    }
    return pooled_records, metadata


def write_pooled() -> dict:
    aggregated = aggregate_per_country_wave()
    latest_per_country = _select_latest_wave_per_country(aggregated)
    pooled_records, model_metadata = calibrate_and_predict(latest_per_country)

    payload = {
        "_meta": {
            "source": "WVS Time-Series 1981-2022 (v5.0) — Inglehart-Welzel cultural map coordinates",
            "url": "https://www.worldvaluessurvey.org/WVSDocumentationWVL.jsp",
            "license": "CC-BY 4.0 (non-commercial usage, citation required)",
            "citation": "Inglehart, Haerpfer, Moreno, Welzel et al. (2022). World Values Survey: All Rounds — Country-Pooled Datafile. Dataset Version 3.0.0. doi:10.14281/18241.17",
            "extraction_policy": (
                "Latest wave (5-7) per country. Wave-7 countries already in "
                "cultural_map_wave7.json are kept verbatim ('source': 'wvs_wave7_official'). "
                "Countries observed only in waves 5-6 receive predicted (ts, se) from a "
                "ridge regression calibrated on the wave-7 intersection ('source': "
                "'wvs_waveX_predicted_from_items')."
            ),
            "calibration_metadata": model_metadata,
        },
        "countries": sorted(pooled_records.values(), key=lambda r: r["iso3"]),
    }
    POOLED_OUTPUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return {
        "pooled_records": len(pooled_records),
        "wave7_official": sum(
            1 for r in pooled_records.values() if r["source"] == "wvs_wave7_official"
        ),
        "predicted_from_items": sum(
            1
            for r in pooled_records.values()
            if r["source"].endswith("predicted_from_items")
        ),
        "calibration_metadata": model_metadata,
    }


if __name__ == "__main__":
    result = write_pooled()
    print(json.dumps(result, indent=2))

"""Rapport de couverture des États membres de l'ONU.

Pour chacun des 193 États membres de l'ONU, croise quatre sources :
- géométrie Natural Earth (présence du polygone) ;
- Hofstede dimensions (couverture des 6 indicateurs) ;
- Inglehart-Welzel cultural map (coordonnées TS/SE) ;
- taxonomie ``macro_civilizations.v2.json`` (rôle, sous-ensemble).

Écrit :
- ``data_sources/un_members/coverage_report.md`` — tableau lisible (français) ;
- ``data_sources/un_members/coverage_report.json`` — version machine.
"""
from __future__ import annotations

import json

from apps.basis_builder.geometries import NATURAL_EARTH_ADM0_PATH
from apps.basis_builder.load_hofstede import load_hofstede
from apps.basis_builder.load_iw import load_inglehart_welzel
from apps.basis_builder.projector import project_states
from apps.basis_builder.taxonomy_membership import load_iso3_to_membership
from apps.basis_builder.un_members import UN_MEMBERS_DIR, load_un_member_names_fr

COVERAGE_MARKDOWN_PATH = UN_MEMBERS_DIR / "coverage_report.md"
COVERAGE_JSON_PATH = UN_MEMBERS_DIR / "coverage_report.json"


def _load_geojson_iso3() -> set[str]:
    if not NATURAL_EARTH_ADM0_PATH.exists():
        return set()
    payload = json.loads(NATURAL_EARTH_ADM0_PATH.read_text())
    return {feature["properties"]["iso3"] for feature in payload["features"]}


def build_coverage_records() -> list[dict]:
    un_names = load_un_member_names_fr()
    geojson_iso3 = _load_geojson_iso3()
    hofstede_profiles = load_hofstede()
    iw_coords = load_inglehart_welzel()
    membership_index = load_iso3_to_membership()
    projected_states = project_states()

    records: list[dict] = []
    for iso3 in sorted(un_names.keys()):
        name_fr = un_names[iso3]
        hofstede_profile = hofstede_profiles.get(iso3)
        hofstede_coverage = (
            hofstede_profile.coverage if hofstede_profile is not None else "missing"
        )
        iw_coverage = "present" if iso3 in iw_coords else "missing"
        membership = membership_index.get(iso3)
        projected = projected_states.get(iso3)
        records.append(
            {
                "iso3": iso3,
                "name_fr": name_fr,
                "in_geojson": iso3 in geojson_iso3,
                "hofstede_coverage": hofstede_coverage,
                "iw_coverage": iw_coverage,
                "curated_civilization": membership.curated_civilization
                if membership is not None
                else None,
                "curated_role": membership.curated_role if membership is not None else None,
                "sub_cluster_id": membership.sub_cluster_id
                if membership is not None
                else None,
                "x_viz_provenance": projected.data_quality["x_viz_provenance"]
                if projected is not None
                else "unresolved",
                "x_score_provenance": projected.data_quality["x_score_provenance"]
                if projected is not None
                else "unresolved",
                "in_state_coordinates": projected is not None
                and all(value is not None for value in projected.x_viz)
                and all(value is not None for value in projected.x_score),
            }
        )
    return records


def _is_fully_covered(record: dict) -> bool:
    return (
        record["in_geojson"]
        and record["hofstede_coverage"] in ("present", "imputed")
        and record["iw_coverage"] == "present"
        and record["curated_civilization"] is not None
    )


def _missing_signals(record: dict) -> list[str]:
    missing: list[str] = []
    if not record["in_geojson"]:
        missing.append("géométrie")
    if record["hofstede_coverage"] == "missing":
        missing.append("Hofstede")
    if record["iw_coverage"] == "missing":
        missing.append("Inglehart-Welzel")
    if record["curated_civilization"] is None:
        missing.append("taxonomie (civilisation curatée)")
    return missing


def render_markdown(records: list[dict]) -> str:
    total = len(records)
    fully_covered = sum(1 for record in records if _is_fully_covered(record))
    missing_geometry = [record for record in records if not record["in_geojson"]]
    missing_hofstede = [
        record for record in records if record["hofstede_coverage"] == "missing"
    ]
    missing_iw = [record for record in records if record["iw_coverage"] == "missing"]
    missing_taxonomy = [
        record for record in records if record["curated_civilization"] is None
    ]

    def bullet_list(items: list[dict]) -> str:
        if not items:
            return "_(aucun)_"
        return "\n".join(
            f"- `{record['iso3']}` — {record['name_fr']}" for record in items
        )

    lines: list[str] = []
    lines.append("# Couverture des États membres de l'ONU")
    lines.append("")
    lines.append(
        "Croise la liste canonique des 193 États membres de l'ONU avec les "
        "quatre sources qui alimentent la carte civilisationnelle. Régénéré "
        "par `civvec basis coverage-report`."
    )
    lines.append("")
    lines.append("## Synthèse")
    lines.append("")
    lines.append(f"- Total États ONU : **{total}**")
    lines.append(f"- Couverture intégrale (géométrie + Hofstede + IW + taxonomie) : **{fully_covered}**")
    lines.append(f"- Géométrie absente : **{len(missing_geometry)}**")
    lines.append(f"- Hofstede manquant : **{len(missing_hofstede)}**")
    lines.append(f"- Inglehart-Welzel manquant : **{len(missing_iw)}**")
    lines.append(f"- Civilisation curatée manquante : **{len(missing_taxonomy)}**")
    lines.append("")

    in_state_coords = sum(1 for record in records if record["in_state_coordinates"])
    viz_breakdown: dict[str, int] = {}
    score_breakdown: dict[str, int] = {}
    for record in records:
        viz_breakdown[record["x_viz_provenance"]] = (
            viz_breakdown.get(record["x_viz_provenance"], 0) + 1
        )
        score_breakdown[record["x_score_provenance"]] = (
            score_breakdown.get(record["x_score_provenance"], 0) + 1
        )

    lines.append("## Provenance des coordonnées (cascade d'imputation)")
    lines.append("")
    lines.append(
        f"- États avec `x_viz` ET `x_score` non-nuls dans `state_coordinates.json` : **{in_state_coords} / {total}**"
    )
    lines.append("")
    lines.append("Provenance de `x_viz` :")
    for provenance, count in sorted(viz_breakdown.items()):
        lines.append(f"- `{provenance}` : {count}")
    lines.append("")
    lines.append("Provenance de `x_score` :")
    for provenance, count in sorted(score_breakdown.items()):
        lines.append(f"- `{provenance}` : {count}")
    lines.append("")
    lines.append(
        "Cf. `docs/16_imputation_cascade.md` pour la définition de chaque tier"
        " (`observed` > `imputed_pew` / `imputed_governance` > `centroid_prior`)."
    )
    lines.append("")
    lines.append("## États sans polygone (à charger depuis NE 50m ou source équivalente)")
    lines.append("")
    lines.append(bullet_list(missing_geometry))
    lines.append("")
    lines.append("## États sans données Hofstede")
    lines.append("")
    lines.append(bullet_list(missing_hofstede))
    lines.append("")
    lines.append("## États sans coordonnées Inglehart-Welzel")
    lines.append("")
    lines.append(bullet_list(missing_iw))
    lines.append("")
    lines.append("## États sans rattachement curaté dans la taxonomie")
    lines.append("")
    lines.append(bullet_list(missing_taxonomy))
    lines.append("")
    lines.append("## Tableau détaillé")
    lines.append("")
    lines.append(
        "| ISO3 | Nom (fr) | Géo | Hofstede | IW | Civ. curatée | Sous-ensemble | x_viz prov. | x_score prov. |"
    )
    lines.append(
        "|------|----------|-----|----------|----|--------------|---------------|-------------|---------------|"
    )
    for record in records:
        lines.append(
            "| `{iso3}` | {name} | {geo} | {hof} | {iw} | {civ} | {sub} | {viz} | {score} |".format(
                iso3=record["iso3"],
                name=record["name_fr"],
                geo="✓" if record["in_geojson"] else "✗",
                hof=record["hofstede_coverage"],
                iw=record["iw_coverage"],
                civ=record["curated_civilization"] or "—",
                sub=record["sub_cluster_id"] or "—",
                viz=record["x_viz_provenance"],
                score=record["x_score_provenance"],
            )
        )
    lines.append("")
    return "\n".join(lines)


def write_coverage_report() -> tuple:
    records = build_coverage_records()
    UN_MEMBERS_DIR.mkdir(parents=True, exist_ok=True)
    COVERAGE_JSON_PATH.write_text(
        json.dumps(
            {
                "_meta": {
                    "total_un_members": len(records),
                    "schema_version": "1.0.0",
                },
                "records": records,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    COVERAGE_MARKDOWN_PATH.write_text(render_markdown(records))
    return COVERAGE_JSON_PATH, COVERAGE_MARKDOWN_PATH

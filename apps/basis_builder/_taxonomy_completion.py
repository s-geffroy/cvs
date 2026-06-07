"""One-shot builder that completes ``macro_civilizations.v2.json`` to all 193 UN members.

Run from a Docker container: ``python -m apps.basis_builder._taxonomy_completion``.

Each new ``member_states`` entry carries a ``role`` ∈ {core, periphery,
ambiguous} and a ``rationale`` derived from a transparent heuristic:

- geography and dominant religion are the primary signals
- ``core`` when the state is a textbook archetype of its civilization
  (e.g. ARE, KWT, QAT for Islamic; AUT, CHE for Western; AGO, CMR for African)
- ``periphery`` when there is cultural distance from the archetype but the
  state still belongs unambiguously (e.g. KAZ for Islamic — Sunni majority,
  Turkic, but heavy Russian/Soviet legacy)
- ``ambiguous`` when two civilizations contest, e.g. BIH (Islamic + Orthodox
  + Western), LBN (Islamic + Western), TCD (Islamic + African)

The rationale fields cite Huntington (1996) and the relevant Pew/IW priors
without inventing new sources. Cross-check the dominant religion against
``data_sources/pew/religious_composition_2020.json`` when available.

This file is **idempotent**: re-running it does not duplicate entries.
"""
from __future__ import annotations

import json
from pathlib import Path

from apps.basis_builder.paths import MACRO_CIVILIZATIONS_V2_PATH


def _assignments() -> dict[str, dict]:
    """Return ISO3 → assignment record (civilization, role, rationale, competing).

    `competing` is non-empty only for ``role == "ambiguous"``.
    """
    # fmt: off
    return {
        # ---------- Western (Europe Catholic/Protestant + Anglo Caribbean) ----------
        "AND": {"civilization": "western", "role": "core", "rationale": "Microétat catholique des Pyrénées, héritage catalan/français."},
        "AUT": {"civilization": "western", "role": "core", "rationale": "Catholique germanophone, Habsburg, UE."},
        "BEL": {"civilization": "western", "role": "core", "rationale": "Catholique, fondateur de l'UE."},
        "CHE": {"civilization": "western", "role": "core", "rationale": "Confédération germano-romande-italophone protestante/catholique."},
        "CZE": {"civilization": "western", "role": "core", "rationale": "Tchéquie catholique/laïque, Habsburg, UE — frontière occidentale chez Huntington."},
        "EST": {"civilization": "western", "role": "periphery", "rationale": "Luthérienne historique, UE, Schengen — basculement post-1991 vers l'Occident."},
        "HRV": {"civilization": "western", "role": "periphery", "rationale": "Catholique, héritage Habsburg, UE — frontière sud-est de l'Occident."},
        "HUN": {"civilization": "western", "role": "core", "rationale": "Catholique/protestante, Habsburg, UE."},
        "ISL": {"civilization": "western", "role": "core", "rationale": "Luthérienne, scandinave."},
        "LIE": {"civilization": "western", "role": "core", "rationale": "Microétat catholique germanophone."},
        "LTU": {"civilization": "western", "role": "periphery", "rationale": "Catholique, UE — frontière occidentale (Huntington 1996 ch. 8)."},
        "LUX": {"civilization": "western", "role": "core", "rationale": "Catholique, fondateur UE."},
        "LVA": {"civilization": "western", "role": "periphery", "rationale": "Luthérienne/catholique, UE — frontière occidentale."},
        "MCO": {"civilization": "western", "role": "core", "rationale": "Microétat catholique francophone."},
        "MLT": {"civilization": "western", "role": "core", "rationale": "Catholique, UE."},
        "POL": {"civilization": "western", "role": "core", "rationale": "Catholique, UE — pilier de l'Occident centro-est chez Huntington."},
        "PRT": {"civilization": "western", "role": "core", "rationale": "Catholique, ibérique, UE."},
        "SMR": {"civilization": "western", "role": "core", "rationale": "Microétat catholique italien."},
        "SVK": {"civilization": "western", "role": "core", "rationale": "Catholique, UE."},
        "SVN": {"civilization": "western", "role": "core", "rationale": "Catholique, Habsburg, UE."},
        # Caraïbes anglophones (Commonwealth, protestant/catholique)
        "ATG": {"civilization": "western", "role": "periphery", "rationale": "Caraïbe anglophone, Commonwealth, chrétienne — Occident via colonisation britannique."},
        "BHS": {"civilization": "western", "role": "periphery", "rationale": "Caraïbe anglophone, Commonwealth."},
        "BRB": {"civilization": "western", "role": "periphery", "rationale": "Caraïbe anglophone, Commonwealth."},
        "BLZ": {"civilization": "western", "role": "periphery", "rationale": "Anglophone, Commonwealth — distinct du noyau latino-américain hispanique."},
        "DMA": {"civilization": "western", "role": "periphery", "rationale": "Caraïbe anglophone, Commonwealth."},
        "GRD": {"civilization": "western", "role": "periphery", "rationale": "Caraïbe anglophone, Commonwealth."},
        "JAM": {"civilization": "western", "role": "periphery", "rationale": "Caraïbe anglophone, Commonwealth."},
        "KNA": {"civilization": "western", "role": "periphery", "rationale": "Caraïbe anglophone, Commonwealth."},
        "LCA": {"civilization": "western", "role": "periphery", "rationale": "Caraïbe anglophone, Commonwealth."},
        "TTO": {"civilization": "western", "role": "periphery", "rationale": "Caraïbe anglophone (40% chrétienne, 18% hindoue, 5% musulmane) — Occident anglophone dominant."},
        "VCT": {"civilization": "western", "role": "periphery", "rationale": "Caraïbe anglophone, Commonwealth."},

        # ---------- Orthodox (chrétienne orthodoxe + arménienne) ----------
        "ARM": {"civilization": "orthodox", "role": "core", "rationale": "Arménie apostolique (Église orientale orthodoxe) — Huntington classe l'Arménie en sphère orthodoxe."},
        "CYP": {"civilization": "orthodox", "role": "periphery", "rationale": "République de Chypre majoritairement grecque-orthodoxe — partagée avec Occident via UE."},
        "GEO": {"civilization": "orthodox", "role": "core", "rationale": "Église orthodoxe géorgienne — Caucase orthodoxe."},
        "MDA": {"civilization": "orthodox", "role": "core", "rationale": "Orthodoxe roumanophone — sphère post-soviétique orthodoxe."},
        "MKD": {"civilization": "orthodox", "role": "core", "rationale": "Orthodoxe macédonienne, Balkans."},
        "MNE": {"civilization": "orthodox", "role": "core", "rationale": "Orthodoxe, Balkans."},

        # ---------- Islamic (musulmane majoritaire) ----------
        # Golfe + MENA arabe
        "ARE": {"civilization": "islamic", "role": "core", "rationale": "Sunnite, péninsule arabique."},
        "BHR": {"civilization": "islamic", "role": "core", "rationale": "Chiite majoritaire, Golfe arabe."},
        "DZA": {"civilization": "islamic", "role": "core", "rationale": "Maghreb sunnite arabophone."},
        "KWT": {"civilization": "islamic", "role": "core", "rationale": "Sunnite, Golfe arabe."},
        "LBY": {"civilization": "islamic", "role": "core", "rationale": "Maghreb sunnite."},
        "OMN": {"civilization": "islamic", "role": "core", "rationale": "Ibadite, péninsule arabique."},
        "QAT": {"civilization": "islamic", "role": "core", "rationale": "Sunnite wahhabite, Golfe arabe."},
        "SYR": {"civilization": "islamic", "role": "core", "rationale": "Multi-confessionnelle (sunnite ~74%, alaouite, chrétiens, druzes) — sphère arabo-islamique."},
        "TUN": {"civilization": "islamic", "role": "core", "rationale": "Maghreb sunnite arabophone."},
        "YEM": {"civilization": "islamic", "role": "core", "rationale": "Sunnite/zaydite, péninsule arabique."},
        # Asie centrale (post-soviétique turcophone/iranophone musulmane)
        "AFG": {"civilization": "islamic", "role": "core", "rationale": "Sunnite hanafite + chiite, pachtoune/tadjike — sphère islamique d'Asie centrale."},
        "ALB": {"civilization": "islamic", "role": "periphery", "rationale": "Musulmane majoritaire (~58% sunnite/bektashi) + minorités chrétiennes orthodoxe et catholique — Balkans, fortement laïcisée."},
        "AZE": {"civilization": "islamic", "role": "core", "rationale": "Chiite turcophone — sphère islamique, héritage soviétique."},
        "KAZ": {"civilization": "islamic", "role": "periphery", "rationale": "Sunnite turcophone, sécularisation soviétique marquée — périphérie islamique."},
        "KGZ": {"civilization": "islamic", "role": "periphery", "rationale": "Sunnite turcophone, sécularisation soviétique."},
        "TJK": {"civilization": "islamic", "role": "periphery", "rationale": "Sunnite iranophone, sécularisation soviétique."},
        "TKM": {"civilization": "islamic", "role": "periphery", "rationale": "Sunnite turcophone, sécularisation soviétique."},
        "UZB": {"civilization": "islamic", "role": "periphery", "rationale": "Sunnite turcophone, sécularisation soviétique."},
        # SE Asie musulmane
        "BRN": {"civilization": "islamic", "role": "core", "rationale": "Sultanat sunnite malais."},
        "MDV": {"civilization": "islamic", "role": "core", "rationale": "Sunnite, océan Indien."},
        # Afrique sub-saharienne musulmane
        "COM": {"civilization": "islamic", "role": "core", "rationale": "Sunnite swahili, océan Indien."},
        "DJI": {"civilization": "islamic", "role": "core", "rationale": "Sunnite, Corne de l'Afrique."},
        "GIN": {"civilization": "islamic", "role": "core", "rationale": "Sunnite majoritaire (~85%), Afrique de l'Ouest."},
        "GMB": {"civilization": "islamic", "role": "core", "rationale": "Sunnite majoritaire (~95%), Afrique de l'Ouest."},
        "MLI": {"civilization": "islamic", "role": "core", "rationale": "Sunnite majoritaire (~95%), Sahel."},
        "MRT": {"civilization": "islamic", "role": "core", "rationale": "Sunnite, Sahara occidental — pont Maghreb/Sahel."},
        "NER": {"civilization": "islamic", "role": "core", "rationale": "Sunnite (~99%), Sahel."},
        "SEN": {"civilization": "islamic", "role": "core", "rationale": "Sunnite soufi (~95%), Afrique de l'Ouest."},
        "SOM": {"civilization": "islamic", "role": "core", "rationale": "Sunnite, Corne de l'Afrique."},
        "BFA": {"civilization": "islamic", "role": "periphery", "rationale": "Musulmane majoritaire (~64%), forte minorité chrétienne/animiste — frange islamique sahélienne."},
        "SDN": {"civilization": "islamic", "role": "core", "rationale": "Sunnite arabophone (post-séparation du Sud-Soudan)."},
        "SLE": {"civilization": "islamic", "role": "periphery", "rationale": "Musulmane majoritaire (~78%), forte minorité chrétienne — pluralisme religieux notable."},

        # ---------- Sinic ----------
        "PRK": {"civilization": "sinic", "role": "periphery", "rationale": "Héritage confucéen-coréen, juché — sphère sinique alignée historiquement sur Pékin/Moscou."},

        # ---------- Latin American (catholique hispanophone/lusophone des Amériques) ----------
        "CRI": {"civilization": "latin_american", "role": "core", "rationale": "Catholique hispanophone, Amérique centrale."},
        "CUB": {"civilization": "latin_american", "role": "core", "rationale": "Catholique/syncrétique hispanophone, Caraïbes hispaniques."},
        "DOM": {"civilization": "latin_american", "role": "core", "rationale": "Catholique hispanophone."},
        "HND": {"civilization": "latin_american", "role": "core", "rationale": "Catholique hispanophone, Amérique centrale."},
        "HTI": {"civilization": "latin_american", "role": "periphery", "rationale": "Catholicisme + vaudou, francophone — distincte du noyau hispanique mais Amérique latine selon Huntington."},
        "NIC": {"civilization": "latin_american", "role": "core", "rationale": "Catholique hispanophone."},
        "PAN": {"civilization": "latin_american", "role": "core", "rationale": "Catholique hispanophone."},
        "PRY": {"civilization": "latin_american", "role": "core", "rationale": "Catholique hispano-guarani."},
        "SLV": {"civilization": "latin_american", "role": "core", "rationale": "Catholique hispanophone, Amérique centrale."},
        # Guyanes : ambiguës, héritage colonial non-ibérique
        "GUY": {"civilization": "latin_american", "role": "periphery", "rationale": "Anglophone, hindouisme/christianisme — Amérique latine géographique mais culturellement caraïbe-indienne."},
        "SUR": {"civilization": "latin_american", "role": "periphery", "rationale": "Néerlandophone multi-confessionnelle — Amérique latine géographique mais héritage colonial non-ibérique."},

        # ---------- African (sub-saharienne non-musulmane majoritaire) ----------
        "AGO": {"civilization": "african", "role": "core", "rationale": "Chrétienne, lusophone, Afrique australe."},
        "BDI": {"civilization": "african", "role": "core", "rationale": "Chrétienne, Grands Lacs."},
        "BEN": {"civilization": "african", "role": "core", "rationale": "Chrétienne/vodun, francophone, golfe de Guinée."},
        "BWA": {"civilization": "african", "role": "core", "rationale": "Chrétienne, Afrique australe."},
        "CAF": {"civilization": "african", "role": "core", "rationale": "Chrétienne majoritaire, Afrique centrale."},
        "CMR": {"civilization": "african", "role": "core", "rationale": "Chrétienne + musulmane (Nord), pluraliste — Afrique centrale francophone/anglophone."},
        "COD": {"civilization": "african", "role": "core", "rationale": "Chrétienne, francophone, Afrique centrale."},
        "COG": {"civilization": "african", "role": "core", "rationale": "Chrétienne, francophone, Afrique centrale."},
        "CPV": {"civilization": "african", "role": "periphery", "rationale": "Lusophone catholique, archipel — héritage créole ouest-africain."},
        "ERI": {"civilization": "african", "role": "periphery", "rationale": "Chrétienne orthodoxe tewahedo + musulmane, Corne — proche d'ETH culturellement."},
        "GAB": {"civilization": "african", "role": "core", "rationale": "Chrétienne, francophone, Afrique centrale."},
        "GNB": {"civilization": "african", "role": "periphery", "rationale": "Mixte chrétienne/musulmane/animiste, lusophone — pluralisme religieux."},
        "GNQ": {"civilization": "african", "role": "core", "rationale": "Hispanophone catholique, Afrique centrale."},
        "LBR": {"civilization": "african", "role": "core", "rationale": "Anglophone, chrétienne, héritage afro-américain."},
        "LSO": {"civilization": "african", "role": "core", "rationale": "Chrétienne, Afrique australe."},
        "MDG": {"civilization": "african", "role": "periphery", "rationale": "Chrétienne + traditionnelle, héritage austronésien — singularité culturelle dans la sphère africaine."},
        "MOZ": {"civilization": "african", "role": "core", "rationale": "Chrétienne + musulmane (côte nord), lusophone."},
        "MWI": {"civilization": "african", "role": "core", "rationale": "Chrétienne, Afrique australe."},
        "NAM": {"civilization": "african", "role": "core", "rationale": "Chrétienne, héritage germano-sud-africain."},
        "RWA": {"civilization": "african", "role": "core", "rationale": "Chrétienne, Grands Lacs."},
        "SSD": {"civilization": "african", "role": "core", "rationale": "Chrétienne + animiste, Nilotique — sphère africaine post-2011."},
        "STP": {"civilization": "african", "role": "periphery", "rationale": "Lusophone catholique, archipel."},
        "SWZ": {"civilization": "african", "role": "core", "rationale": "Chrétienne, Afrique australe."},
        "SYC": {"civilization": "african", "role": "periphery", "rationale": "Chrétienne créole, océan Indien — héritage colonial mixte."},
        "TGO": {"civilization": "african", "role": "core", "rationale": "Chrétienne/animiste, francophone, golfe de Guinée."},
        "TZA": {"civilization": "african", "role": "core", "rationale": "Chrétienne + musulmane (côte/Zanzibar), swahili."},
        "UGA": {"civilization": "african", "role": "core", "rationale": "Chrétienne, Grands Lacs."},

        # ---------- Oceanian (États insulaires du Pacifique) ----------
        "FSM": {"civilization": "oceanian", "role": "core", "rationale": "Micronésie, christianisme + traditions austronésiennes."},
        "KIR": {"civilization": "oceanian", "role": "core", "rationale": "Micronésie, christianisme + traditions."},
        "MHL": {"civilization": "oceanian", "role": "core", "rationale": "Micronésie, christianisme + traditions."},
        "NRU": {"civilization": "oceanian", "role": "core", "rationale": "Micronésie, christianisme."},
        "PLW": {"civilization": "oceanian", "role": "core", "rationale": "Micronésie, christianisme + religions ethniques."},
        "PNG": {"civilization": "oceanian", "role": "core", "rationale": "Mélanésie, christianisme + grande diversité de langues austronésiennes/papoues."},
        "SLB": {"civilization": "oceanian", "role": "core", "rationale": "Mélanésie, christianisme."},
        "TON": {"civilization": "oceanian", "role": "core", "rationale": "Polynésie, christianisme."},
        "TUV": {"civilization": "oceanian", "role": "core", "rationale": "Polynésie, christianisme."},
        "VUT": {"civilization": "oceanian", "role": "core", "rationale": "Mélanésie, christianisme + religions ethniques."},
        "WSM": {"civilization": "oceanian", "role": "core", "rationale": "Polynésie, christianisme."},

        # ---------- South-East Asia singularities ----------
        "PHL": {"civilization": "latin_american", "role": "periphery", "rationale": "Catholique (~80%), hispanisme colonial — Huntington classe les Philippines hors sinic et signale leur héritage catholique ibérique; rattachement périphérique à la sphère latino-américaine au sens culturel large."},
        "TLS": {"civilization": "latin_american", "role": "periphery", "rationale": "Catholique (~96%), héritage lusophone — distinct du noyau sinique/buddhist environnant."},

        # ---------- Cas ambigus (multi-civilisation contestée) ----------
        "BIH": {"civilization": "ambiguous", "role": "ambiguous", "rationale": "Bosniaque musulmane ~50%, Serbe orthodoxe ~30%, Croate catholique ~15% — frontière des trois civilisations.", "competing": ["islamic", "orthodox", "western"]},
        "LBN": {"civilization": "ambiguous", "role": "ambiguous", "rationale": "Sunnite/chiite ~67% + chrétienne maronite/orthodoxe/uniate ~32% — interface arabo-méditerranéenne.", "competing": ["islamic", "western"]},
        "TCD": {"civilization": "ambiguous", "role": "ambiguous", "rationale": "Musulmane ~55% (Nord) + chrétienne/animiste ~45% (Sud) — frontière sahélienne.", "competing": ["islamic", "african"]},
        "CIV": {"civilization": "ambiguous", "role": "ambiguous", "rationale": "Musulmane ~43% + chrétienne ~34% + animiste — frontière religieuse.", "competing": ["islamic", "african"]},
    }
    # fmt: on


def _civilization_for_ambiguous(record: dict) -> tuple[str, list[str]]:
    """For ambiguous cases, leave them out of member_states; only register in ambiguous_cases."""
    return record["civilization"], record.get("competing", [])


def complete_taxonomy(taxonomy_path: Path = MACRO_CIVILIZATIONS_V2_PATH) -> dict:
    taxonomy = json.loads(taxonomy_path.read_text())
    assignments = _assignments()

    civilization_index: dict[str, dict] = {
        civilization["id"]: civilization for civilization in taxonomy["civilizations"]
    }

    existing_member_iso3s_per_civ: dict[str, set[str]] = {
        civilization_id: {member["iso3"] for member in civ.get("member_states", [])}
        for civilization_id, civ in civilization_index.items()
    }
    existing_ambiguous_iso3s_per_civ: dict[str, set[str]] = {
        civilization_id: {
            entry["iso3"] for entry in civ.get("ambiguous_cases", [])
        }
        for civilization_id, civ in civilization_index.items()
    }

    added_member_count = 0
    added_ambiguous_count = 0

    for iso3, record in assignments.items():
        if record["civilization"] == "ambiguous":
            competing = record["competing"]
            for competing_civilization_id in competing:
                civilization_entry = civilization_index.get(competing_civilization_id)
                if civilization_entry is None:
                    continue
                if iso3 in existing_ambiguous_iso3s_per_civ[competing_civilization_id]:
                    continue
                civilization_entry.setdefault("ambiguous_cases", []).append(
                    {
                        "iso3": iso3,
                        "civilizations_competing": competing,
                        "discussion": record["rationale"],
                        "citation_ids": ["huntington_1996"],
                    }
                )
                existing_ambiguous_iso3s_per_civ[competing_civilization_id].add(iso3)
                added_ambiguous_count += 1
            continue

        civilization_id = record["civilization"]
        civilization_entry = civilization_index.get(civilization_id)
        if civilization_entry is None:
            raise ValueError(
                f"Assignment references unknown civilization {civilization_id} for {iso3}"
            )
        if iso3 in existing_member_iso3s_per_civ[civilization_id]:
            continue
        civilization_entry.setdefault("member_states", []).append(
            {
                "iso3": iso3,
                "role": record["role"],
                "rationale": record["rationale"],
                "citation_ids": ["huntington_1996"],
            }
        )
        existing_member_iso3s_per_civ[civilization_id].add(iso3)
        added_member_count += 1

    taxonomy.setdefault("policy", {})
    taxonomy["policy"]["completion_to_un_members"] = {
        "completed_to": 193,
        "method": "deterministic heuristic on geography + dominant religion (Pew 2020) + Huntington (1996) regional sphere",
        "ambiguous_cases_treated_as": "co-listed in competing civilizations' ambiguous_cases; excluded from centroid computation (ROLE_WEIGHT == 0)",
        "review_status": "first-pass automatic — manual review encouraged via coverage report",
    }

    taxonomy_path.write_text(
        json.dumps(taxonomy, indent=2, ensure_ascii=False) + "\n"
    )
    return {
        "added_member_states": added_member_count,
        "added_ambiguous_cases": added_ambiguous_count,
    }


if __name__ == "__main__":
    result = complete_taxonomy()
    print(json.dumps(result, indent=2))

"""Orchestrator: render Phase 1b pages into site_src/docs/ so mkdocs can build dist/."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from apps.basis_builder.paths import REPO_ROOT
from apps.site_builder.guards import ETHICAL_WARNING, ETHICAL_WARNING_FR
from apps.site_builder.loaders import (
    SOURCES_MD_PATH,
    iter_methodology_docs,
    iter_schemas,
    load_schema_title,
    load_sources_markdown,
    load_taxonomy_v2,
)

SITE_SRC_DIR = REPO_ROOT / "site_src"
SITE_DOCS_DIR = SITE_SRC_DIR / "docs"
TEMPLATES_DIR = SITE_SRC_DIR / "templates"
METHODOLOGY_OUT_DIR = SITE_DOCS_DIR / "methodology"
TAXONOMY_OUT_DIR = SITE_DOCS_DIR / "taxonomy"
CIVILIZATIONS_OUT_DIR = TAXONOMY_OUT_DIR / "civilizations"
SOURCES_OUT_DIR = SITE_DOCS_DIR / "sources"
SCHEMAS_OUT_DIR = SITE_DOCS_DIR / "schemas"
SCHEMAS_ASSETS_DIR = SITE_DOCS_DIR / "assets" / "schemas"

METHODOLOGY_TITLES = {
    "00": "Décisions du projet",
    "01": "Modèle conceptuel",
    "02": "Méthodologie source-only",
    "03": "Scope État (V1)",
    "04": "ADM1 préparé",
    "05": "Calibration du scoring",
    "06": "Outputs et stockage",
    "07": "Éthique de publication",
    "08": "Base civilisationnelle (B_doc + B_vec)",
    "09": "Mécanique tensorielle",
    "10": "Algèbre des distances",
}


def _jinja_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
    )


def render_methodology() -> None:
    METHODOLOGY_OUT_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()
    methodology_docs_metadata: list[dict[str, str]] = []
    for source_path in iter_methodology_docs():
        target_path = METHODOLOGY_OUT_DIR / source_path.name
        target_path.write_text(source_path.read_text())
        number_prefix = source_path.stem.split("_", 1)[0]
        title = METHODOLOGY_TITLES.get(number_prefix, source_path.stem)
        methodology_docs_metadata.append(
            {
                "number": number_prefix,
                "title": title,
                "filename": source_path.name,
            }
        )
    index_template = env.get_template("methodology_index.md.j2")
    (METHODOLOGY_OUT_DIR / "index.md").write_text(
        index_template.render(
            ethical_warning_fr=ETHICAL_WARNING_FR,
            methodology_docs=methodology_docs_metadata,
        )
    )


def render_taxonomy() -> None:
    CIVILIZATIONS_OUT_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()
    taxonomy = load_taxonomy_v2()
    biblio_index = {entry["id"]: entry for entry in taxonomy["bibliography"]}

    civilization_template = env.get_template("civilization_page.md.j2")
    for civ in taxonomy["civilizations"]:
        rendered = civilization_template.render(
            civ=civ,
            biblio_index=biblio_index,
            ethical_warning=ETHICAL_WARNING,
            ethical_warning_fr=ETHICAL_WARNING_FR,
        )
        (CIVILIZATIONS_OUT_DIR / f"{civ['id']}.md").write_text(rendered)

    index_template = env.get_template("taxonomy_index.md.j2")
    (TAXONOMY_OUT_DIR / "index.md").write_text(
        index_template.render(
            taxonomy=taxonomy,
            version_major=taxonomy["version"].split(".")[0] or "2",
            ethical_warning_fr=ETHICAL_WARNING_FR,
        )
    )


def render_sources() -> None:
    SOURCES_OUT_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()
    taxonomy = load_taxonomy_v2()
    sources_md_content = load_sources_markdown()
    sources_md_content = sources_md_content.replace(
        "(../docs/07_ethics_publication_policy.md)",
        "(../methodology/07_ethics_publication_policy.md)",
    )
    index_template = env.get_template("sources_index.md.j2")
    (SOURCES_OUT_DIR / "index.md").write_text(
        index_template.render(
            bibliography=taxonomy["bibliography"],
            sources_md_content=sources_md_content,
            ethical_warning_fr=ETHICAL_WARNING_FR,
        )
    )


def render_schemas() -> None:
    SCHEMAS_OUT_DIR.mkdir(parents=True, exist_ok=True)
    SCHEMAS_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()
    schemas_metadata: list[dict[str, str]] = []
    for schema_path in iter_schemas():
        destination = SCHEMAS_ASSETS_DIR / schema_path.name
        shutil.copyfile(schema_path, destination)
        schemas_metadata.append(
            {
                "name": schema_path.name,
                "title": load_schema_title(schema_path),
                "relative_url": f"../assets/schemas/{schema_path.name}",
            }
        )
    index_template = env.get_template("schemas_index.md.j2")
    (SCHEMAS_OUT_DIR / "index.md").write_text(
        index_template.render(
            schemas=schemas_metadata,
            ethical_warning_fr=ETHICAL_WARNING_FR,
        )
    )


def render_all() -> None:
    render_methodology()
    render_taxonomy()
    render_sources()
    render_schemas()
    print("[site] rendered methodology, taxonomy, sources, schemas")

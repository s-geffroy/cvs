"""JSON / Markdown loaders for the site builder."""
from __future__ import annotations

import json
from pathlib import Path

from apps.basis_builder.paths import (
    DATA_SOURCES_DIR,
    MACRO_CIVILIZATIONS_V2_PATH,
    REPO_ROOT,
    SCHEMAS_DIR,
)

DOCS_DIR = REPO_ROOT / "docs"
SOURCES_MD_PATH = DATA_SOURCES_DIR / "SOURCES.md"


def load_taxonomy_v2() -> dict:
    return json.loads(MACRO_CIVILIZATIONS_V2_PATH.read_text())


def load_sources_markdown() -> str:
    return SOURCES_MD_PATH.read_text() if SOURCES_MD_PATH.exists() else ""


def iter_methodology_docs() -> list[Path]:
    return sorted(DOCS_DIR.glob("[0-9][0-9]_*.md"))


def iter_schemas() -> list[Path]:
    return sorted(SCHEMAS_DIR.glob("*.schema.json"))


def load_schema_title(schema_path: Path) -> str:
    try:
        payload = json.loads(schema_path.read_text())
        return str(payload.get("title", schema_path.name))
    except json.JSONDecodeError:
        return schema_path.name

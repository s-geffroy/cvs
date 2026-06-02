"""Render the standalone 'vulgarisation' mini-site (hors-thème Material).

This module reads Markdown sources from `site_src/vulgarisation_src/`, converts
them to HTML, wraps them in a custom Jinja2 layout (no MkDocs Material chrome),
and writes the result into `site_src/docs/vulgarisation/` so that mkdocs picks
them up as-is (non-Markdown files are copied verbatim).

The mini-site is excluded from the MkDocs nav via `not_in_nav: /vulgarisation/**`
in mkdocs.yml. A single external nav entry links back from the main site.
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

import markdown as md_lib
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from apps.basis_builder.paths import REPO_ROOT
from apps.site_builder.guards import ETHICAL_WARNING_FR

VULGARISATION_SRC_DIR = REPO_ROOT / "site_src" / "vulgarisation_src"
VULGARISATION_OUT_DIR = REPO_ROOT / "site_src" / "docs" / "vulgarisation"
VULGARISATION_ASSETS_SRC = VULGARISATION_SRC_DIR / "assets"
VULGARISATION_ASSETS_OUT = VULGARISATION_OUT_DIR / "assets"


@dataclass(frozen=True)
class PageContext:
    """Metadata used by the layout to render a single page."""

    title: str
    audience: str
    relative_to_root: str
    body_html: str
    sub_nav: list[dict[str, str]]
    section_label: str
    section_slug: str


def _jinja_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(VULGARISATION_SRC_DIR)),
        autoescape=False,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
    )


def _markdown_to_html(text: str) -> str:
    converter = md_lib.Markdown(
        extensions=["extra", "sane_lists", "toc", "admonition", "attr_list"],
        output_format="html5",
    )
    return converter.convert(text)


def _split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse a minimal YAML-ish frontmatter (key: value pairs only)."""
    if not text.startswith("---\n"):
        return {}, text
    _, rest = text.split("---\n", 1)
    if "\n---\n" not in rest:
        return {}, text
    header, body = rest.split("\n---\n", 1)
    metadata: dict[str, str] = {}
    for line in header.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, body.lstrip("\n")


SECTIONS = [
    {
        "slug": "niveau-1-citoyen",
        "label": "Niveau 1 — Citoyen curieux",
        "audience": "Citoyen / lycéen — métaphores, exemples concrets, zéro math.",
        "pages": [
            ("index", "Le tour en 5 minutes"),
            ("qu-est-ce-qu-une-civilisation", "Qu'est-ce qu'une « civilisation » ici ?"),
            ("comment-on-classe-un-pays", "Comment on « classe » un pays ?"),
            ("si-la-france-etait", "Si la France était…"),
            ("pourquoi-c-est-imparfait", "Pourquoi c'est imparfait"),
        ],
    },
    {
        "slug": "niveau-2-journaliste",
        "label": "Niveau 2 — Journaliste, décideur",
        "audience": "Journaliste / décideur — comment lire, limites, boîte à outils.",
        "pages": [
            ("index", "Le brief en 10 minutes"),
            ("comment-lire-la-carte", "Comment lire la carte"),
            ("les-3-distances-en-1-image", "Les 3 distances en une image"),
            ("ce-que-ces-chiffres-ne-disent-pas", "Ce que ces chiffres ne disent pas"),
            ("boite-a-outils-redactionnelle", "Boîte à outils rédactionnelle"),
        ],
    },
    {
        "slug": "niveau-3-etudiant-shs",
        "label": "Niveau 3 — Étudiant SHS",
        "audience": "Étudiant en sciences humaines — Huntington, Hofstede, IW, sans le bayésien.",
        "pages": [
            ("index", "Le panorama académique"),
            ("huntington-en-2-pages", "Huntington en 2 pages"),
            ("hofstede-en-2-pages", "Hofstede en 2 pages"),
            ("inglehart-welzel-en-2-pages", "Inglehart-Welzel en 2 pages"),
            ("ce-que-le-bayesien-apporte", "Ce que le bayésien apporte (sans dériver)"),
            ("controverses-academiques", "Controverses académiques"),
        ],
    },
]

TRANSVERSE_PAGES = [
    ("glossaire-illustre", "Glossaire illustré", "Transverse"),
    ("faq", "Questions fréquentes", "Transverse"),
    ("credits", "Crédits et sources", "Transverse"),
]


def _build_sub_nav(section: dict) -> list[dict[str, str]]:
    return [
        {
            "slug": slug,
            "label": label,
            "href": f"{slug}.html" if slug != "index" else "index.html",
        }
        for slug, label in section["pages"]
    ]


def _render_layout(env: Environment, ctx: PageContext) -> str:
    layout = env.get_template("_layout.html.j2")
    relative_to_main_site = (
        "../" if ctx.relative_to_root == "./" else ctx.relative_to_root + "../"
    )
    return layout.render(
        page_title=ctx.title,
        section_label=ctx.section_label,
        section_slug=ctx.section_slug,
        audience=ctx.audience,
        body_html=ctx.body_html,
        sub_nav=ctx.sub_nav,
        relative_to_root=ctx.relative_to_root,
        relative_to_main_site=relative_to_main_site,
        ethical_warning_fr=ETHICAL_WARNING_FR,
        all_sections=SECTIONS,
        transverse_pages=TRANSVERSE_PAGES,
    )


def _read_and_render_md(env: Environment, src: Path, ctx_kwargs: dict) -> str:
    raw = src.read_text(encoding="utf-8")
    metadata, body = _split_frontmatter(raw)
    title = metadata.get("title") or ctx_kwargs["title"]
    body_html = _markdown_to_html(body)
    ctx = PageContext(
        title=title,
        audience=ctx_kwargs["audience"],
        relative_to_root=ctx_kwargs["relative_to_root"],
        body_html=body_html,
        sub_nav=ctx_kwargs["sub_nav"],
        section_label=ctx_kwargs["section_label"],
        section_slug=ctx_kwargs["section_slug"],
    )
    return _render_layout(env, ctx)


def _copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def render_vulgarisation() -> None:
    """Render the vulgarisation mini-site under site_src/docs/vulgarisation/."""
    if not VULGARISATION_SRC_DIR.exists():
        print("[site] vulgarisation source missing — skipping")
        return

    VULGARISATION_OUT_DIR.mkdir(parents=True, exist_ok=True)
    env = _jinja_env()

    hub_src = VULGARISATION_SRC_DIR / "index.md"
    if hub_src.exists():
        hub_html = _read_and_render_md(
            env,
            hub_src,
            {
                "title": "Comprendre cvs sans les maths",
                "audience": "Trois portes d'entrée selon votre profil.",
                "relative_to_root": "./",
                "sub_nav": [],
                "section_label": "Accueil",
                "section_slug": "hub",
            },
        )
        (VULGARISATION_OUT_DIR / "index.html").write_text(hub_html, encoding="utf-8")

    for section in SECTIONS:
        section_dir_src = VULGARISATION_SRC_DIR / section["slug"]
        section_dir_out = VULGARISATION_OUT_DIR / section["slug"]
        section_dir_out.mkdir(parents=True, exist_ok=True)
        sub_nav = _build_sub_nav(section)
        for slug, label in section["pages"]:
            page_src = section_dir_src / f"{slug}.md"
            if not page_src.exists():
                continue
            html = _read_and_render_md(
                env,
                page_src,
                {
                    "title": label,
                    "audience": section["audience"],
                    "relative_to_root": "../",
                    "sub_nav": sub_nav,
                    "section_label": section["label"],
                    "section_slug": section["slug"],
                },
            )
            out_path = section_dir_out / f"{slug}.html"
            out_path.write_text(html, encoding="utf-8")

    for slug, label, section_label in TRANSVERSE_PAGES:
        page_src = VULGARISATION_SRC_DIR / f"{slug}.md"
        if not page_src.exists():
            continue
        html = _read_and_render_md(
            env,
            page_src,
            {
                "title": label,
                "audience": "Pages transverses (tous publics).",
                "relative_to_root": "./",
                "sub_nav": [],
                "section_label": section_label,
                "section_slug": slug,
            },
        )
        (VULGARISATION_OUT_DIR / f"{slug}.html").write_text(html, encoding="utf-8")

    _copy_tree(VULGARISATION_ASSETS_SRC, VULGARISATION_ASSETS_OUT)

    print(
        f"[site] vulgarisation rendered: hub + {sum(len(s['pages']) for s in SECTIONS)} stratified pages + {len(TRANSVERSE_PAGES)} transverse."
    )

"""Page 6 — Sources & bibliographie."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from apps.basis_builder.paths import DATA_SOURCES_DIR
from apps.ui_streamlit.components import ethics_banner, loaders

st.set_page_config(page_title="6 — Sources", layout="wide")
ethics_banner.render()

st.title("Sources & bibliographie")

sources_md_path = DATA_SOURCES_DIR / "SOURCES.md"
if sources_md_path.exists():
    st.markdown(sources_md_path.read_text())
else:
    st.error("SOURCES.md introuvable.")

st.subheader("Bibliographie machine-lisible (taxonomie v2)")
taxonomy = loaders.load_taxonomy_v2()
for entry in taxonomy["bibliography"]:
    st.markdown(
        f"- **[{entry['id']}]** ({entry['type']}) {entry['citation']}"
        + (f" — _{entry['license']}_" if entry.get("license") else "")
        + (f" — [URL]({entry['url']})" if entry.get("url") else "")
    )

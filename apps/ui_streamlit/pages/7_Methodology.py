"""Page 7 — Méthodologie (docs/00..10)."""
from __future__ import annotations

import streamlit as st

from apps.basis_builder.paths import REPO_ROOT
from apps.ui_streamlit.components import ethics_banner

st.set_page_config(page_title="7 — Methodology", layout="wide")
ethics_banner.render()

st.title("Méthodologie")

docs_dir = REPO_ROOT / "docs"
doc_files = sorted(p for p in docs_dir.glob("*.md"))
if not doc_files:
    st.error("Aucun fichier docs/*.md trouvé.")
    st.stop()

selected = st.selectbox("Document", [p.name for p in doc_files])
selected_path = next(p for p in doc_files if p.name == selected)
st.markdown(selected_path.read_text())

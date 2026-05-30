"""Page 1 — B_doc : taxonomie hyper-détaillée."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from apps.ui_streamlit.components import ethics_banner, loaders

st.set_page_config(page_title="1 — Documentary Basis", layout="wide")
ethics_banner.render()

st.title("B_doc — Taxonomie hyper-détaillée")

taxonomy = loaders.load_taxonomy_v2()

st.markdown(f"**Version** `{taxonomy['version']}` — {len(taxonomy['civilizations'])} civilisations.")

selected_id = st.selectbox(
    "Civilisation",
    [civ["id"] for civ in taxonomy["civilizations"]],
)
civ = next(c for c in taxonomy["civilizations"] if c["id"] == selected_id)

st.subheader(f"{civ['label']} ({civ['id']})")
st.caption(civ["short_description"])
st.markdown(civ["long_description"])

col_a, col_b = st.columns(2)
col_a.metric("Étiquette Huntington", civ.get("huntington_label") or "—")
col_a.metric("Quadrant IW", civ.get("iw_quadrant") or "—")
col_b.metric("low_archetype_coverage", str(civ["low_archetype_coverage"]))
col_b.metric("extension_to_huntington", str(civ["extension_to_huntington"]))

st.markdown("### États membres")
if civ["member_states"]:
    st.dataframe(pd.DataFrame(civ["member_states"]), use_container_width=True)

st.markdown("### Sous-clusters")
if civ["sub_clusters"]:
    st.dataframe(pd.DataFrame(civ["sub_clusters"]), use_container_width=True)
else:
    st.info("Aucun sous-cluster.")

st.markdown("### Cas ambigus")
if civ["ambiguous_cases"]:
    st.dataframe(pd.DataFrame(civ["ambiguous_cases"]), use_container_width=True)
else:
    st.info("Aucun cas ambigu documenté.")

st.markdown("### Citations")
biblio_index = {entry["id"]: entry for entry in taxonomy["bibliography"]}
for citation_id in civ["citation_ids"]:
    entry = biblio_index.get(citation_id)
    if entry is None:
        st.error(f"Citation orpheline : {citation_id}")
    else:
        st.markdown(f"- **[{entry['id']}]** {entry['citation']}")

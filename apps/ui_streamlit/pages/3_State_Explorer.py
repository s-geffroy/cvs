"""Page 3 — explorateur d'un État."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from apps.ui_streamlit.components import charts, ethics_banner, loaders

st.set_page_config(page_title="3 — State Explorer", layout="wide")
ethics_banner.render()

st.title("Explorateur d'État")

state_payload = loaders.load_state_coordinates()
centroids_payload = loaders.load_centroids()
if state_payload is None or centroids_payload is None:
    st.warning("Bases non calculées. Lance `civvec basis build`.")
    st.stop()

states_index = {s["iso3"]: s for s in state_payload["states"]}
selected_iso3 = st.selectbox("ISO3", sorted(states_index.keys()), index=sorted(states_index.keys()).index("FRA") if "FRA" in states_index else 0)
state = states_index[selected_iso3]

col_left, col_right = st.columns(2)
with col_left:
    st.metric("x_viz [TS]", f"{state['x_viz'][0]:.2f}" if state['x_viz'][0] is not None else "—")
    st.metric("x_viz [SE]", f"{state['x_viz'][1]:.2f}" if state['x_viz'][1] is not None else "—")
with col_right:
    quality = state["data_quality"]
    st.write(f"**IW coverage** : {quality['iw_coverage']}")
    st.write(f"**Hofstede coverage** : {quality['hofstede_coverage']}")
    st.write(f"**low_evidence** : {quality['low_evidence']}")
    st.write(f"**Provenance x_viz** : `{quality.get('x_viz_provenance', '—')}`")
    st.write(f"**Provenance x_score** : `{quality.get('x_score_provenance', '—')}`")
    fallback_civilization = quality.get("fallback_civilization_id")
    if fallback_civilization:
        st.caption(f"Centroïde de repli : `{fallback_civilization}`")

st.markdown("### x_score (Hofstede 6D)")
score_table = pd.DataFrame(
    {
        "dimension": ["PDI", "IDV", "MAS", "UAI", "LTO", "IVR"],
        "value": state["x_score"],
    }
)
st.dataframe(score_table, use_container_width=True)

st.markdown("### Vecteur d'affinité civilisationnelle (dérivé)")
affinity_table = pd.DataFrame(
    sorted(state["affinity_vector"].items(), key=lambda x: -x[1]),
    columns=["civilization", "weight"],
)
st.dataframe(affinity_table, use_container_width=True)
st.bar_chart(affinity_table.set_index("civilization"))

st.markdown("### Radar Hofstede vs centroïdes top-3")
top_civilizations = affinity_table.head(3)["civilization"].tolist()
centroids_by_id = {c["civilization_id"]: c for c in centroids_payload["centroids"]}
items = [
    {"civilization_id": selected_iso3, "mu_score": state["x_score"]},
] + [
    {"civilization_id": civ_id, "mu_score": centroids_by_id[civ_id]["mu_score"]}
    for civ_id in top_civilizations
    if civ_id in centroids_by_id
]
st.plotly_chart(charts.radar_score(items), use_container_width=True)

st.markdown("### Evidence trace")
for ref in state.get("source_refs", []):
    st.markdown(f"- {ref}")

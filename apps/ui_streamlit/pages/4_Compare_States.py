"""Page 4 — comparaison de 2-5 États."""
from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from apps.ui_streamlit.components import charts, ethics_banner, loaders

st.set_page_config(page_title="4 — Compare States", layout="wide")
ethics_banner.render()

st.title("Comparaison d'États")

state_payload = loaders.load_state_coordinates()
if state_payload is None:
    st.warning("Bases non calculées. Lance `civvec basis build`.")
    st.stop()

states_index = {s["iso3"]: s for s in state_payload["states"]}
selected = st.multiselect(
    "ISO3 (2-5)",
    sorted(states_index.keys()),
    default=["FRA", "DEU", "JPN", "BRA"][: min(4, len(states_index))],
    max_selections=5,
)
if len(selected) < 2:
    st.info("Sélectionne au moins 2 États.")
    st.stop()

selected_states = [states_index[iso3] for iso3 in selected]

st.subheader("Radar B_score (Hofstede)")
items = [{"civilization_id": s["iso3"], "mu_score": s["x_score"]} for s in selected_states]
st.plotly_chart(charts.radar_score(items), use_container_width=True)

st.subheader("Tableau B_viz (Inglehart-Welzel)")
viz_table = pd.DataFrame(
    [{"iso3": s["iso3"], "TS": s["x_viz"][0], "SE": s["x_viz"][1]} for s in selected_states]
)
st.dataframe(viz_table, use_container_width=True)

st.subheader("Distances Euclidiennes dans B_score")
score_matrix = np.array([s["x_score"] for s in selected_states], dtype=float)
diff = score_matrix[:, None, :] - score_matrix[None, :, :]
distance_matrix = np.sqrt(np.nansum(diff ** 2, axis=-1))
st.plotly_chart(
    charts.heatmap(distance_matrix, [s["iso3"] for s in selected_states], "d_score^E"),
    use_container_width=True,
)

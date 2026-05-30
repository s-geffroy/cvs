"""Page 8 — Tensions internes : mécanique tensorielle."""
from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from apps.ui_streamlit.components import charts, ethics_banner, loaders

st.set_page_config(page_title="8 — State Tensions", layout="wide")
ethics_banner.render()

st.title("Tensions internes — mécanique tensorielle")

tensors_payload = loaders.load_state_tensors()
if tensors_payload is None:
    st.warning("Tenseurs non calculés. Lance `civvec basis build`.")
    st.stop()

tensions_index = {t["iso3"]: t for t in tensors_payload["tensions"]}
selected_iso3 = st.selectbox(
    "ISO3", sorted(tensions_index.keys()),
    index=sorted(tensions_index.keys()).index("FRA") if "FRA" in tensions_index else 0,
)
tension = tensions_index[selected_iso3]

col_a, col_b, col_c = st.columns(3)
col_a.metric("I1 (tension totale)", f"{tension['invariants']['I1']:.2f}")
col_b.metric("Anisotropie A", f"{tension['anisotropy']:.3f}")
col_c.metric("det(T)", f"{tension['invariants']['det']:.3e}")

st.subheader("Matrice T(s) (6×6, Hofstede axes)")
tension_matrix = np.array(tension["T"], dtype=float)
st.plotly_chart(
    charts.tensor_heatmap(tension_matrix, f"T({selected_iso3})"),
    use_container_width=True,
)

st.subheader("Eigenvalues (tensions principales)")
st.plotly_chart(
    charts.eigenvalues_bar(tension["eigenvalues"], "λ_1 ≥ ... ≥ λ_6"),
    use_container_width=True,
)

st.subheader("Directions propres (dominantes)")
eigenvectors = np.array(tension["eigenvectors"], dtype=float)
direction_table = pd.DataFrame(
    eigenvectors,
    index=["PDI", "IDV", "MAS", "UAI", "LTO", "IVR"],
    columns=[f"e_{i + 1}" for i in range(6)],
)
st.dataframe(direction_table, use_container_width=True)

st.subheader("Comparaison panel — anisotropie")
panel_anisotropy = pd.DataFrame(
    [{"iso3": t["iso3"], "anisotropy": t["anisotropy"]} for t in tensors_payload["tensions"]]
)
st.bar_chart(panel_anisotropy.set_index("iso3"))

"""Page 8 — Second moment civilisationnel M(s)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from apps.ui_streamlit.components import charts, ethics_banner, loaders

st.set_page_config(page_title="8 — Second moment M(s)", layout="wide")
ethics_banner.render()

st.title("Second moment civilisationnel M(s)")

moments_payload = loaders.load_state_moments()
if moments_payload is None:
    st.warning("Second moments non calculés. Lance `civvec basis build`.")
    st.stop()

moments_index = {entry["iso3"]: entry for entry in moments_payload["moments"]}
selected_iso3 = st.selectbox(
    "ISO3",
    sorted(moments_index.keys()),
    index=sorted(moments_index.keys()).index("FRA") if "FRA" in moments_index else 0,
)
moment_entry = moments_index[selected_iso3]

col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("I1 = tr(M)", f"{moment_entry['invariants']['I1_trace']:.2f}")
col_b.metric("I2 von Mises", f"{moment_entry['invariants']['I2_von_mises']:.2f}")
col_c.metric("Anisotropie A", f"{moment_entry['anisotropy']:.3f}")
col_d.metric("det(M)", f"{moment_entry['invariants']['det']:.3e}")

st.subheader("Matrice M(s) (6×6 sur axes Hofstede)")
moment_matrix = np.array(moment_entry["M"], dtype=float)
st.plotly_chart(
    charts.moment_heatmap(moment_matrix, f"M({selected_iso3})"),
    use_container_width=True,
)

st.subheader("Valeurs propres λ₁ ≥ … ≥ λ₆")
st.plotly_chart(
    charts.eigenvalues_bar(moment_entry["eigenvalues"], "Eigenvalues"),
    use_container_width=True,
)

st.subheader("Directions propres (eₖ dans B_score)")
eigenvectors = np.array(moment_entry["eigenvectors"], dtype=float)
direction_table = pd.DataFrame(
    eigenvectors,
    index=["PDI", "IDV", "MAS", "UAI", "LTO", "IVR"],
    columns=[f"e_{index + 1}" for index in range(6)],
)
st.dataframe(direction_table, use_container_width=True)

st.subheader("Décomposition M = Cov_w + biais (traces)")
decomposition_table = pd.DataFrame(
    [
        {
            "iso3": entry["iso3"],
            "trace_total": entry["invariants"]["I1_trace"],
            "trace_intra": entry["decomposition"]["trace_intra"],
            "trace_bias": entry["decomposition"]["trace_bias"],
        }
        for entry in moments_payload["moments"]
    ]
).set_index("iso3")
st.dataframe(decomposition_table.loc[[selected_iso3]], use_container_width=True)

st.subheader("Comparaison panel — anisotropie")
panel_anisotropy = pd.DataFrame(
    [{"iso3": entry["iso3"], "anisotropy": entry["anisotropy"]}
     for entry in moments_payload["moments"]]
)
st.bar_chart(panel_anisotropy.set_index("iso3"))

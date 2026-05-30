"""Page 9 — Algèbre des distances civilisationnelles."""
from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from packages.civvec_core.algebra.distances import (
    HybridWeights,
    civilization_ground_cost_squared,
    d_hybrid,
    d_score_euclidean,
    d_score_mahalanobis,
    d_T_frobenius,
    d_viz,
    d_w_cosine,
    d_w_js,
    d_w_wasserstein,
    weighted_covariance_inverse,
)
from apps.ui_streamlit.components import charts, ethics_banner, loaders

st.set_page_config(page_title="9 — Distance Algebra", layout="wide")
ethics_banner.render()

st.title("Algèbre des distances")

state_payload = loaders.load_state_coordinates()
centroids_payload = loaders.load_centroids()
tensors_payload = loaders.load_state_tensors()
if state_payload is None or centroids_payload is None:
    st.warning("Bases non calculées. Lance `civvec basis build`.")
    st.stop()

states_by_iso3 = {s["iso3"]: s for s in state_payload["states"]}
tensions_by_iso3 = (
    {t["iso3"]: t for t in tensors_payload["tensions"]} if tensors_payload else {}
)
civilization_ids_order = [c["civilization_id"] for c in centroids_payload["centroids"]]
mu_score_matrix = np.array(
    [
        [v if v is not None else 50.0 for v in c["mu_score"]]
        for c in centroids_payload["centroids"]
    ]
)
ground_cost_squared = civilization_ground_cost_squared(mu_score_matrix)
covariance_inverse = weighted_covariance_inverse(mu_score_matrix)

selected = st.multiselect(
    "ISO3 (2-10)",
    sorted(states_by_iso3.keys()),
    default=["FRA", "DEU", "JPN", "BRA", "RUS"][: min(5, len(states_by_iso3))],
    max_selections=10,
)
if len(selected) < 2:
    st.info("Sélectionne au moins 2 États.")
    st.stop()

col_alpha, col_beta, col_gamma = st.columns(3)
alpha = col_alpha.slider("α (Mahalanobis)", 0.0, 1.0, 0.4, 0.05)
beta = col_beta.slider("β (Wasserstein)", 0.0, 1.0, 0.4, 0.05)
gamma_raw = max(0.0, 1.0 - alpha - beta)
col_gamma.metric("γ (Frobenius)", f"{gamma_raw:.2f}")

if not np.isclose(alpha + beta + gamma_raw, 1.0):
    st.warning("Re-normalisation auto pour α + β + γ = 1.")
total = alpha + beta + gamma_raw
weights = HybridWeights(
    alpha=alpha / total, beta=beta / total, gamma=gamma_raw / total
)

st.subheader("Toutes les distances par paire")
pairs: list[dict[str, float | str]] = []
for source in selected:
    for target in selected:
        if source >= target:
            continue
        state_source = states_by_iso3[source]
        state_target = states_by_iso3[target]
        x_viz_s = np.array(state_source["x_viz"], dtype=float)
        x_viz_t = np.array(state_target["x_viz"], dtype=float)
        x_score_s = np.array(state_source["x_score"], dtype=float)
        x_score_t = np.array(state_target["x_score"], dtype=float)
        weights_source = np.array(
            [state_source["affinity_vector"][cid] for cid in civilization_ids_order]
        )
        weights_target = np.array(
            [state_target["affinity_vector"][cid] for cid in civilization_ids_order]
        )

        d_score_mahalanobis_value = d_score_mahalanobis(
            x_score_s, x_score_t, covariance_inverse
        )
        d_w_wasserstein_value = d_w_wasserstein(
            weights_source, weights_target, ground_cost_squared
        )
        tensor_source = np.array(tensions_by_iso3[source]["T"]) if source in tensions_by_iso3 else np.zeros((6, 6))
        tensor_target = np.array(tensions_by_iso3[target]["T"]) if target in tensions_by_iso3 else np.zeros((6, 6))
        d_T_value = d_T_frobenius(tensor_source, tensor_target)

        pairs.append(
            {
                "pair": f"{source}-{target}",
                "d_viz": d_viz(x_viz_s, x_viz_t),
                "d_score_E": d_score_euclidean(x_score_s, x_score_t),
                "d_score_M": d_score_mahalanobis_value,
                "d_w_cos": d_w_cosine(weights_source, weights_target),
                "d_w_JS": d_w_js(weights_source, weights_target),
                "d_w_W": d_w_wasserstein_value,
                "d_T": d_T_value,
                "d_hyb": d_hybrid(
                    d_score_mahalanobis_value, d_w_wasserstein_value, d_T_value, weights
                ),
            }
        )

st.dataframe(pd.DataFrame(pairs), use_container_width=True)

st.subheader("Heatmap — d_hyb")
n = len(selected)
distance_matrix = np.zeros((n, n))
for entry in pairs:
    source, target = entry["pair"].split("-")
    i, j = selected.index(source), selected.index(target)
    distance_matrix[i, j] = entry["d_hyb"]
    distance_matrix[j, i] = entry["d_hyb"]
st.plotly_chart(
    charts.heatmap(distance_matrix, selected, "d_hyb"),
    use_container_width=True,
)

if len(selected) >= 3:
    st.subheader("Dendrogramme Ward sur d_hyb")
    st.plotly_chart(
        charts.dendrogram_from_condensed(distance_matrix, selected, "Clustering hiérarchique"),
        use_container_width=True,
    )

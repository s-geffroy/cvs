"""Page 9 — Algèbre des distances civilisationnelles (v3.0)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from packages.civvec_core.algebra.distances import (
    HybridWeights,
    civilization_ground_cost_squared,
    d_hybrid,
    d_M_frobenius,
    d_score_euclidean,
    d_score_mahalanobis_centroids,
    d_score_mahalanobis_intra,
    d_viz,
    d_w_cosine,
    d_w_js,
    d_w_wasserstein,
    intra_civilizational_covariance_inverse,
    weighted_centroid_covariance_inverse,
)
from apps.ui_streamlit.components import charts, ethics_banner, loaders

st.set_page_config(page_title="9 — Distance Algebra", layout="wide")
ethics_banner.render()

st.title("Algèbre des distances")

st.info(
    "ℹ️ Les coordonnées d'origine peuvent être `observed`, `imputed_wvs_items`, "
    "`imputed_pew` ou `imputed_governance` (cf. [doc 16](../methodology/16_imputation_cascade/)). "
    "Les distances calculées sont valides sur n'importe quel tier, mais leur interprétation "
    "doit tenir compte de la provenance : deux États tous deux observés produisent une distance "
    "directement comparable à la littérature ; un État imputé voit son ellipse d'incertitude "
    "déjà gonflée — la distance reste finie, mais son RMSE de calibration s'ajoute."
)

state_payload = loaders.load_state_coordinates()
centroids_payload = loaders.load_centroids()
moments_payload = loaders.load_state_moments()
if state_payload is None or centroids_payload is None:
    st.warning("Bases non calculées. Lance `civvec basis build`.")
    st.stop()

states_by_iso3 = {entry["iso3"]: entry for entry in state_payload["states"]}
moments_by_iso3 = (
    {entry["iso3"]: entry for entry in moments_payload["moments"]}
    if moments_payload
    else {}
)
civilization_ids_order = [centroid["civilization_id"] for centroid in centroids_payload["centroids"]]
mu_score_matrix = np.array(
    [
        [value if value is not None else 50.0 for value in centroid["mu_score"]]
        for centroid in centroids_payload["centroids"]
    ]
)
sigma_score_matrix = np.array(
    [
        [value if value is not None else 0.0 for value in centroid.get("sigma_score", [0.0] * 6)]
        for centroid in centroids_payload["centroids"]
    ]
)
ground_cost_squared = civilization_ground_cost_squared(mu_score_matrix)
covariance_inverse_centroids = weighted_centroid_covariance_inverse(mu_score_matrix)
covariance_inverse_intra = intra_civilizational_covariance_inverse(sigma_score_matrix)

selected_iso3s = st.multiselect(
    "ISO3 (2-10)",
    sorted(states_by_iso3.keys()),
    default=["FRA", "DEU", "JPN", "BRA", "RUS"][: min(5, len(states_by_iso3))],
    max_selections=10,
)
if len(selected_iso3s) < 2:
    st.info("Sélectionne au moins 2 États.")
    st.stop()

col_alpha, col_beta, col_gamma = st.columns(3)
alpha_weight = col_alpha.slider("α (Mahalanobis intra)", 0.0, 1.0, 0.4, 0.05)
beta_weight = col_beta.slider("β (Wasserstein)", 0.0, 1.0, 0.4, 0.05)
gamma_weight_raw = max(0.0, 1.0 - alpha_weight - beta_weight)
col_gamma.metric("γ (Frobenius M)", f"{gamma_weight_raw:.2f}")

if not np.isclose(alpha_weight + beta_weight + gamma_weight_raw, 1.0):
    st.warning("Re-normalisation auto pour α + β + γ = 1.")
total_weight = alpha_weight + beta_weight + gamma_weight_raw
hybrid_weights = HybridWeights(
    alpha=alpha_weight / total_weight,
    beta=beta_weight / total_weight,
    gamma=gamma_weight_raw / total_weight,
)

st.subheader("Toutes les distances par paire")
pair_rows: list[dict[str, float | str]] = []
for source_iso3 in selected_iso3s:
    for target_iso3 in selected_iso3s:
        if source_iso3 >= target_iso3:
            continue
        state_source = states_by_iso3[source_iso3]
        state_target = states_by_iso3[target_iso3]
        x_viz_source = np.array(state_source["x_viz"], dtype=float)
        x_viz_target = np.array(state_target["x_viz"], dtype=float)
        x_score_source = np.array(state_source["x_score"], dtype=float)
        x_score_target = np.array(state_target["x_score"], dtype=float)
        affinity_source = np.array(
            [state_source["affinity_vector"][civ_id] for civ_id in civilization_ids_order]
        )
        affinity_target = np.array(
            [state_target["affinity_vector"][civ_id] for civ_id in civilization_ids_order]
        )

        d_score_mahalanobis_centroids_value = d_score_mahalanobis_centroids(
            x_score_source, x_score_target, covariance_inverse_centroids
        )
        d_score_mahalanobis_intra_value = d_score_mahalanobis_intra(
            x_score_source, x_score_target, covariance_inverse_intra
        )
        d_w_wasserstein_value = d_w_wasserstein(
            affinity_source, affinity_target, ground_cost_squared
        )
        moment_source = (
            np.array(moments_by_iso3[source_iso3]["M"])
            if source_iso3 in moments_by_iso3
            else np.zeros((6, 6))
        )
        moment_target = (
            np.array(moments_by_iso3[target_iso3]["M"])
            if target_iso3 in moments_by_iso3
            else np.zeros((6, 6))
        )
        d_M_frobenius_value = d_M_frobenius(moment_source, moment_target)

        source_provenance = state_source.get("data_quality", {}).get(
            "x_viz_provenance", "—"
        )
        target_provenance = state_target.get("data_quality", {}).get(
            "x_viz_provenance", "—"
        )
        pair_rows.append(
            {
                "pair": f"{source_iso3}-{target_iso3}",
                "provenance": f"{source_provenance} / {target_provenance}",
                "d_viz": d_viz(x_viz_source, x_viz_target),
                "d_score_E": d_score_euclidean(x_score_source, x_score_target),
                "d_score_M_intra": d_score_mahalanobis_intra_value,
                "d_score_M_centroids": d_score_mahalanobis_centroids_value,
                "d_w_cos": d_w_cosine(affinity_source, affinity_target),
                "d_w_JS": d_w_js(affinity_source, affinity_target),
                "d_w_W": d_w_wasserstein_value,
                "d_M_F": d_M_frobenius_value,
                "d_hyb": d_hybrid(
                    d_score_mahalanobis_intra_value,
                    d_w_wasserstein_value,
                    d_M_frobenius_value,
                    hybrid_weights,
                ),
            }
        )

st.dataframe(pd.DataFrame(pair_rows), use_container_width=True)

st.subheader("Heatmap — d_hyb")
n_selected = len(selected_iso3s)
distance_matrix = np.zeros((n_selected, n_selected))
for row in pair_rows:
    source_iso3, target_iso3 = row["pair"].split("-")
    left_index, right_index = selected_iso3s.index(source_iso3), selected_iso3s.index(target_iso3)
    distance_matrix[left_index, right_index] = row["d_hyb"]
    distance_matrix[right_index, left_index] = row["d_hyb"]
st.plotly_chart(
    charts.heatmap(distance_matrix, selected_iso3s, "d_hyb"),
    use_container_width=True,
)

if len(selected_iso3s) >= 3:
    st.subheader("Dendrogramme Ward sur d_hyb")
    st.plotly_chart(
        charts.dendrogram_from_condensed(distance_matrix, selected_iso3s, "Clustering hiérarchique"),
        use_container_width=True,
    )

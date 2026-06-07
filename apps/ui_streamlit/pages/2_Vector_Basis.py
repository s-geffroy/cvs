"""Page 2 — B_vec : scatter IW 2D + radars Hofstede 6D."""
from __future__ import annotations

import numpy as np
import streamlit as st

from apps.ui_streamlit.components import charts, ethics_banner, loaders

st.set_page_config(page_title="2 — Vector Basis", layout="wide")
ethics_banner.render()

st.title("B_vec — Espace vectoriel civilisationnel")

centroids_payload = loaders.load_centroids()
state_coords_payload = loaders.load_state_coordinates()

if centroids_payload is None:
    st.warning("Centroïdes non calculés. Lance `docker compose run --rm civvec_ui civvec basis build`.")
    st.stop()

centroids = centroids_payload["centroids"]
state_coords = state_coords_payload["states"] if state_coords_payload else []

st.subheader("B_viz = ℝ² (Inglehart-Welzel)")
provenance_filter = st.multiselect(
    "Filtrer par provenance des coordonnées x_viz",
    options=[
        "observed",
        "imputed_wvs_items",
        "imputed_pew",
        "centroid_prior",
    ],
    default=["observed", "imputed_wvs_items", "imputed_pew", "centroid_prior"],
    help=(
        "Provenance tier de la cascade. `observed` = WVS wave-7 officiel. "
        "`imputed_wvs_items` = WVS waves 5-6 prédit par ridge. "
        "`imputed_pew` = composition religieuse Pew + UNDP HDR + UN voting + V-Dem. "
        "`centroid_prior` = barycentre civilisationnel. Cf. doc 16."
    ),
)
filtered_state_coords = [
    state
    for state in state_coords
    if state.get("data_quality", {}).get("x_viz_provenance") in provenance_filter
]
st.caption(
    f"Affichés : {len(filtered_state_coords)} / {len(state_coords)} États selon la sélection."
)
st.plotly_chart(
    charts.scatter_viz(centroids, filtered_state_coords),
    use_container_width=True,
)

st.subheader("B_score = ℝ⁶ (Hofstede)")
selected_civilization_ids = st.multiselect(
    "Civilisations à afficher",
    [c["civilization_id"] for c in centroids],
    default=[c["civilization_id"] for c in centroids[:4]],
)
filtered_centroids = [c for c in centroids if c["civilization_id"] in selected_civilization_ids]
st.plotly_chart(
    charts.radar_score(filtered_centroids),
    use_container_width=True,
)

st.subheader("Distances inter-civilisations dans B_score")
labels = [c["civilization_id"] for c in centroids]
mu_matrix = np.array(
    [[v if v is not None else np.nan for v in c["mu_score"]] for c in centroids]
)
diff = mu_matrix[:, None, :] - mu_matrix[None, :, :]
distance_matrix = np.sqrt(np.nansum(diff ** 2, axis=-1))
st.plotly_chart(
    charts.heatmap(distance_matrix, labels, title="d_score^E entre centroïdes"),
    use_container_width=True,
)

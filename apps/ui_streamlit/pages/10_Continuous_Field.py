"""Page 10 — Champ civilisationnel continu (V2 : multi-output, grille 1°).

Sélecteur sur les 19 composantes (TS, SE, 6 Hofstede, 11 affinités).
Affiche la valeur prédite μ, la magnitude du gradient (fault lines),
l'écart-type prédictif σ et un quiver des vecteurs gradient.

Source data : ``packages/civvec_core/basis/continuous_field_v2_meta.json``
(metadata) + ``..._arrays.npz`` (arrays compressed). Produced by
``apps/basis_builder/field/train_v2.py``.
"""
from __future__ import annotations

import json

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from apps.basis_builder.paths import BASIS_DIR
from apps.ui_streamlit.components import ethics_banner

CONTINUOUS_FIELD_V2_META_PATH = BASIS_DIR / "continuous_field_v2_meta.json"
CONTINUOUS_FIELD_V2_ARRAYS_PATH = BASIS_DIR / "continuous_field_v2_arrays.npz"

st.set_page_config(page_title="10 — Continuous Field V2", layout="wide")
ethics_banner.render()

st.title("Champ civilisationnel continu sur la sphère — V2")

st.markdown(
    "Représentation **sans frontière d'État**. Un Gaussian Process à kernel "
    "Matérn 3/2 sur grand-cercle interpole les coordonnées d'État (placées "
    "à leur centroïde pondéré par population) en un champ continu "
    "interrogeable à tout `(λ, φ)`. La dérivée `(∂μ/∂λ, ∂μ/∂φ)` est calculée "
    "analytiquement et validée par tests de différence finie. "
    "Cf. [doc 17](../methodology/17_continuous_field/)."
)


@st.cache_resource
def _load_v2_field():
    if not CONTINUOUS_FIELD_V2_META_PATH.exists():
        return None, None
    meta = json.loads(CONTINUOUS_FIELD_V2_META_PATH.read_text())
    arrays_data = np.load(CONTINUOUS_FIELD_V2_ARRAYS_PATH)
    return meta, arrays_data


metadata_payload, arrays_archive = _load_v2_field()

if metadata_payload is None:
    st.warning(
        "Le champ V2 n'a pas encore été calculé. Lance dans Docker :\n\n"
        "`python -m apps.basis_builder.field.train_v2`"
    )
    st.stop()

grid_longitudes_deg = np.array(metadata_payload["grid"]["longitudes_deg"])
grid_latitudes_deg = np.array(metadata_payload["grid"]["latitudes_deg"])
component_names = metadata_payload["_meta"]["component_names"]
hyperparameters = metadata_payload["_meta"]["hyperparameters"]

col_meta_left, col_meta_right = st.columns(2)
with col_meta_left:
    st.metric("Points d'entraînement", metadata_payload["_meta"]["n_training_points"])
    st.metric("Composantes", metadata_payload["_meta"]["n_components"])
with col_meta_right:
    st.metric(
        "Length scale (rad)",
        f"{hyperparameters['length_scale_rad']:.3f}",
        help=f"≈ {hyperparameters['length_scale_km_earth']:.0f} km sur Terre — optimisée par ML",
    )
    st.metric(
        "NLML",
        f"{hyperparameters.get('negative_log_marginal_likelihood', float('nan')):.0f}",
        help="Négative log marginal likelihood au minimum trouvé",
    )

component_label_groups = {
    "Inglehart-Welzel (B_viz)": [c for c in component_names if c.startswith("x_viz_")],
    "Hofstede (B_score)": [c for c in component_names if c.startswith("x_score_")],
    "Affinités civilisationnelles (Δ¹⁰)": [
        c for c in component_names if c.startswith("affinity_")
    ],
}
component_display_options: list[str] = []
for group_label, components_in_group in component_label_groups.items():
    component_display_options.extend(components_in_group)

selected_component = st.selectbox(
    "Composante à visualiser",
    options=component_display_options,
    format_func=lambda x: x.replace("_", " "),
)

display_mode = st.radio(
    "Quoi afficher ?",
    options=[
        "Valeur prédite μ",
        "Magnitude du gradient ‖∇μ‖ (fault lines)",
        "Écart-type prédictif σ",
    ],
    horizontal=True,
)

predicted_mean = arrays_archive[f"{selected_component}__predicted_mean"]
gradient_magnitude = arrays_archive[f"{selected_component}__gradient_magnitude"]
gradient_longitude = arrays_archive[f"{selected_component}__gradient_longitude"]
gradient_latitude = arrays_archive[f"{selected_component}__gradient_latitude"]
predicted_variance = arrays_archive["predicted_variance"]

if display_mode == "Valeur prédite μ":
    z_values = predicted_mean
    color_scale = "RdBu_r"
    colorbar_title = f"{selected_component} prédit"
elif display_mode == "Magnitude du gradient ‖∇μ‖ (fault lines)":
    z_values = gradient_magnitude
    color_scale = "Plasma"
    colorbar_title = "‖∇μ‖ par radian"
else:
    z_values = np.sqrt(predicted_variance)
    color_scale = "Cividis"
    colorbar_title = "σ prédictif"

heatmap_figure = go.Figure(
    data=go.Heatmap(
        x=grid_longitudes_deg,
        y=grid_latitudes_deg,
        z=z_values,
        colorscale=color_scale,
        colorbar={"title": colorbar_title},
        connectgaps=False,
    )
)
heatmap_figure.update_layout(
    xaxis_title="Longitude (°)",
    yaxis_title="Latitude (°)",
    height=520,
    margin={"l": 10, "r": 10, "t": 30, "b": 10},
    title=f"{display_mode} — {selected_component}",
)
st.plotly_chart(heatmap_figure, use_container_width=True)

st.subheader("Champ de vecteurs gradient (quiver)")
quiver_subsample = st.slider(
    "Densité des flèches (1 = grille complète, 12 = 1 cellule sur 12)",
    min_value=4,
    max_value=18,
    value=10,
)

quiver_longitudes = grid_longitudes_deg[::quiver_subsample]
quiver_latitudes = grid_latitudes_deg[::quiver_subsample]
quiver_grad_longitude = gradient_longitude[::quiver_subsample, ::quiver_subsample]
quiver_grad_latitude = gradient_latitude[::quiver_subsample, ::quiver_subsample]

quiver_mesh_x, quiver_mesh_y = np.meshgrid(quiver_longitudes, quiver_latitudes)
arrow_scale = float(quiver_subsample)
quiver_traces = []
for i in range(quiver_mesh_x.shape[0]):
    for j in range(quiver_mesh_x.shape[1]):
        gx = float(quiver_grad_longitude[i, j])
        gy = float(quiver_grad_latitude[i, j])
        if not np.isfinite(gx) or not np.isfinite(gy):
            continue
        norm = float(np.hypot(gx, gy))
        if norm < 1e-3:
            continue
        scale_factor = arrow_scale / max(norm, 1e-3) * min(norm, 6.0)
        quiver_traces.append(
            go.Scatter(
                x=[
                    float(quiver_mesh_x[i, j]),
                    float(quiver_mesh_x[i, j] + gx * scale_factor / norm),
                ],
                y=[
                    float(quiver_mesh_y[i, j]),
                    float(quiver_mesh_y[i, j] + gy * scale_factor / norm),
                ],
                mode="lines",
                line={"color": "rgba(20,20,20,0.45)", "width": 0.6},
                showlegend=False,
                hoverinfo="skip",
            )
        )

quiver_figure = go.Figure(data=quiver_traces)
quiver_figure.update_layout(
    xaxis_title="Longitude (°)",
    yaxis_title="Latitude (°)",
    xaxis={"range": [-180, 180]},
    yaxis={"range": [-90, 90]},
    height=520,
    margin={"l": 10, "r": 10, "t": 30, "b": 10},
    title=f"Vecteurs gradient — {selected_component}",
)
st.plotly_chart(quiver_figure, use_container_width=True)

with st.expander("Hyperparamètres et provenance noise"):
    st.json(metadata_payload["_meta"]["hyperparameters"])
    st.write(
        "**Provenance → noise** : chaque sample point porte un bruit GP "
        "calibré sur la provenance de l'État correspondant. Les `observed` "
        "ont un poids fort, les `centroid_prior` agissent comme anchors "
        "doux. Le multiplicateur global est optimisé par maximum de "
        "marginal likelihood."
    )
    st.json(metadata_payload["_meta"]["provenance_base_noise"])

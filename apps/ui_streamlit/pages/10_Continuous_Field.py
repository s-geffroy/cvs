"""Page 10 — Champ civilisationnel continu sur la sphère (prototype TS).

Visualise:
- la valeur prédite μ(λ, φ) du Gaussian Process pour la composante TS
  (Inglehart-Welzel Traditional ↔ Secular-Rational) ;
- la magnitude du gradient ‖∇μ‖ (fault lines de Huntington) ;
- les vecteurs gradient sous forme de flèches (quiver).
"""
from __future__ import annotations

import json

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from apps.basis_builder.paths import BASIS_DIR
from apps.ui_streamlit.components import ethics_banner

CONTINUOUS_FIELD_TS_PATH = BASIS_DIR / "continuous_field_ts.json"

st.set_page_config(page_title="10 — Continuous Field", layout="wide")
ethics_banner.render()

st.title("Champ civilisationnel continu sur la sphère — prototype TS")

st.markdown(
    "Cette page abandonne la représentation par État pour montrer le champ "
    "**continu** `μ(λ, φ)` interpolé par un Gaussian Process (kernel Matérn 3/2 "
    "sur grand-cercle) à partir des coordonnées d'État. La dérivée `(∂μ/∂λ, ∂μ/∂φ)` "
    "est calculée analytiquement et validée contre une différence finie. "
    "Cf. [`docs/17_continuous_field.md`](../methodology/17_continuous_field/) "
    "pour la méthodologie complète."
)

if not CONTINUOUS_FIELD_TS_PATH.exists():
    st.warning(
        "Le champ continu n'a pas encore été calculé. Lance dans Docker :\n\n"
        "`python -m apps.basis_builder.field.train_prototype`"
    )
    st.stop()

payload = json.loads(CONTINUOUS_FIELD_TS_PATH.read_text())
grid_longitudes_deg = np.array(payload["grid"]["longitudes_deg"])
grid_latitudes_deg = np.array(payload["grid"]["latitudes_deg"])
predicted_mean = np.array(payload["predicted_mean_ts"])
predicted_variance = np.array(payload["predicted_variance_ts"])
gradient_longitude = np.array(payload["gradient_longitude_ts"])
gradient_latitude = np.array(payload["gradient_latitude_ts"])
gradient_magnitude = np.array(payload["gradient_magnitude_ts"])

meta = payload["_meta"]
col_meta_left, col_meta_right = st.columns(2)
with col_meta_left:
    st.metric("Points d'entraînement", meta["n_training_points"])
    st.metric("Cellules de grille", predicted_mean.size)
with col_meta_right:
    st.metric(
        "Length scale (rad)",
        f"{meta['length_scale_rad']:.3f}",
        help=f"≈ {meta['length_scale_km_earth_equivalent']:.0f} km sur Terre",
    )
    st.metric("Pas de grille", f"{meta['grid_step_deg']}°")

display_mode = st.radio(
    "Quoi afficher ?",
    options=[
        "Valeur prédite μ(λ, φ)",
        "Magnitude du gradient ‖∇μ‖ (fault lines)",
        "Écart-type prédictif σ(λ, φ)",
    ],
    horizontal=True,
)

if display_mode == "Valeur prédite μ(λ, φ)":
    z_values = predicted_mean
    color_scale = "RdBu_r"
    colorbar_title = "TS prédit"
elif display_mode == "Magnitude du gradient ‖∇μ‖ (fault lines)":
    z_values = gradient_magnitude
    color_scale = "Plasma"
    colorbar_title = "‖∇μ‖ (unités TS / rad)"
else:
    z_values = np.sqrt(predicted_variance)
    color_scale = "Cividis"
    colorbar_title = "σ prédictif"

heatmap = go.Figure(
    data=go.Heatmap(
        x=grid_longitudes_deg,
        y=grid_latitudes_deg,
        z=z_values,
        colorscale=color_scale,
        colorbar={"title": colorbar_title},
        connectgaps=False,
    )
)
heatmap.update_layout(
    xaxis_title="Longitude (°)",
    yaxis_title="Latitude (°)",
    height=500,
    margin={"l": 10, "r": 10, "t": 30, "b": 10},
    title=display_mode,
)
st.plotly_chart(heatmap, use_container_width=True)

st.subheader("Champ de vecteurs gradient (quiver)")

quiver_density = st.slider(
    "Densité des flèches (1 = toutes les cellules, 4 = 1 cellule sur 4)",
    min_value=1,
    max_value=6,
    value=2,
)

quiver_longitudes = grid_longitudes_deg[::quiver_density]
quiver_latitudes = grid_latitudes_deg[::quiver_density]
quiver_grad_longitude = gradient_longitude[::quiver_density, ::quiver_density]
quiver_grad_latitude = gradient_latitude[::quiver_density, ::quiver_density]

quiver_mesh_x, quiver_mesh_y = np.meshgrid(quiver_longitudes, quiver_latitudes)
arrow_scale = 4.0
quiver_traces = []
for i in range(quiver_mesh_x.shape[0]):
    for j in range(quiver_mesh_x.shape[1]):
        gx = quiver_grad_longitude[i, j]
        gy = quiver_grad_latitude[i, j]
        if not np.isfinite(gx) or not np.isfinite(gy):
            continue
        norm = np.hypot(gx, gy)
        if norm < 1e-3:
            continue
        scale_factor = arrow_scale / max(norm, 1e-3) * min(norm, 8.0)
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
                line={"color": "rgba(20,20,20,0.55)", "width": 0.6},
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
    height=500,
    margin={"l": 10, "r": 10, "t": 30, "b": 10},
    title="Vecteurs gradient (∂μ/∂λ, ∂μ/∂φ) — direction où TS croît",
)
st.plotly_chart(quiver_figure, use_container_width=True)

st.markdown(
    "**Lecture des fault lines** : la magnitude du gradient pointe les "
    "transitions civilisationnelles abruptes. À ~35-40°N, 0-15°E (Méditerranée "
    "sud) correspond la frontière Maghreb islamique ↔ Europe latine ; à ~55-60°N, "
    "15-20°E (mer Baltique) la frontière catholique ↔ orthodoxe. Ces zones sont "
    "celles de Huntington (1996) — mais ici **émergentes du data, pas postulées**."
)

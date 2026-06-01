"""Plotly chart helpers used across pages."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
from scipy.cluster.hierarchy import dendrogram, linkage

HOFSTEDE_AXES = ("PDI", "IDV", "MAS", "UAI", "LTO", "IVR")


def scatter_viz(
    civilization_centroids: list[dict],
    state_points: list[dict] | None = None,
) -> go.Figure:
    """Inglehart-Welzel 2D scatter with civilization centroids + optional state points."""
    figure = go.Figure()
    for centroid in civilization_centroids:
        mu = centroid.get("mu_viz")
        if mu is None or any(v is None for v in mu):
            continue
        figure.add_trace(
            go.Scatter(
                x=[mu[0]],
                y=[mu[1]],
                mode="markers+text",
                text=[centroid["civilization_id"]],
                textposition="top center",
                marker={"size": 16, "symbol": "diamond"},
                name=centroid["civilization_id"],
            )
        )
    if state_points:
        figure.add_trace(
            go.Scatter(
                x=[s["x_viz"][0] for s in state_points if s["x_viz"][0] is not None],
                y=[s["x_viz"][1] for s in state_points if s["x_viz"][1] is not None],
                mode="markers+text",
                text=[s["iso3"] for s in state_points if s["x_viz"][0] is not None],
                textposition="bottom center",
                marker={"size": 6, "color": "rgba(50,50,50,0.5)"},
                name="states",
            )
        )
    figure.update_layout(
        xaxis_title="Traditional ↔ Secular-Rational",
        yaxis_title="Survival ↔ Self-Expression",
        height=600,
        showlegend=False,
    )
    figure.update_xaxes(range=[-2.5, 2.5], zeroline=True)
    figure.update_yaxes(range=[-2.5, 2.5], zeroline=True)
    return figure


def radar_score(
    items: list[dict], value_key: str = "mu_score", label_key: str = "civilization_id"
) -> go.Figure:
    """Radar chart over Hofstede 6 dimensions."""
    figure = go.Figure()
    for item in items:
        values = item.get(value_key)
        if values is None or any(v is None for v in values):
            continue
        figure.add_trace(
            go.Scatterpolar(
                r=list(values) + [values[0]],
                theta=list(HOFSTEDE_AXES) + [HOFSTEDE_AXES[0]],
                fill="toself",
                name=str(item.get(label_key)),
            )
        )
    figure.update_layout(
        polar={"radialaxis": {"range": [0, 100]}},
        height=550,
        showlegend=True,
    )
    return figure


def heatmap(matrix: np.ndarray, labels: list[str], title: str = "") -> go.Figure:
    figure = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=labels,
            y=labels,
            colorscale="Viridis",
        )
    )
    figure.update_layout(title=title, height=600)
    return figure


def moment_heatmap(moment_matrix: np.ndarray, title: str = "") -> go.Figure:
    """6x6 heatmap of the civilizational second moment M(s) over Hofstede axes."""
    figure = go.Figure(
        data=go.Heatmap(
            z=moment_matrix,
            x=list(HOFSTEDE_AXES),
            y=list(HOFSTEDE_AXES),
            colorscale="RdBu_r",
            zmid=0,
        )
    )
    figure.update_layout(title=title, height=500)
    return figure


def eigenvalues_bar(eigenvalues: list[float], title: str = "") -> go.Figure:
    figure = go.Figure(
        data=go.Bar(
            x=[f"λ_{index + 1}" for index in range(len(eigenvalues))],
            y=eigenvalues,
        )
    )
    figure.update_layout(title=title, height=350, yaxis_title="valeur propre λₖ")
    return figure


def dendrogram_from_condensed(
    distance_matrix: np.ndarray, labels: list[str], title: str = ""
) -> go.Figure:
    from scipy.spatial.distance import squareform

    condensed = squareform(distance_matrix, checks=False)
    linkage_matrix = linkage(condensed, method="ward")
    tree = dendrogram(linkage_matrix, labels=labels, no_plot=True)
    figure = go.Figure()
    icoord = np.array(tree["icoord"])
    dcoord = np.array(tree["dcoord"])
    for x_coords, y_coords in zip(icoord, dcoord):
        figure.add_trace(
            go.Scatter(
                x=x_coords,
                y=y_coords,
                mode="lines",
                line={"color": "rgb(80,80,80)"},
                showlegend=False,
            )
        )
    leaf_positions = np.arange(5, len(tree["ivl"]) * 10 + 5, 10)
    figure.update_layout(
        title=title,
        height=500,
        xaxis={
            "tickmode": "array",
            "tickvals": leaf_positions,
            "ticktext": tree["ivl"],
        },
        yaxis={"title": "distance"},
    )
    return figure

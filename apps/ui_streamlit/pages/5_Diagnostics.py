"""Page 5 — Diagnostics santé des bases."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from apps.ui_streamlit.components import ethics_banner, loaders

st.set_page_config(page_title="5 — Diagnostics", layout="wide")
ethics_banner.render()

st.title("Diagnostics des bases")

taxonomy = loaders.load_taxonomy_v2()
state_payload = loaders.load_state_coordinates()
centroids_payload = loaders.load_centroids()

st.subheader("Couverture par État (cascade d'imputation)")
if state_payload:
    rows = [
        {
            "iso3": state["iso3"],
            "iw_coverage": state["data_quality"]["iw_coverage"],
            "hofstede_coverage": state["data_quality"]["hofstede_coverage"],
            "low_evidence": state["data_quality"]["low_evidence"],
            "x_viz_provenance": state["data_quality"].get("x_viz_provenance", "—"),
            "x_score_provenance": state["data_quality"].get("x_score_provenance", "—"),
        }
        for state in state_payload["states"]
    ]
    df_coverage = pd.DataFrame(rows)
    st.dataframe(df_coverage, use_container_width=True)
    st.caption(
        "Tiers de la cascade : `observed` > `imputed_wvs_items` > `imputed_pew` > "
        "`imputed_governance` > `centroid_prior`. Cf. `docs/16_imputation_cascade.md`."
    )
    summary_cols = st.columns(2)
    with summary_cols[0]:
        st.markdown("**Distribution provenance `x_viz`**")
        st.bar_chart(df_coverage["x_viz_provenance"].value_counts())
    with summary_cols[1]:
        st.markdown("**Distribution provenance `x_score`**")
        st.bar_chart(df_coverage["x_score_provenance"].value_counts())

st.subheader("Civilisations à faible évidence")
low_evidence_civilizations = [
    {
        "id": civ["id"],
        "low_archetype_coverage": civ["low_archetype_coverage"],
        "extension_to_huntington": civ["extension_to_huntington"],
        "n_archetypes": len(civ["hofstede_archetype_states"]),
    }
    for civ in taxonomy["civilizations"]
]
st.dataframe(pd.DataFrame(low_evidence_civilizations), use_container_width=True)

st.subheader("Vérification — citations orphelines")
biblio_ids = {entry["id"] for entry in taxonomy["bibliography"]}
orphans: list[str] = []
for civ in taxonomy["civilizations"]:
    for citation_id in civ["citation_ids"]:
        if citation_id not in biblio_ids:
            orphans.append(f"{civ['id']} -> {citation_id}")
if orphans:
    st.error("Citations orphelines détectées :")
    for orphan in orphans:
        st.markdown(f"- {orphan}")
else:
    st.success("Aucune citation orpheline.")

st.subheader("Vérification — coordonnées orphelines")
if centroids_payload:
    centroid_ids = {c["civilization_id"] for c in centroids_payload["centroids"]}
    missing_centroids = [civ["id"] for civ in taxonomy["civilizations"] if civ["id"] not in centroid_ids]
    if missing_centroids:
        st.error(f"Civilisations sans centroïde : {missing_centroids}")
    else:
        st.success("Toutes les civilisations ont un centroïde calculé.")

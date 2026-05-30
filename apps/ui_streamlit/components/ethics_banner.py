"""Sticky ethics banner displayed on every Streamlit page."""
from __future__ import annotations

import streamlit as st

ETHICAL_WARNING_FR: str = (
    "Ce profil est inféré à partir de sources publiques agrégées. "
    "Il ne doit pas être utilisé pour classer des individus réels."
)
ETHICAL_WARNING_EN: str = (
    "This profile is inferred from public aggregate sources. "
    "It must not be used to classify real individuals."
)


def render() -> None:
    """Inject a sticky, non-dismissable ethics banner at the top of the page."""
    st.markdown(
        """
        <style>
        .cvs-ethics-banner {
            position: sticky;
            top: 0;
            z-index: 9999;
            background: #fff3cd;
            color: #664d03;
            border: 1px solid #ffecb5;
            padding: 0.6rem 1rem;
            border-radius: 0.4rem;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='cvs-ethics-banner'><strong>⚠️ Avertissement éthique</strong> — "
        f"{ETHICAL_WARNING_FR}</div>",
        unsafe_allow_html=True,
    )

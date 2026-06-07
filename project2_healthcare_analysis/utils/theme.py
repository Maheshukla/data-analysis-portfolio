import streamlit as st
from pathlib import Path

def apply_theme():

    css_path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "assets"
        / "style.css"
    )

    with open(
        css_path,
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
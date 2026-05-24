import streamlit as st

def apply_theme():

    with open(
        "project1_sales_analysis/assets/style.css",
        encoding="utf-8"
    ) as f:

        css = f.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )
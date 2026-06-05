import streamlit as st

from dashboards.sports_dashboard import sports_dashboard

st.set_page_config(
    page_title="Sports Analytics",
    page_icon="🏏",
    layout="wide"
)

sports_dashboard()
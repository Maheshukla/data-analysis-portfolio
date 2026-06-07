import streamlit as st
from dashboards.financial_dashboard import financial_dashboard

st.set_page_config(
    page_title="Financial Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

financial_dashboard()
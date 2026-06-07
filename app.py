import streamlit as st

# =========================
# IMPORTS
# =========================

from project1_sales_analysis.dashboards.sales_dashboard import (
    sales_dashboard
)

from project2_healthcare_analysis.dashboards.healthcare_dashboard import (
    healthcare_dashboard
)

from project3_sports_analytics.dashboards.sports_dashboard import (
    sports_dashboard
)

from project4_financial_analysis.dashboards.financial_dashboard import (
    financial_dashboard
)

from project5_ecommerce_analytics.dashboards.ecommerce_dashboard import (
    ecommerce_dashboard
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Analytics Portfolio",
    page_icon="📊",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("📊 Data Analytics Portfolio")

selected = st.sidebar.radio(
    "Select Project",
    [
        "Sales Analytics",
        "Healthcare Analytics",
        "Sports Analytics",
        "Financial Analytics",
        "E-Commerce Analytics"
    ]
)

# =========================
# ROUTING
# =========================

if selected == "Sales Analytics":

    sales_dashboard()

elif selected == "Healthcare Analytics":

    healthcare_dashboard()

elif selected == "Sports Analytics":

    sports_dashboard()

elif selected == "Financial Analytics":

    financial_dashboard()

elif selected == "E-Commerce Analytics":

    ecommerce_dashboard()
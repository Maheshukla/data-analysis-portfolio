import streamlit as st

from ..utils.helpers import (
    column_exists,
    safe_mean
)

# =========================
# KPI SECTION
# =========================

def render_kpis(df):

    # =========================
    # SAFE KPI VALUES
    # =========================

    total_patients = len(df)

    avg_age = safe_mean(
        df,
        "Patient Age"
    )

    avg_wait = safe_mean(
        df,
        "Patient Waittime"
    )

    avg_satisfaction = safe_mean(
        df,
        "Patient Satisfaction Score"
    )

    # =========================
    # SAFE DEPARTMENT
    # =========================

    if column_exists(
        df,
        "Department Referral"
    ):

        if not df[
            "Department Referral"
        ].dropna().empty:

            busiest_department = (

                df[
                    "Department Referral"
                ]

                .value_counts()

                .idxmax()
            )

        else:

            busiest_department = "No Data"

    else:

        busiest_department = "Missing"

    # =========================
    # KPI STYLES
    # =========================

    st.markdown(
        """
        <style>

        .kpi-card {

            background: linear-gradient(
                135deg,
                #111827,
                #1f2937
            );

            padding: 20px;

            border-radius: 18px;

            border: 1px solid #374151;

            text-align: center;

            box-shadow:
                0 0 15px rgba(0,0,0,0.4);

            transition: 0.3s;

            margin-bottom: 10px;
        }

        .kpi-card:hover {

            transform: translateY(-5px);

            box-shadow:
                0 0 20px rgba(59,130,246,0.5);
        }

        .kpi-title {

            color: #9ca3af;

            font-size: 15px;

            margin-bottom: 10px;
        }

        .kpi-value {

            color: white;

            font-size: 28px;

            font-weight: bold;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # KPI COLUMNS
    # =========================

    col1, col2, col3, col4, col5 = st.columns(5)

    # =========================
    # KPI 1
    # =========================

    with col1:

        st.markdown(f"""
    <div class="kpi-card">

    <div class="kpi-title">
    Total Patients
    </div>

    <div class="kpi-value">
    {total_patients:,}
    </div>

    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI 2
    # =========================

    with col2:

        st.markdown(f"""
    <div class="kpi-card">

    <div class="kpi-title">
    Average Age
    </div>

    <div class="kpi-value">
    {avg_age:.1f}
    </div>

    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI 3
    # =========================

    with col3:

        st.markdown(f"""
    <div class="kpi-card">

    <div class="kpi-title">
    Average Wait
    </div>

    <div class="kpi-value">
    {avg_wait:.1f} min
    </div>

    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI 4
    # =========================

    with col4:

        st.markdown(f"""
    <div class="kpi-card">

    <div class="kpi-title">
    Satisfaction
    </div>

    <div class="kpi-value">
    {avg_satisfaction:.1f}
    </div>

    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI 5
    # =========================

    with col5:

        st.markdown(f"""
    <div class="kpi-card">

    <div class="kpi-title">
    Busiest Department
    </div>

    <div class="kpi-value">
    {busiest_department}
    </div>

    </div>
    """, unsafe_allow_html=True)
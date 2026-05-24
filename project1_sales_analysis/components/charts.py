import plotly.express as px
import streamlit as st

from utils.helpers import column_exists

# =========================
# COMMON CHART STYLE
# =========================

def apply_chart_style(fig):

    fig.update_layout(

        template="plotly_dark",

        height=500,

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        font=dict(
            color="white"
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        title_font=dict(
            size=22
        )
    )

    return fig

# =========================
# GENDER DISTRIBUTION
# =========================

def gender_distribution_chart(df):

    if not column_exists(
        df,
        "Patient Gender"
    ):

        st.warning(
            "⚠️ Patient Gender column missing."
        )

        return

    fig = px.pie(
        df,
        names="Patient Gender",
        title="Gender Distribution",
        hole=0.5
    )

    fig = apply_chart_style(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="gender_chart"
    )

# =========================
# AGE DISTRIBUTION
# =========================

def age_distribution_chart(df):

    if not column_exists(
        df,
        "Patient Age"
    ):

        st.warning(
            "⚠️ Patient Age column missing."
        )

        return

    fig = px.histogram(
        df,
        x="Patient Age",
        nbins=25,
        title="Patient Age Distribution"
    )

    fig = apply_chart_style(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="age_chart"
    )

# =========================
# DEPARTMENT ANALYSIS
# =========================

def department_chart(df):

    if not column_exists(
        df,
        "Department Referral"
    ):

        st.warning(
            "⚠️ Department Referral column missing."
        )

        return

    department_df = (
        df["Department Referral"]
        .value_counts()
        .reset_index()
    )

    department_df.columns = [
        "Department",
        "Count"
    ]

    fig = px.bar(
        department_df,
        x="Department",
        y="Count",
        color="Department",
        title="Department Referral Analysis"
    )

    fig = apply_chart_style(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="department_chart"
    )

# =========================
# WAIT TIME ANALYSIS
# =========================

def wait_time_chart(df):

    if not column_exists(
        df,
        "Patient Waittime"
    ):

        st.warning(
            "⚠️ Patient Waittime column missing."
        )

        return

    fig = px.histogram(
        df,
        x="Patient Waittime",
        nbins=30,
        title="Patient Wait Time Distribution"
    )

    fig = apply_chart_style(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="wait_time_chart"
    )

# =========================
# BILLING ANALYSIS
# =========================

def billing_chart(df):

    if not column_exists(
        df,
        "Patient Waittime"
    ):

        st.warning(
            "⚠️ Patient Waittime column missing."
        )

        return

    fig = px.histogram(
        df,
        x="Patient Waittime",
        nbins=30,
        title="Billing Analysis"
    )

    fig = apply_chart_style(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="billing_chart"
    )

# =========================
# BILLING BY CONDITION
# =========================

def billing_by_condition_chart(df):

    if not (
        column_exists(
            df,
            "Department Referral"
        )

        and

        column_exists(
            df,
            "Patient Waittime"
        )
    ):

        st.warning(
            """
            ⚠️ Required columns missing for
            billing analysis.
            """
        )

        return

    billing_df = (
        df.groupby("Department Referral")
        ["Patient Waittime"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        billing_df,
        x="Department Referral",
        y="Patient Waittime",
        color="Department Referral",
        title="Average Wait Time by Department"
    )

    fig = apply_chart_style(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="billing_condition_chart"
    )

# =========================
# RACE DISTRIBUTION
# =========================

def race_distribution_chart(df):

    if not column_exists(
        df,
        "Patient Race"
    ):

        st.warning(
            "⚠️ Patient Race column missing."
        )

        return

    fig = px.pie(
        df,
        names="Patient Race",
        title="Patient Race Distribution",
        hole=0.4
    )

    fig = apply_chart_style(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="race_distribution_chart"
    )

# =========================
# SATISFACTION ANALYSIS
# =========================

def satisfaction_chart(df):

    if not column_exists(
        df,
        "Patient Satisfaction Score"
    ):

        st.warning(
            """
            ⚠️ Patient Satisfaction Score
            column missing.
            """
        )

        return

    fig = px.histogram(
        df,
        x="Patient Satisfaction Score",
        nbins=10,
        title="Patient Satisfaction Analysis"
    )

    fig = apply_chart_style(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="satisfaction_chart"
    )

# =========================
# GENDER VS SATISFACTION
# =========================

def gender_satisfaction_chart(df):

    if not (
        column_exists(
            df,
            "Patient Gender"
        )

        and

        column_exists(
            df,
            "Patient Satisfaction Score"
        )
    ):

        st.warning(
            """
            ⚠️ Required columns missing for
            gender satisfaction analysis.
            """
        )

        return

    fig = px.box(
        df,
        x="Patient Gender",
        y="Patient Satisfaction Score",
        color="Patient Gender",
        title="Gender vs Satisfaction Score"
    )

    fig = apply_chart_style(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="gender_satisfaction_chart"
    )
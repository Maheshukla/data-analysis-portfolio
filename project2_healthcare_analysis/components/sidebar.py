import streamlit as st

from ..utils.helpers import (
    column_exists,
    safe_category_values
)

# =========================
# SIDEBAR
# =========================

def render_sidebar(df):

    st.sidebar.markdown("---")

    st.sidebar.title(
        "🏥 Healthcare Analytics"
    )

    st.sidebar.markdown("---")

    st.sidebar.header(
        "📂 Dataset Filters"
    )

    # =========================
    # DOWNLOAD FILTERED DATA
    # =========================

    csv = df.to_csv(index=False)

    st.sidebar.download_button(
        label="📥 Download Dataset",
        data=csv,
        file_name="healthcare_filtered_data.csv",
        mime="text/csv"
    )

    filters = {}

    # =========================
    # GENDER FILTER
    # =========================

    if column_exists(df, "Patient Gender"):

        gender_options = safe_category_values(
            df,
            "Patient Gender"
        )

        selected_gender = st.sidebar.multiselect(
            "Select Gender",
            options=gender_options,
            default=gender_options
        )

        if not selected_gender:

            selected_gender = gender_options

        filters["gender"] = selected_gender

    else:

        filters["gender"] = []

    # =========================
    # RACE FILTER
    # =========================

    if column_exists(df, "Patient Race"):

        race_options = safe_category_values(
            df,
            "Patient Race"
        )

        selected_race = st.sidebar.multiselect(
            "Select Race",
            options=race_options,
            default=race_options
        )

        if not selected_race:

            selected_race = race_options

        filters["race"] = selected_race

    else:

        filters["race"] = []

    # =========================
    # DEPARTMENT FILTER
    # =========================

    if column_exists(df, "Department Referral"):

        department_options = safe_category_values(
            df,
            "Department Referral"
        )

        selected_department = st.sidebar.multiselect(
            "Department Referral",
            options=department_options,
            default=department_options
        )

        if not selected_department:

            selected_department = department_options

        filters["department"] = selected_department

    else:

        filters["department"] = []

    return filters
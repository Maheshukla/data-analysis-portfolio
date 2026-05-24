import pandas as pd
import streamlit as st

# =========================
# LOAD HEALTHCARE DATA
# =========================

@st.cache_data
def load_data(uploaded_file=None):

    try:

        # =========================
        # USER UPLOADED CSV
        # =========================

        if uploaded_file is not None:

            df = pd.read_csv(
                uploaded_file
            )

        # =========================
        # DEFAULT DATASET
        # =========================

        else:

            df = pd.read_csv(
                "project1_sales_analysis/datasets/healthcare_dataset.csv"
            )

        # =========================
        # CLEAN COLUMN NAMES
        # =========================

        df.columns = (
            df.columns
            .str.strip()
        )

        return df

    # =========================
    # ERROR HANDLING
    # =========================

    except Exception as e:

        st.error(
            f"""
            ❌ Error loading dataset:

            {str(e)}
            """
        )

        return pd.DataFrame()
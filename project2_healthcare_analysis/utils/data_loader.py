import pandas as pd
import streamlit as st
from pathlib import Path

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

            dataset_path = (
                Path(__file__)
                .resolve()
                .parent.parent
                / "datasets"
                / "healthcare_dataset.csv"
            )

            df = pd.read_csv(
                dataset_path
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
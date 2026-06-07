import pandas as pd
import streamlit as st
from pathlib import Path


# =========================
# ODI MATCH INFO
# =========================

@st.cache_data
def load_odi_match_info():

    data_path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "data"
        / "ODI_Match_info.csv"
    )

    df = pd.read_csv(
        data_path,
        low_memory=False
    )

    return df


# =========================
# ODI BALL DATA
# =========================

@st.cache_data
def load_odi_ball_data():

    data_path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "data"
        / "ODI_Match_Data.csv"
    )

    df = pd.read_csv(
        data_path,
        low_memory=False
    )

    return df


# =========================
# IPL MATCH DATA
# =========================

@st.cache_data
def load_ipl_matches():

    data_path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "data"
        / "matches_updated_ipl_upto_2025.csv"
    )

    df = pd.read_csv(
        data_path,
        low_memory=False
    )

    return df


# =========================
# COMBINED MATCH DATA
# =========================

@st.cache_data
def load_combined_data():

    odi_df = load_odi_match_info()

    ipl_df = load_ipl_matches()

    # ODI Standard Columns

    odi_df = odi_df.rename(
        columns={
            "team1": "team1",
            "team2": "team2",
            "winner": "winner",
            "venue": "venue",
            "date": "date"
        }
    )

    # IPL Standard Columns

    ipl_df = ipl_df.rename(
        columns={
            "team1": "team1",
            "team2": "team2",
            "winner": "winner",
            "venue": "venue",
            "date": "date"
        }
    )

    common_columns = [

        "team1",
        "team2",
        "winner",
        "venue",
        "date"

    ]

    combined_df = pd.concat(

        [

            odi_df[common_columns],

            ipl_df[common_columns]

        ],

        ignore_index=True

    )

    return combined_df
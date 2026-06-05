import streamlit as st


def render_sidebar(df):

    st.sidebar.title("🏏 Cricket Analytics")

    cricket_format = st.sidebar.selectbox(
        "Select Format",
        ["ODI", "IPL", "Combined"],
        key="cricket_format"
    )

    teams = sorted(
        set(df["team1"].dropna())
        |
        set(df["team2"].dropna())
    )

    selected_teams = st.sidebar.multiselect(
        "Select Team",
        options=teams,
        default=teams,
        key="team_filter"
    )

    venues = sorted(
        df["venue"].dropna().unique()
    ) if "venue" in df.columns else []

    selected_venues = st.sidebar.multiselect(
        "Select Venue",
        options=venues,
        default=venues,
        key="venue_filter"
    )

    seasons = sorted(
        df["season"].dropna().astype(str).unique()
    ) if "season" in df.columns else []

    selected_seasons = st.sidebar.multiselect(
        "Select Season",
        options=seasons,
        default=seasons,
        key="season_filter"
    )

    return {
        "format": cricket_format,
        "teams": selected_teams,
        "venues": selected_venues,
        "seasons": selected_seasons
    }
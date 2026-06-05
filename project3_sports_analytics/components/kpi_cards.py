import streamlit as st


def render_kpis(df):

    # =========================
    # TOTAL MATCHES
    # =========================

    total_matches = len(df)

    # =========================
    # TOTAL TEAMS
    # =========================

    teams = set(df["team1"].dropna()) | set(df["team2"].dropna())

    total_teams = len(teams)

    # =========================
    # TOTAL VENUES
    # =========================

    if "venue" in df.columns:

        total_venues = (
            df["venue"]
            .nunique()
        )

    else:

        total_venues = 0

    # =========================
    # TOTAL SEASONS
    # =========================

    if "season" in df.columns:

        total_seasons = (
            df["season"]
            .astype(str)
            .nunique()
        )

    else:

        total_seasons = 0

    # =========================
    # MOST SUCCESSFUL TEAM
    # =========================

    if "winner" in df.columns:

        winner_counts = (
            df["winner"]
            .value_counts()
        )

        most_successful_team = (
            winner_counts.idxmax()
        )

        top_team_wins = (
            winner_counts.max()
        )

    else:

        most_successful_team = "N/A"

        top_team_wins = 0

    # =========================
    # KPI DISPLAY
    # =========================

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Matches",
        f"{total_matches:,}"
    )

    col2.metric(
        "Teams",
        total_teams
    )

    col3.metric(
        "Venues",
        total_venues
    )

    col4.metric(
        "Seasons",
        total_seasons
    )

    col5.metric(
        "Top Team Wins",
        top_team_wins,
        most_successful_team
    )
import plotly.express as px
import streamlit as st


def top_winning_teams_chart(df):

    if "winner" not in df.columns:
        st.warning("Winner column not found")
        return

    team_wins = (
        df["winner"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    team_wins.columns = [
        "Team",
        "Wins"
    ]

    fig = px.bar(
        team_wins,
        x="Team",
        y="Wins",
        title="🏆 Top 10 Winning Teams"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def toss_impact_chart(df):

    required_cols = [
        "toss_winner",
        "winner"
    ]

    if not all(col in df.columns for col in required_cols):
        st.warning(
            "Toss data not available"
        )
        return

    toss_df = df[
        df["toss_winner"] == df["winner"]
    ]

    toss_win_pct = round(
        (
            len(toss_df)
            / len(df)
        ) * 100,
        2
    )

    fig = px.pie(
        values=[
            toss_win_pct,
            100 - toss_win_pct
        ],
        names=[
            "Won Toss & Match",
            "Lost After Toss Win"
        ],
        title="🎯 Toss Impact Analysis"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def top_venues_chart(df):

    if "venue" not in df.columns:
        st.warning(
            "Venue column not found"
        )
        return

    venue_df = (
        df["venue"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    venue_df.columns = [
        "Venue",
        "Matches"
    ]

    fig = px.bar(
        venue_df,
        x="Matches",
        y="Venue",
        orientation="h",
        title="🏟 Top Match Venues"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def top_player_of_match_chart(df):

    if "player_of_match" not in df.columns:
        st.warning("player_of_match column not found")
        return

    pom = (
        df["player_of_match"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    pom.columns = [
        "Player",
        "Awards"
    ]

    fig = px.bar(
        pom,
        x="Player",
        y="Awards",
        title="🏅 Top Player Of Match Winners"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def matches_per_season_chart(df):

    if "season" not in df.columns:
        st.warning("season column not found")
        return

    season_df = (
        df["season"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    season_df.columns = [
        "Season",
        "Matches"
    ]

    fig = px.line(
        season_df,
        x="Season",
        y="Matches",
        markers=True,
        title="📈 Matches Per Season"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def top_cities_chart(df):

    if "city" not in df.columns:
        st.warning("city column not found")
        return

    city_df = (
        df["city"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    city_df.columns = [
        "City",
        "Matches"
    ]

    fig = px.bar(
        city_df,
        x="City",
        y="Matches",
        title="🌍 Top Cricket Cities"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def biggest_wins_by_runs_chart(df):

    if "win_by_runs" not in df.columns:
        st.warning("win_by_runs column not found")
        return

    runs_df = (
        df[
            df["win_by_runs"] > 0
        ]
        .sort_values(
            "win_by_runs",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        runs_df,
        x="winner",
        y="win_by_runs",
        title="🔥 Biggest Wins By Runs"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def biggest_wins_by_wickets_chart(df):

    if "win_by_wickets" not in df.columns:
        st.warning("win_by_wickets column not found")
        return

    wickets_df = (
        df[
            df["win_by_wickets"] > 0
        ]
        .sort_values(
            "win_by_wickets",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        wickets_df,
        x="winner",
        y="win_by_wickets",
        title="⚡ Biggest Wins By Wickets"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def top_run_scorers_chart(ball_df):

    runs_df = (
        ball_df
        .groupby("striker")["runs_off_bat"]
        .sum()
        .reset_index()
        .sort_values(
            "runs_off_bat",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        runs_df,
        x="striker",
        y="runs_off_bat",
        title="🏏 Top Run Scorers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def top_wicket_takers_chart(ball_df):

    wickets_df = (
        ball_df[
            ball_df["player_dismissed"]
            .notna()
        ]
        .groupby("bowler")
        .size()
        .reset_index(
            name="wickets"
        )
        .sort_values(
            "wickets",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        wickets_df,
        x="bowler",
        y="wickets",
        title="🎯 Top Wicket Takers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def most_fours_chart(ball_df):

    fours_df = (
        ball_df[
            ball_df["runs_off_bat"] == 4
        ]
        .groupby("striker")
        .size()
        .reset_index(
            name="fours"
        )
        .sort_values(
            "fours",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        fours_df,
        x="striker",
        y="fours",
        title="4️⃣ Most Fours"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def most_sixes_chart(ball_df):

    sixes_df = (
        ball_df[
            ball_df["runs_off_bat"] == 6
        ]
        .groupby("striker")
        .size()
        .reset_index(
            name="sixes"
        )
        .sort_values(
            "sixes",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        sixes_df,
        x="striker",
        y="sixes",
        title="6️⃣ Most Sixes"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def player_comparison_stats(ball_df, player1, player2):

    p1_runs = (
        ball_df[
            ball_df["striker"] == player1
        ]["runs_off_bat"]
        .sum()
    )

    p2_runs = (
        ball_df[
            ball_df["striker"] == player2
        ]["runs_off_bat"]
        .sum()
    )

    p1_fours = len(
        ball_df[
            (ball_df["striker"] == player1)
            &
            (ball_df["runs_off_bat"] == 4)
        ]
    )

    p2_fours = len(
        ball_df[
            (ball_df["striker"] == player2)
            &
            (ball_df["runs_off_bat"] == 4)
        ]
    )

    p1_sixes = len(
        ball_df[
            (ball_df["striker"] == player1)
            &
            (ball_df["runs_off_bat"] == 6)
        ]
    )

    p2_sixes = len(
        ball_df[
            (ball_df["striker"] == player2)
            &
            (ball_df["runs_off_bat"] == 6)
        ]
    )

    return {
        "Runs": [p1_runs, p2_runs],
        "Fours": [p1_fours, p2_fours],
        "Sixes": [p1_sixes, p2_sixes]
    }

def player_comparison_chart(
    comparison_df
):

    fig = px.line_polar(
        comparison_df.reset_index(),
        r=comparison_df.iloc[0],
        theta=comparison_df.columns,
        line_close=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def player_comparison_bar_chart(
    comparison_df
):

    chart_df = (
        comparison_df
        .reset_index()
        .melt(
            id_vars="index",
            var_name="Metric",
            value_name="Value"
        )
    )

    fig = px.bar(
        chart_df,
        x="Metric",
        y="Value",
        color="index",
        barmode="group",
        title="⚔️ Player Comparison"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
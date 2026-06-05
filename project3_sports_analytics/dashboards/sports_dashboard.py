import streamlit as st
import pandas as pd
from components.sidebar import render_sidebar
from components.kpi_cards import render_kpis
from utils.data_loader import (
    load_odi_match_info,
    load_odi_ball_data
)
from utils.preprocessing import preprocess_data
from components.charts import (
    top_winning_teams_chart,
    top_venues_chart,
    top_player_of_match_chart,
    matches_per_season_chart,
    top_cities_chart,
    biggest_wins_by_runs_chart,
    biggest_wins_by_wickets_chart,
    top_run_scorers_chart,
    top_wicket_takers_chart,
    most_fours_chart,
    most_sixes_chart,
    player_comparison_stats,
    player_comparison_bar_chart
)
from models.prediction_model import (
    train_match_winner_model
)

from models.anomaly_detection import (
    detect_anomalies
)

from models.forecasting_model import (
    forecast_matches
)

def sports_dashboard():

    # =========================
    # LOAD DATA
    # =========================

    with st.spinner(
        "Loading Cricket Data..."
    ):

        df = load_odi_match_info()

        ball_df = load_odi_ball_data()

    df = preprocess_data(
        df,
        "date"
    )

    df["player_of_match"] = (
        df["player_of_match"]
        .replace(0, pd.NA)
    )

    df["player_of_match"] = (
        df["player_of_match"]
        .replace("0", pd.NA)
    )

    # =========================
    # SIDEBAR
    # =========================

    filters = render_sidebar(df)

    # =========================
    # APPLY FILTERS
    # =========================

    if filters["teams"]:

        df = df[

            (df["team1"].isin(filters["teams"]))

            |

            (df["team2"].isin(filters["teams"]))

        ]

    if filters["venues"]:

        df = df[
            df["venue"].isin(
                filters["venues"]
            )
        ]

    if filters["seasons"]:

        df = df[
            df["season"]
            .astype(str)
            .isin(
                filters["seasons"]
            )
        ]

    # =========================
    # HEADER
    # =========================

    st.markdown(
        """
        <div style="
        background:linear-gradient(
        135deg,
        #111827,
        #1e293b
        );
        padding:25px;
        border-radius:15px;
        margin-bottom:20px;
        ">

        <h1 style="
        color:white;
        text-align:center;
        ">
        🏏 Cricket Analytics Dashboard
        </h1>

        <p style="
        color:#d1d5db;
        text-align:center;
        ">
        ODI • IPL • Combined Analytics
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # KPIs
    # =========================

    render_kpis(df)

    st.divider()

    # =========================
    # TABS
    # =========================

    (
        tab1,
        tab2,
        tab3,
        tab4,
        tab5,
        tab6,
        tab7,
        tab8,
        tab9,
        tab10

    ) = st.tabs([

        "Overview",

        "Team Analytics",

        "Player Analytics",

        "Match Analytics",

        "AI Insights",

        "SQL Analytics",

        "Anomaly Detection",

        "Forecasting",

        "ML Prediction",

        "Reports"

    ])

    # =========================
    # OVERVIEW
    # =========================

    with tab1:

        st.subheader(
            "📋 Cricket Overview"
        )

        st.dataframe(
            df.head(20),
            use_container_width=True
        )

    # =========================
    # TEAM ANALYTICS
    # =========================

    with tab2:

        st.subheader("🏏 Team Analytics")

        top_winning_teams_chart(df)

        st.divider()

        top_venues_chart(df)

    # =========================
    # PLAYER ANALYTICS
    # =========================

    with tab3:

        st.subheader(
            "👨‍💼 Player Analytics"
        )

        col1, col2 = st.columns(2)

        with col1:
            top_run_scorers_chart(
                ball_df
            )

        with col2:
            top_wicket_takers_chart(
                ball_df
            )

        st.divider()

        st.subheader(
            "⚔️ Player Comparison"
        )

        players = sorted(
            ball_df["striker"]
            .dropna()
            .unique()
        )

        player1 = st.selectbox(
            "Player 1",
            players,
            key="player1"
        )

        player2 = st.selectbox(
            "Player 2",
            players,
            index=1,
            key="player2"
        )

        comparison = player_comparison_stats(
            ball_df,
            player1,
            player2
        )

        comparison_df = pd.DataFrame(
            comparison,
            index=[
                player1,
                player2
            ]
        )

        st.dataframe(
            comparison_df,
            use_container_width=True
        )

        player_comparison_bar_chart(
            comparison_df
        )

    # =========================
    # MATCH ANALYTICS
    # =========================

    with tab4:

        st.subheader(
            "📊 Match Analytics"
        )

        col1, col2 = st.columns(2)

        with col1:
            matches_per_season_chart(df)

        with col2:
            top_cities_chart(df)

        st.divider()

        col3, col4 = st.columns(2)

        with col3:
            biggest_wins_by_runs_chart(df)

        with col4:
            biggest_wins_by_wickets_chart(df)

    # =========================
    # AI INSIGHTS
    # =========================

    with tab5:

        st.subheader(
            "🤖 AI Cricket Insights"
        )

        top_team = (
            df["winner"]
            .value_counts()
            .idxmax()
        )

        top_team_wins = (
            df["winner"]
            .value_counts()
            .max()
        )

        top_player = (
            df["player_of_match"]
            .value_counts()
            .idxmax()
        )

        top_player_awards = (
            df["player_of_match"]
            .value_counts()
            .max()
        )

        top_venue = (
            df["venue"]
            .value_counts()
            .idxmax()
        )

        total_matches = len(df)

        st.success(
            f"""
    🏆 Most Successful Team: {top_team}
    ({top_team_wins} wins)

    🌟 Top Player Of Match Winner:
    {top_player}
    ({top_player_awards} awards)

    🏟 Most Used Venue:
    {top_venue}

    📊 Total Matches Analyzed:
    {total_matches}
            """
        )

        st.divider()

        st.markdown("### 🧠 Auto Generated Insights")

        st.info(
            f"""
    • {top_team} is currently the most successful team in the dataset.

    • {top_player} has won the highest number of Player of Match awards.

    • {top_venue} has hosted the most matches.

    • The dashboard currently contains analysis of {total_matches} matches.

    • Team performance and venue impact appear to be the strongest predictors in the ML model.
            """
        )

        st.metric(
            "Most Successful Team",
            top_team
        )

        st.metric(
            "Top Player",
            top_player
        )

    # =========================
    # SQL ANALYTICS
    # =========================

    with tab6:

        st.subheader(
            "🗄 SQL Analytics"
        )

        st.markdown(
            "### Top Teams By Wins"
        )

        top_teams = (
            df.groupby("winner")
            .size()
            .reset_index(
                name="wins"
            )
            .sort_values(
                "wins",
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            top_teams,
            use_container_width=True
        )

        st.divider()

        st.markdown(
            "### Top Venues By Matches"
        )

        top_venues = (
            df.groupby("venue")
            .size()
            .reset_index(
                name="matches"
            )
            .sort_values(
                "matches",
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            top_venues,
            use_container_width=True
        )

        st.divider()

        st.markdown(
            "### Top Players Of Match"
        )

        top_players = (
            df.groupby(
                "player_of_match"
            )
            .size()
            .reset_index(
                name="awards"
            )
            .sort_values(
                "awards",
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            top_players,
            use_container_width=True
        )

    # =========================
    # ANOMALY
    # =========================

    with tab7:

        st.subheader(
            "🚨 Match Anomaly Detection"
        )

        anomaly_df = detect_anomalies(df)

        anomaly_count = len(
            anomaly_df[
                anomaly_df["anomaly"] == -1
            ]
        )

        st.metric(
            "Detected Anomalies",
            anomaly_count
        )

        st.dataframe(
            anomaly_df[
                anomaly_df["anomaly"] == -1
            ].head(20),
            use_container_width=True
        )

    # =========================
    # FORECASTING
    # =========================

    with tab8:

        st.subheader(
            "📈 Match Forecasting"
        )

        season_df, forecast = (
            forecast_matches(df)
        )

        st.line_chart(
            season_df.set_index(
                "season"
            )["matches"]
        )

        st.metric(
            "Predicted Matches Next Season",
            forecast
        )

    # =========================
    # ML
    # =========================

    with tab9:

        st.subheader(
            "🧠 Match Winner Prediction"
        )

        model, encoders, accuracy, feature_importance = (
            train_match_winner_model(df)
        )

        st.info(
            f"Model Accuracy: {accuracy:.2%}"
        )

        st.subheader(
            "Feature Importance"
        )

        st.bar_chart(
            feature_importance.set_index(
                "Feature"
            )
        )

        teams = sorted(
            list(
                set(
                    df["team1"].dropna().unique()
                )
                |
                set(
                    df["team2"].dropna().unique()
                )
            )
        )

        venues = sorted(
            df["venue"]
            .dropna()
            .unique()
        )

        team1 = st.selectbox(
            "Select Team 1",
            teams
        )

        team2 = st.selectbox(
            "Select Team 2",
            teams,
            index=1
        )

        venue = st.selectbox(
            "Venue",
            venues
        )

        toss_winner = st.selectbox(
            "Toss Winner",
            [
                team1,
                team2
            ]
        )

        toss_decision = st.selectbox(
            "Toss Decision",
            [
                "bat",
                "field"
            ]
        )

        if st.button(
            "Predict Winner"
        ):

            if (
                team1 not in encoders["team1"].classes_
                or
                team2 not in encoders["team2"].classes_
            ):
                st.error(
                    "Selected team not available in training data."
                )

            else:

                sample = [[

                    encoders["team1"]
                    .transform([team1])[0],

                    encoders["team2"]
                    .transform([team2])[0],

                    encoders["toss_winner"]
                    .transform([toss_winner])[0],

                    encoders["toss_decision"]
                    .transform([toss_decision])[0],

                    encoders["venue"]
                    .transform([venue])[0]

                ]]

                prediction = model.predict(
                    sample
                )[0]

                probabilities = model.predict_proba(
                    sample
                )[0]

                predicted_winner = (
                    encoders["winner"]
                    .inverse_transform(
                        [prediction]
                    )[0]
                )

                confidence = round(
                    max(probabilities) * 100,
                    2
                )

                st.success(
                    f"🏆 Predicted Winner: {predicted_winner}"
                )

                st.metric(
                    "Prediction Confidence",
                    f"{confidence}%"
                )

    # =========================
    # REPORTS
    # =========================

    with tab10:

        st.subheader(
            "📄 Reports"
        )

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download CSV Report",
            data=csv,
            file_name="cricket_report.csv",
            mime="text/csv"
        )

        st.divider()

        st.caption(
            "🏏 Cricket Analytics Dashboard | Python • Streamlit • Machine Learning • Data Analytics"
        )
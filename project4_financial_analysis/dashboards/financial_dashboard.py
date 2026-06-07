import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.ensemble import IsolationForest

@st.cache_data
def load_data():

    data_path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "data"
        / "Market.csv"
    )

    df = pd.read_csv(data_path)

    df["Date"] = pd.to_datetime(df["Date"])

    return df


def financial_dashboard():

    st.title("📈 Financial Analytics Dashboard")

    st.caption(
        """
        Interactive Financial Analytics Platform
        with Market Analytics, Risk Analysis,
        AI Insights, Forecasting and Machine Learning.
        """
    )

    df = load_data()

    # ======================
    # SIDEBAR FILTERS
    # ======================

    st.sidebar.header("Filters")

    selected_index = st.sidebar.selectbox(
        "Select Market Index",
        sorted(df["Index"].unique())
    )

    filtered_df = df[
        df["Index"] == selected_index
    ]

    min_date = filtered_df["Date"].min()
    max_date = filtered_df["Date"].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    year_list = sorted(
        filtered_df["Date"].dt.year.unique()
    )

    selected_year = st.sidebar.selectbox(
        "Select Year",
        ["All"] + list(year_list)
    )

    st.sidebar.subheader("Advanced Filters")

    min_close = float(df["Close"].min())
    max_close = float(df["Close"].max())

    close_range = st.sidebar.slider(
        "Close Price Range",
        min_value=min_close,
        max_value=max_close,
        value=(min_close, max_close)
    )

    min_volume = int(
        filtered_df["Volume"].quantile(0.01)
    )

    max_volume = int(
        filtered_df["Volume"].quantile(0.99)
    )

    volume_range = st.sidebar.slider(
        "Volume Range",
        min_value=min_volume,
        max_value=max_volume,
        value=(min_volume, max_volume)
    )

    if len(date_range) == 2:

        start_date, end_date = date_range

        filtered_df = filtered_df[
            (filtered_df["Date"] >= pd.to_datetime(start_date))
            &
            (filtered_df["Date"] <= pd.to_datetime(end_date))
        ]

    if selected_year != "All":

        filtered_df = filtered_df[
            filtered_df["Date"].dt.year
            == selected_year
        ]

    # ======================
    # ADVANCED FILTERS
    # ======================

    filtered_df = filtered_df[
        (filtered_df["Close"] >= close_range[0])
        &
        (filtered_df["Close"] <= close_range[1])
    ]

    filtered_df = filtered_df[
        (filtered_df["Volume"] >= volume_range[0])
        &
        (filtered_df["Volume"] <= volume_range[1])
    ]

    chart_data = filtered_df.sort_values("Date")

    # ======================
    # KPI CARDS
    # ======================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📈 Records",
            len(filtered_df)
        )

    with col2:
        st.metric(
            "💰 Avg Close",
            round(filtered_df["Close"].mean(), 2)
        )

    with col3:
        st.metric(
            "🚀 Highest Close",
            round(filtered_df["Close"].max(), 2)
        )

    with col4:
        st.metric(
            "📉 Lowest Close",
            round(filtered_df["Close"].min(), 2)
        )

    st.divider()

    # ======================
    # TABS
    # ======================

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "Overview",
        "Market Analytics",
        "Risk Analytics",
        "AI Insights",
        "SQL Analytics",
        "Forecasting",
        "ML Prediction",
        "Reports",
        "Anomaly Detection",
        "Portfolio Simulator"
    ])

    # ======================
    # OVERVIEW TAB
    # ======================

    with tab1:

        st.subheader("📈 Closing Price Trend")

        fig = px.line(
            chart_data,
            x="Date",
            y="Close",
            title=f"{selected_index} Closing Price Trend"
        )

        fig.update_layout(
            height=600
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
        st.info(
            f"""
            Selected Index: {selected_index}

            Total Records: {len(chart_data)}

            Date Range:
            {chart_data['Date'].min().date()}
            to
            {chart_data['Date'].max().date()}
            """
        )

    # ======================
    # MARKET ANALYTICS TAB
    # ======================

    with tab2:

        st.subheader("📊 Market Analytics")

        col1, col2 = st.columns(2)

        with col1:

            open_close_fig = px.line(
                chart_data,
                x="Date",
                y=["Open", "Close"],
                title="Open vs Close Price"
            )

            st.plotly_chart(
                open_close_fig,
                use_container_width=True
            )

        with col2:

            volume_fig = px.line(
                chart_data,
                x="Date",
                y="Volume",
                title="Trading Volume Trend"
            )

            st.plotly_chart(
                volume_fig,
                use_container_width=True
            )

        st.markdown("---")

        st.subheader(
            "Correlation Analysis"
        )

        corr = chart_data[
            [
                "Open",
                "High",
                "Low",
                "Close",
                "Volume"
            ]
        ].corr()

        heatmap = px.imshow(
            corr,
            text_auto=True,
            title="Correlation Heatmap"
        )

        heatmap.update_layout(
            height=700
        )

        st.plotly_chart(
            heatmap,
            use_container_width=True
        )

    # ======================
    # RISK ANALYTICS TAB
    # ======================

    with tab3:

        st.subheader("⚠️ Risk Analytics")

        risk_df = chart_data.copy()

        risk_df["Daily Return"] = (
            risk_df["Close"].pct_change() * 100
        )

        volatility = risk_df["Daily Return"].std()

        avg_return = risk_df["Daily Return"].mean()

        if volatility < 1:
            risk_level = "Low Risk"
        elif volatility < 2:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Average Return %",
                round(avg_return, 2)
            )

        with col2:
            st.metric(
                "Volatility",
                round(volatility, 2)
            )

        with col3:
            st.metric(
                "Risk Level",
                risk_level
            )

        st.divider()

        return_fig = px.histogram(
            risk_df,
            x="Daily Return",
            nbins=50,
            title="Daily Return Distribution"
        )

        st.plotly_chart(
            return_fig,
            use_container_width=True
        )

    # ======================
    # AI INSIGHTS TAB
    # ======================

    with tab4:

        st.subheader("🤖 AI Financial Insights")

        latest_close = chart_data["Close"].iloc[-1]

        avg_close = chart_data["Close"].mean()

        volatility = (
            chart_data["Close"]
            .pct_change()
            .std() * 100
        )

        if latest_close > avg_close:

            st.success(
                f"""
                Current market price ({latest_close:.2f})
                is above historical average
                ({avg_close:.2f}).

                Market trend appears bullish.
                """
            )

        else:

            st.warning(
                f"""
                Current market price ({latest_close:.2f})
                is below historical average
                ({avg_close:.2f}).

                Market trend appears bearish.
                """
            )

        if volatility > 2:

            st.error(
                "High market volatility detected. Risk level is elevated."
            )

        else:

            st.info(
                "Market volatility appears stable."
            )

        st.markdown("---")

        st.subheader("AI Recommendations")

        recommendations = []

        if latest_close > avg_close:
            recommendations.append(
                "Consider trend-following investment strategies."
            )

        if volatility > 2:
            recommendations.append(
                "Maintain strict risk management."
            )

        if volatility <= 2:
            recommendations.append(
                "Market conditions appear relatively stable."
            )

        for rec in recommendations:
            st.write("✅", rec)

    # ======================
    # SQL ANALYTICS TAB
    # ======================

    with tab5:

        st.subheader("📊 SQL Analytics")

        col1, col2 = st.columns(2)

        with col1:

            highest_close = chart_data.loc[
                chart_data["Close"].idxmax()
            ]

            st.info(
                f"""
                Highest Close Price

                Date: {highest_close['Date'].date()}

                Close: {highest_close['Close']:.2f}
                """
            )

        with col2:

            lowest_close = chart_data.loc[
                chart_data["Close"].idxmin()
            ]

            st.info(
                f"""
                Lowest Close Price

                Date: {lowest_close['Date'].date()}

                Close: {lowest_close['Close']:.2f}
                """
            )

        st.markdown("---")

        st.subheader("Query Results")

        query1 = pd.DataFrame({
            "Metric": [
                "Average Close",
                "Maximum Close",
                "Minimum Close",
                "Average Volume"
            ],
            "Value": [
                round(chart_data["Close"].mean(), 2),
                round(chart_data["Close"].max(), 2),
                round(chart_data["Close"].min(), 2),
                round(chart_data["Volume"].mean(), 2)
            ]
        })

        st.dataframe(
            query1,
            use_container_width=True
        )

        st.markdown("---")

        st.subheader("Top 10 Trading Volume Days")

        top_volume = chart_data.nlargest(
            10,
            "Volume"
        )[
            ["Date", "Volume", "Close"]
        ]

        st.dataframe(
            top_volume,
            use_container_width=True
        )

    # ======================
    # FORECASTING TAB
    # ======================

    with tab6:

        st.subheader("📈 Forecasting")

        forecast_df = chart_data.copy()

        forecast_df["MA_30"] = (
            forecast_df["Close"]
            .rolling(30)
            .mean()
        )

        forecast_df["MA_90"] = (
            forecast_df["Close"]
            .rolling(90)
            .mean()
        )

        fig = px.line(
            forecast_df,
            x="Date",
            y=["Close", "MA_30", "MA_90"],
            title="Price Forecast Trend Using Moving Averages"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        latest_price = forecast_df["Close"].iloc[-1]
        ma30 = forecast_df["MA_30"].iloc[-1]
        ma90 = forecast_df["MA_90"].iloc[-1]

        st.markdown("---")

        st.subheader("Forecast Summary")

        if ma30 > ma90:

            st.success(
                f"""
                Bullish Signal Detected

                Current Price : {latest_price:.2f}

                30 Day MA : {ma30:.2f}

                90 Day MA : {ma90:.2f}
                """
            )

        else:

            st.warning(
                f"""
                Bearish Signal Detected

                Current Price : {latest_price:.2f}

                30 Day MA : {ma30:.2f}

                90 Day MA : {ma90:.2f}
                """
            )

        predicted_price = latest_price * 1.03

        st.metric(
            "Estimated Next Trend Price",
            round(predicted_price, 2)
        )

    # ======================
    # ML PREDICTION TAB
    # ======================

    with tab7:

        st.subheader("🧠 ML Price Prediction")

        ml_df = chart_data.copy()

        ml_df = ml_df[
            [
                "Open",
                "High",
                "Low",
                "Volume",
                "Close"
            ]
        ].dropna()

        X = ml_df[
            [
                "Open",
                "High",
                "Low",
                "Volume"
            ]
        ]

        y = ml_df["Close"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        model = LinearRegression()

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        accuracy = r2_score(
            y_test,
            predictions
        )

        st.metric(
            "Model Accuracy (R²)",
            round(accuracy, 4)
        )

        st.markdown("---")

        st.subheader(
            "Predict Closing Price"
        )

        open_price = st.number_input(
            "Open Price",
            value=float(
                ml_df["Open"].mean()
            )
        )

        high_price = st.number_input(
            "High Price",
            value=float(
                ml_df["High"].mean()
            )
        )

        low_price = st.number_input(
            "Low Price",
            value=float(
                ml_df["Low"].mean()
            )
        )

        volume = st.number_input(
            "Volume",
            value=float(
                ml_df["Volume"].mean()
            )
        )

        if st.button(
            "Predict Close Price"
        ):

            prediction = model.predict(
                [[
                    open_price,
                    high_price,
                    low_price,
                    volume
                ]]
            )[0]

            st.success(
                f"Predicted Close Price: {prediction:.2f}"
            )

        st.markdown("---")

        st.subheader(
            "Actual vs Predicted"
        )

        compare_df = pd.DataFrame({

            "Actual": y_test.values[:100],

            "Predicted": predictions[:100]

        })

        compare_fig = px.line(
            compare_df,
            title="Actual vs Predicted Prices"
        )

        st.plotly_chart(
            compare_fig,
            use_container_width=True
        )

        st.markdown("---")

        st.subheader(
            "Feature Importance"
        )

        importance_df = pd.DataFrame({

            "Feature": X.columns,

            "Importance": abs(
                model.coef_
            )

        })

        importance_fig = px.bar(
            importance_df,
            x="Feature",
            y="Importance",
            title="Feature Importance"
        )

        st.plotly_chart(
            importance_fig,
            use_container_width=True
        )

    with tab8:

        st.subheader("📄 Reports & Export")

        st.write(
            "Download filtered financial data."
        )

        csv = chart_data.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download CSV Report",
            data=csv,
            file_name="financial_report.csv",
            mime="text/csv"
        )

        summary_df = pd.DataFrame({

            "Metric": [
                "Average Close",
                "Maximum Close",
                "Minimum Close",
                "Average Volume"
            ],

            "Value": [
                round(chart_data["Close"].mean(), 2),
                round(chart_data["Close"].max(), 2),
                round(chart_data["Close"].min(), 2),
                round(chart_data["Volume"].mean(), 2)
            ]

        })

        st.dataframe(
            summary_df,
            use_container_width=True
        )

        st.markdown("---")

        st.subheader(
            "Top 10 Highest Close Prices"
        )

        top_close = chart_data.nlargest(
            10,
            "Close"
        )[
            ["Date", "Close", "Volume"]
        ]

        top_close["Date"] = top_close["Date"].dt.date

        st.dataframe(
            top_close,
            use_container_width=True
        )

    # ======================
    # ANOMALY DETECTION TAB
    # ======================

    with tab9:

        st.subheader("🚨 Market Anomaly Detection")

        anomaly_df = chart_data.copy()

        anomaly_model = IsolationForest(
            contamination=0.02,
            random_state=42
        )

        anomaly_df["Anomaly"] = anomaly_model.fit_predict(
            anomaly_df[["Close"]]
        )

        anomalies = anomaly_df[
            anomaly_df["Anomaly"] == -1
        ]

        st.metric(
            "Anomalies Detected",
            len(anomalies)
        )

        fig = px.scatter(
            anomaly_df,
            x="Date",
            y="Close",
            color="Anomaly",
            title="Market Anomalies"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("---")

        st.subheader(
            "Detected Anomaly Records"
        )

        st.dataframe(
            anomalies[
                ["Date", "Close"]
            ],
            use_container_width=True
        )

    # ======================
    # PORTFOLIO SIMULATOR
    # ======================

    with tab10:

        st.subheader("💰 Portfolio Simulator")

        investment = st.number_input(
            "Initial Investment Amount",
            min_value=1000,
            value=10000,
            step=1000
        )

        first_price = chart_data["Close"].iloc[0]

        last_price = chart_data["Close"].iloc[-1]

        shares = investment / first_price

        current_value = shares * last_price

        profit = current_value - investment

        roi = (profit / investment) * 100

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current Value",
                f"₹{current_value:,.2f}"
            )

        with col2:
            st.metric(
                "Profit/Loss",
                f"₹{profit:,.2f}"
            )

        with col3:
            st.metric(
                "ROI %",
                f"{roi:.2f}%"
            )

        growth_df = chart_data.copy()

        growth_df["Portfolio Value"] = (
            growth_df["Close"] / first_price
        ) * investment

        fig = px.line(
            growth_df,
            x="Date",
            y="Portfolio Value",
            title="Portfolio Growth Over Time"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
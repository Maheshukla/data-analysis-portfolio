from sklearn.ensemble import IsolationForest


def detect_anomalies(df):

    anomaly_df = df[
        [
            "win_by_runs",
            "win_by_wickets"
        ]
    ].fillna(0)

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    anomaly_df["anomaly"] = model.fit_predict(
        anomaly_df
    )

    return anomaly_df
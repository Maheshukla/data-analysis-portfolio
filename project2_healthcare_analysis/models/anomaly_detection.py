from sklearn.ensemble import IsolationForest

def detect_anomalies(df, column):

    anomaly_df = df[[column]].dropna()

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    anomaly_df["Anomaly"] = model.fit_predict(
        anomaly_df[[column]]
    )

    anomaly_df["Anomaly"] = anomaly_df[
        "Anomaly"
    ].map({
        1: "Normal",
        -1: "Anomaly"
    })

    return anomaly_df
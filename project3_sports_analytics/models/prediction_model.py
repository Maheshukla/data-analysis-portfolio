import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train_match_winner_model(df):

    required_columns = [
        "team1",
        "team2",
        "toss_winner",
        "toss_decision",
        "venue",
        "winner"
    ]

    model_df = df[
        required_columns
    ].dropna()
    model_df = model_df.astype(str)

    encoders = {}

    for col in required_columns:

        encoder = LabelEncoder()

        model_df[col] = encoder.fit_transform(
            model_df[col]
        )

        encoders[col] = encoder

    X = model_df[
        [
            "team1",
            "team2",
            "toss_winner",
            "toss_decision",
            "venue"
        ]
    ]

    y = model_df["winner"]

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    preds = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        preds
    )

    feature_importance = pd.DataFrame({

        "Feature": X.columns,

        "Importance": model.feature_importances_

    })

    return (
        model,
        encoders,
        accuracy,
        feature_importance
    )
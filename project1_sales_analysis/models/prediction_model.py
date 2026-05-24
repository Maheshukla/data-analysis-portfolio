import pandas as pd

from sklearn.model_selection import (
    train_test_split
)

from sklearn.preprocessing import (
    LabelEncoder
)

from sklearn.ensemble import (
    GradientBoostingRegressor
)

from sklearn.metrics import (
    r2_score,
    mean_absolute_error
)

def train_model(df):

    ml_df = df.copy()

    required_cols = [

        "Patient Age",

        "Patient Gender",

        "Patient Race",

        "Department Referral",

        "Patient Satisfaction Score",

        "Patient Waittime"

    ]

    ml_df = ml_df[
        required_cols
    ].dropna()

    label_encoders = {}

    categorical_cols = [

        "Patient Gender",

        "Patient Race",

        "Department Referral"

    ]

    for col in categorical_cols:

        le = LabelEncoder()

        ml_df[col] = le.fit_transform(
            ml_df[col]
        )

        label_encoders[col] = le

    X = ml_df.drop(
        "Patient Waittime",
        axis=1
    )

    y = ml_df[
        "Patient Waittime"
    ]

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,
        test_size=0.2,
        random_state=42

    )

    model = GradientBoostingRegressor(

        n_estimators=300,

        learning_rate=0.05,

        max_depth=5,

        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    y_pred = model.predict(
        X_test
    )

    r2 = r2_score(
        y_test,
        y_pred
    )

    mae = mean_absolute_error(
        y_test,
        y_pred
    )

    return (

        model,

        label_encoders,

        X,

        r2,

        mae

    )
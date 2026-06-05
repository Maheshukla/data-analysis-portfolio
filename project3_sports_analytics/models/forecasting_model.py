import pandas as pd

from sklearn.linear_model import LinearRegression


def forecast_matches(df):

    season_df = (
        df.groupby("season")
        .size()
        .reset_index(name="matches")
    )

    season_df = season_df.reset_index()

    X = season_df[["index"]]

    y = season_df["matches"]

    model = LinearRegression()

    model.fit(X, y)

    next_season = [[
        len(season_df)
    ]]

    prediction = model.predict(
        next_season
    )[0]

    return (
        season_df,
        round(prediction)
    )
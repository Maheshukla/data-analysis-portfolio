import sqlite3
import pandas as pd


def create_connection(df):

    conn = sqlite3.connect(
        ":memory:",
        check_same_thread=False
    )

    df.to_sql(
        "cricket_data",
        conn,
        if_exists="replace",
        index=False
    )

    return conn
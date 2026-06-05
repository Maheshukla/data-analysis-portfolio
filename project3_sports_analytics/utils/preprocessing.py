import pandas as pd


# =========================
# CLEAN COLUMN NAMES
# =========================

def clean_columns(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


# =========================
# CONVERT DATE COLUMN
# =========================

def convert_date_column(
    df,
    column_name
):

    if column_name in df.columns:

        df[column_name] = pd.to_datetime(
            df[column_name],
            errors="coerce"
        )

    return df


# =========================
# HANDLE MISSING VALUES
# =========================

def handle_missing_values(df):

    for col in df.columns:

        if df[col].dtype == "object":

            df[col] = df[col].fillna(
                "Unknown"
            )

        else:

            df[col] = df[col].fillna(
                0
            )

    return df


# =========================
# STANDARDIZE TEAM NAMES
# =========================

def standardize_team_names(df):

    replacements = {

        "Delhi Daredevils":
        "Delhi Capitals",

        "Kings XI Punjab":
        "Punjab Kings"

    }

    for col in [

        "team1",
        "team2",
        "winner"

    ]:

        if col in df.columns:

            df[col] = (
                df[col]
                .replace(replacements)
            )

    return df


# =========================
# MASTER PREPROCESSOR
# =========================

def preprocess_data(
    df,
    date_column=None
):

    df = clean_columns(df)

    if date_column:

        date_column = (
            date_column
            .strip()
            .lower()
            .replace(" ", "_")
        )

        df = convert_date_column(
            df,
            date_column
        )

    df = handle_missing_values(df)

    df = standardize_team_names(df)

    return df
import pandas as pd

# =========================
# DATA PREPROCESSING
# =========================

def preprocess_data(df):

    # =========================
    # REMOVE DUPLICATES
    # =========================

    df = df.drop_duplicates()

    # =========================
    # CLEAN COLUMN NAMES
    # =========================

    df.columns = [

        col.strip()

        for col in df.columns
    ]

    # =========================
    # CLEAN GENDER VALUES
    # =========================

    if "Patient Gender" in df.columns:

        df["Patient Gender"] = (

            df["Patient Gender"]

            .astype(str)

            .str.strip()

            .replace({

                "Femaleemale": "Female",

                "Femalemale": "Female",

                "Mmale": "Male",

                "male": "Male",

                "female": "Female"
            })
        )

    # =========================
    # CLEAN RACE VALUES
    # =========================

    if "Patient Race" in df.columns:

        df["Patient Race"] = (

            df["Patient Race"]

            .astype(str)

            .str.strip()
        )

    # =========================
    # NUMERIC CONVERSIONS
    # =========================

    numeric_columns = [

        "Patient Age",

        "Patient Waittime",

        "Patient Satisfaction Score"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # =========================
    # HANDLE MISSING VALUES
    # =========================

    fill_values = {}

    if "Patient Gender" in df.columns:

        fill_values[
            "Patient Gender"
        ] = "Unknown"

    if "Patient Race" in df.columns:

        fill_values[
            "Patient Race"
        ] = "Unknown"

    if "Department Referral" in df.columns:

        fill_values[
            "Department Referral"
        ] = "Unknown"

    df = df.fillna(fill_values)

    # =========================
    # REMOVE NEGATIVE VALUES
    # =========================

    if "Patient Waittime" in df.columns:

        df = df[
            df["Patient Waittime"] >= 0
        ]

    if "Patient Age" in df.columns:

        df = df[
            df["Patient Age"] >= 0
        ]

    # =========================
    # RESET INDEX
    # =========================

    df = df.reset_index(drop=True)

    return df
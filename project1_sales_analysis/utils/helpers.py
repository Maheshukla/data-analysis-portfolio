import pandas as pd

# =========================
# SAFE COLUMN CHECK
# =========================

def column_exists(df, column_name):

    return column_name in df.columns


# =========================
# SAFE NUMERIC COLUMN
# =========================

def safe_numeric_column(df, column_name):

    if column_name in df.columns:

        return pd.to_numeric(
            df[column_name],
            errors="coerce"
        )

    return None


# =========================
# SAFE CATEGORY VALUES
# =========================

def safe_category_values(df, column_name):

    if column_name in df.columns:

        return (
            df[column_name]
            .dropna()
            .unique()
            .tolist()
        )

    return []


# =========================
# SAFE COLUMN FILTER
# =========================

def safe_filter(df, column_name, selected_values):

    if column_name not in df.columns:

        return df

    if not selected_values:

        return df

    return df[
        df[column_name].isin(selected_values)
    ]


# =========================
# SAFE MEAN
# =========================

def safe_mean(df, column_name):

    if column_name in df.columns:

        return round(
            pd.to_numeric(
                df[column_name],
                errors="coerce"
            ).mean(),
            2
        )

    return 0


# =========================
# SAFE MAX
# =========================

def safe_max(df, column_name):

    if column_name in df.columns:

        return pd.to_numeric(
            df[column_name],
            errors="coerce"
        ).max()

    return 0


# =========================
# SAFE MIN
# =========================

def safe_min(df, column_name):

    if column_name in df.columns:

        return pd.to_numeric(
            df[column_name],
            errors="coerce"
        ).min()

    return 0
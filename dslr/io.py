import pandas as pd


def read_csv(file: str) -> pd.DataFrame:
    return pd.read_csv(file)


def extract_numeric_features(df: pd.DataFrame) -> dict[str, list[float]]:
    numeric_df = df.select_dtypes(include=["number"])
    if "Index" in numeric_df.columns:
        numeric_df = numeric_df.drop(columns=["Index"])

    return {col: numeric_df[col].astype(float).tolist() for col in numeric_df.columns}


def read_numeric_csv(file: str) -> dict[str, list[float]]:
    try:
        df = read_csv(file)
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        raise ValueError(f"Invalid or empty CSV: {e}") from e

    data = extract_numeric_features(df)
    if not data:
        raise ValueError("No numeric features found in dataset")
    return data

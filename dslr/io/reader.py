import pandas as pd


def read_csv(file: str) -> pd.DataFrame:
    """Read a CSV file into a pandas DataFrame."""
    return pd.read_csv(file)


def extract_numeric_features(df: pd.DataFrame) -> dict[str, list[float]]:
    """Extract numeric columns from a DataFrame, excluding 'Index', as lists of floats."""
    numeric_df = df.select_dtypes(include=["number"])
    if "Index" in numeric_df.columns:
        numeric_df = numeric_df.drop(columns=["Index"])

    return {col: numeric_df[col].astype(float).tolist() for col in numeric_df.columns}

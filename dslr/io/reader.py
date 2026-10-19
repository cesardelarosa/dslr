import pandas as pd


def read_csv(file: str) -> dict[str, dict[str, float]]:
    df = pd.read_csv(file)
    numeric_df = df.select_dtypes(include=["number"])

    if "Index" in numeric_df.columns:
        numeric_df = numeric_df.drop(columns=["Index"])

    return {col: numeric_df[col].astype(float).tolist() for col in numeric_df.columns}

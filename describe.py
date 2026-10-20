import math
import sys

from dslr.io.reader import extract_numeric_features, read_csv
from dslr.math.calc_describe import (
    calc_g1,
    calc_g2,
    calc_mad,
    calc_mean,
    calc_percentile,
    calc_std,
    calc_z,
)


def describe_feature(raw_data: list[float]) -> dict[str, float]:
    clean_data = [x for x in raw_data if math.isfinite(x)]
    n = len(clean_data)
    nan_count = len(raw_data) - n

    mu = calc_mean(clean_data, count=n)
    std = calc_std(clean_data, count=n, mean=mu)

    sorted_data = sorted(clean_data)
    val_min = sorted_data[0] if n > 0 else float("nan")
    val_max = sorted_data[-1] if n > 0 else float("nan")
    rank = val_max - val_min if n > 0 else float("nan")

    p25 = calc_percentile(sorted_data, 0.25, count=n)
    p50 = calc_percentile(sorted_data, 0.5, count=n)
    p75 = calc_percentile(sorted_data, 0.75, count=n)
    iqr = p75 - p25 if n > 0 else float("nan")

    z = calc_z(clean_data, count=n, mean=mu, std=std)
    mad = calc_mad(clean_data, count=n, mean=mu)
    g1 = calc_g1(clean_data, count=n, z=z)
    g2 = calc_g2(clean_data, count=n, z=z)

    return {
        "Count": float(n),
        "Mean": mu,
        "Std": std,
        "Min": val_min,
        "25%": p25,
        "50%": p50,
        "75%": p75,
        "Max": val_max,
        "NaNs": float(nan_count),
        "Range": rank,
        "IQR": iqr,
        "MAD": mad,
        "g1": g1,
        "g2": g2,
    }


def describe(data: dict[str, list[float]]) -> dict[str, dict[str, float]]:
    return {ft: describe_feature(values) for ft, values in data.items()}


def print_describe(summary: dict[str, dict[str, float]]) -> None:
    if not summary:
        return

    features = list(summary.keys())
    metrics = list(next(iter(summary.values())).keys())

    header = [""] + features
    rows = [
        [m]
        + [
            "NaN" if math.isnan(summary[f][m]) else f"{summary[f][m]:.6f}"
            for f in features
        ]
        for m in metrics
    ]
    table = [header] + rows

    col_widths = [max(len(cell) for cell in col) + 3 for col in zip(*table)]
    for row in table:
        print("".join(f"{cell:>{w}}" for cell, w in zip(row, col_widths)))


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 describe.py <dataset.csv>\n")
        sys.exit(1)

    csv_path = sys.argv[1]
    try:
        df = read_csv(csv_path)
    except Exception as e:
        sys.stderr.write(f"Error reading {csv_path}: {e}\n")
        sys.exit(1)

    data = extract_numeric_features(df)
    processed_data = describe(data)
    print_describe(processed_data)


if __name__ == "__main__":
    main()

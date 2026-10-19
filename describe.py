import math
import sys

from dslr.io.reader import read_csv
from dslr.math.calc_describe import calc_mean, calc_percentile, calc_std


def describe_feature(raw_data: list[float]) -> dict[str, float]:

    clean_data = [x for x in raw_data if math.isfinite(x)]
    n = len(clean_data)
    mu = calc_mean(clean_data, count=n)
    std = calc_std(clean_data, count=n, mean=mu)

    sorted_data = sorted(clean_data)
    min = sorted_data[0]
    max = sorted_data[n - 1]
    p25 = calc_percentile(sorted_data, 0.25)
    p50 = calc_percentile(sorted_data, 0.5)
    p75 = calc_percentile(sorted_data, 0.75)

    nan_count = len(raw_data) - n
    rank = max - min
    iqr = p75 - p25

    return {
        "Count": n,
        "Mean": mu,
        "Std": std,
        "Min": min,
        "25%": p25,
        "50%": p50,
        "75%": p75,
        "Max": max,
        "NaNs": nan_count,
        "Range": rank,
        "IQR": iqr,
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
    data = read_csv(csv_path)
    processed_data = describe(data)
    print_describe(processed_data)


if __name__ == "__main__":
    main()

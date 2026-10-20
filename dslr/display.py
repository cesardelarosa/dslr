import math


def print_summary(summary: dict[str, dict[str, float]]) -> None:
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

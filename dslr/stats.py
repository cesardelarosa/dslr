import math


def mean(x: list[float], count: int | None = None) -> float:
    n = count if count is not None else len(x)
    if n <= 0:
        return float("nan")
    return sum(x) / n


def std(
    x: list[float], mean_val: float | None = None, count: int | None = None
) -> float:
    n = count if count is not None else len(x)
    if n <= 1:
        return float("nan")

    mu = mean_val if mean_val is not None else mean(x, count=n)
    if math.isnan(mu):
        return float("nan")

    variance = sum((xi - mu) ** 2 for xi in x) / (n - 1)
    if math.isnan(variance):
        return float("nan")

    return math.sqrt(max(0.0, variance))


def percentile(sorted_list: list[float], p: float, count: int | None = None) -> float:
    n = count if count is not None else len(sorted_list)
    if n <= 0 or math.isnan(p) or not (0.0 <= p <= 1.0):
        return float("nan")
    if n == 1:
        return sorted_list[0]

    rank = p * (n - 1)
    low = math.floor(rank)
    high = math.ceil(rank)
    weight = rank - low

    return sorted_list[low] * (1.0 - weight) + sorted_list[high] * weight


def mad(
    x: list[float],
    count: int | None = None,
    mean_val: float | None = None,
) -> float:
    n = count if count is not None else len(x)
    if n <= 0:
        return float("nan")

    mu = mean_val if mean_val is not None else mean(x, count=n)
    if math.isnan(mu):
        return float("nan")

    return sum(abs(xi - mu) for xi in x) / n


def standardize(
    x: list[float],
    count: int | None = None,
    mean_val: float | None = None,
    std_val: float | None = None,
) -> list[float]:
    n = count if count is not None else len(x)
    if n <= 0:
        return []

    mu = mean_val if mean_val is not None else mean(x, count=n)
    s = std_val if std_val is not None else std(x, mean_val=mu, count=n)

    if s == 0.0 or math.isnan(s) or math.isnan(mu):
        return [float("nan")] * n

    return [(xi - mu) / s for xi in x]


def skewness(z: list[float], count: int | None = None) -> float:
    n = count if count is not None else len(z)
    if n < 3:
        return float("nan")

    sum_z3 = sum(zi**3 for zi in z)
    if math.isnan(sum_z3):
        return float("nan")

    coeff = n / ((n - 1) * (n - 2))
    return coeff * sum_z3


def kurtosis(z: list[float], count: int | None = None) -> float:
    n = count if count is not None else len(z)
    if n < 4:
        return float("nan")

    sum_z4 = sum(zi**4 for zi in z)
    if math.isnan(sum_z4):
        return float("nan")

    term1 = (n * (n + 1) / ((n - 1) * (n - 2) * (n - 3))) * sum_z4
    term2 = (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))
    return term1 - term2


def describe_feature(raw_data: list[float]) -> dict[str, float]:
    clean_data = [x for x in raw_data if math.isfinite(x)]
    n = len(clean_data)
    nan_count = len(raw_data) - n

    mu = mean(clean_data, count=n)
    s = std(clean_data, count=n, mean_val=mu)

    sorted_data = sorted(clean_data)
    val_min = sorted_data[0] if n > 0 else float("nan")
    val_max = sorted_data[-1] if n > 0 else float("nan")
    data_range = val_max - val_min if n > 0 else float("nan")

    p25 = percentile(sorted_data, 0.25, count=n)
    p50 = percentile(sorted_data, 0.5, count=n)
    p75 = percentile(sorted_data, 0.75, count=n)
    iqr = p75 - p25 if n > 0 else float("nan")

    z = standardize(clean_data, count=n, mean_val=mu, std_val=s)
    mad_val = mad(clean_data, count=n, mean_val=mu)
    g1 = skewness(z, count=n)
    g2 = kurtosis(z, count=n)

    return {
        "Count": float(n),
        "Mean": mu,
        "Std": s,
        "Min": val_min,
        "25%": p25,
        "50%": p50,
        "75%": p75,
        "Max": val_max,
        "NaNs": float(nan_count),
        "Range": data_range,
        "IQR": iqr,
        "MAD": mad_val,
        "g1": g1,
        "g2": g2,
    }


def describe(data: dict[str, list[float]]) -> dict[str, dict[str, float]]:
    return {ft: describe_feature(values) for ft, values in data.items()}

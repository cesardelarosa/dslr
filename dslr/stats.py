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


def z_score(
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

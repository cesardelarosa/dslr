import math


def calc_mean(x: list[float], count: int | None = None) -> float:
    n = count if count is not None else len(x)
    if n <= 0:
        return float("nan")
    return sum(x) / n


def calc_std(
    x: list[float], mean: float | None = None, count: int | None = None
) -> float:
    n = count if count is not None else len(x)
    if n <= 1:
        return float("nan")

    mu = mean if mean is not None else calc_mean(x, count=n)
    if math.isnan(mu):
        return float("nan")

    variance = sum((xi - mu) ** 2 for xi in x) / (n - 1)
    if math.isnan(variance):
        return float("nan")

    return math.sqrt(max(0.0, variance))


def calc_percentile(
    sorted_list: list[float], percentile: float, count: int | None = None
) -> float:
    n = count if count is not None else len(sorted_list)
    if n <= 0 or math.isnan(percentile) or not (0.0 <= percentile <= 1.0):
        return float("nan")
    if n == 1:
        return sorted_list[0]

    rank = percentile * (n - 1)
    low = math.floor(rank)
    high = math.ceil(rank)
    weight = rank - low

    return sorted_list[low] * (1.0 - weight) + sorted_list[high] * weight


def calc_mad(
    x: list[float],
    count: int | None = None,
    mean: float | None = None,
) -> float:
    n = count if count is not None else len(x)
    if n <= 0:
        return float("nan")

    mu = mean if mean is not None else calc_mean(x, count=n)
    if math.isnan(mu):
        return float("nan")

    return sum(abs(xi - mu) for xi in x) / n


def calc_zi(xi: float, mean: float, std: float) -> float:
    if std == 0.0 or math.isnan(std) or math.isnan(mean) or math.isnan(xi):
        return float("nan")
    return (xi - mean) / std


def calc_z(
    x: list[float],
    count: int | None = None,
    mean: float | None = None,
    std: float | None = None,
) -> list[float]:
    n = count if count is not None else len(x)
    if n <= 0:
        return []

    mu = mean if mean is not None else calc_mean(x, count=n)
    s = std if std is not None else calc_std(x, mean=mu, count=n)

    if s == 0.0 or math.isnan(s) or math.isnan(mu):
        return [float("nan")] * n

    return [(xi - mu) / s for xi in x]


def calc_g1(
    x: list[float],
    count: int | None = None,
    mean: float | None = None,
    std: float | None = None,
    z: list[float] | None = None,
) -> float:
    n = count if count is not None else (len(z) if z is not None else len(x))
    if n < 3:
        return float("nan")

    if z is None:
        mu = mean if mean is not None else calc_mean(x, count=n)
        s = std if std is not None else calc_std(x, mean=mu, count=n)
        if s == 0.0 or math.isnan(s) or math.isnan(mu):
            return float("nan")
        z = calc_z(x, count=n, mean=mu, std=s)

    sum_z3 = sum(zi**3 for zi in z)
    if math.isnan(sum_z3):
        return float("nan")

    coeff = n / ((n - 1) * (n - 2))
    return coeff * sum_z3


def calc_g2(
    x: list[float],
    count: int | None = None,
    mean: float | None = None,
    std: float | None = None,
    z: list[float] | None = None,
) -> float:
    n = count if count is not None else (len(z) if z is not None else len(x))
    if n < 4:
        return float("nan")

    if z is None:
        mu = mean if mean is not None else calc_mean(x, count=n)
        s = std if std is not None else calc_std(x, mean=mu, count=n)
        if s == 0.0 or math.isnan(s) or math.isnan(mu):
            return float("nan")
        z = calc_z(x, count=n, mean=mu, std=s)

    sum_z4 = sum(zi**4 for zi in z)
    if math.isnan(sum_z4):
        return float("nan")

    term1 = (n * (n + 1) / ((n - 1) * (n - 2) * (n - 3))) * sum_z4
    term2 = (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))
    return term1 - term2

import math


def calc_mean(x: list[float], count: int | None = None) -> float:
    n = count if count is not None else len(x)
    if n == 0:
        return float("nan")
    return sum(x) / n


def calc_std(
    x: list[float], mean: float | None = None, count: int | None = None
) -> float:
    n = count if count is not None else len(x)
    if n <= 1:
        return float("nan")

    mu = mean if mean is not None else calc_mean(x, n)

    variance = sum((xi - mu) ** 2 for xi in x) / (n - 1)
    return math.sqrt(variance)


def calc_percentile(
    sorted_list: list[float], percentile: float, count: int | None = None
) -> float:
    n = count if count is not None else len(sorted_list)
    if n == 0:
        return float("nan")
    if n == 1:
        return sorted_list[0]

    rank = percentile * (n - 1)
    low = math.floor(rank)
    high = math.ceil(rank)
    weight = rank - low

    return sorted_list[low] * (1.0 - weight) + sorted_list[high] * weight


def calc_mad(x: list[float], count: int, mean: float) -> float:
    mad = sum(abs(xi - mean) for xi in x) / count
    return mad


def calc_g1(x: list[float], count: int, mean: float, std: float) -> float:
    pass


def calc_g2(x: list[float], count: int, mean: float, std: float) -> float:
    pass

import math

def calc_mean(x: list[float], count: int | None = None) -> float:
    n = count if count is not None else len(x)
    if n == 0:
        return float("nan")
    return sum(x) / n

def calc_std(
    x: list[float],
    mean: float | None = None,
    count: int | None = None
    ) -> float:
    n = count if count is not None else len(x)
    if n <= 1:
        return float("nan")
    mu = mean if mean is not None else calc_mean(x, n)
    variance = sum((xi - mu) ** 2 for xi in x) / (n - 1)
    return math.sqrt(variance)

def main():
    pass

if __name__ == "__main__":
    main()
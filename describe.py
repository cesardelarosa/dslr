import sys

from dslr.display import print_summary
from dslr.io import read_numeric_csv
from dslr.stats import describe


def main() -> None:
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 describe.py <dataset.csv>\n")
        sys.exit(1)

    try:
        data = read_numeric_csv(sys.argv[1])
        summary = describe(data)
        print_summary(summary)
    except (OSError, ValueError) as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

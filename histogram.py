import sys

from dslr.io import read_csv
from dslr.plot import plot_course_histogram


def main(): 
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 histogram.py <dataset.csv>\n")
        sys.exit(1)

    try:
        df = read_csv(sys.argv[1])
        plot_course_histogram(df)

    except (OSError, ValueError) as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
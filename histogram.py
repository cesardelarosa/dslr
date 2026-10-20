import math
import sys

import matplotlib.pyplot as plt

from dslr.io import read_csv

HG = "Hogwarts House"

def main(): 
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 histogram.py <dataset.csv>\n")
        sys.exit(1)

    try:
        df = read_csv(sys.argv[1])
        houses = df[HG].dropna().unique().tolist()
        courses = [
            col for col in df.select_dtypes(include="number").columns
            if col != "Index"
        ]
        m = len(courses)
        n = math.ceil(math.sqrt(m))
        house_dfs = {house: sub_df for house, sub_df in df.groupby(HG)}
        fig, axes = plt.subplots(nrows=n, ncols=n)
        axes = axes.flatten()
        for ax, course in zip(axes, courses):
            for house in houses:
                scores = house_dfs[house][course].dropna()
                ax.hist(scores, alpha=0.5, label=house)
                ax.set_title(course)

        for j in range(m, n**2):
            fig.delaxes(axes[j])

        plt.show()
    except (OSError, ValueError) as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
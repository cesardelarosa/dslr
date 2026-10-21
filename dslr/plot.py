import math

import matplotlib.pyplot as plt
import pandas as pd

HOUSE_COLORS: dict[str, str] = {
    "Gryffindor": "#ae0001",
    "Hufflepuff": "#f0c75e",
    "Ravenclaw": "#222f5b",
    "Slytherin": "#2a623d",
}

HG = "Hogwarts House"

plt.rcParams.update(
    {
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "figure.titlesize": 16,
        "figure.titleweight": "bold",
        "figure.figsize": (16, 10)
    }
)


def plot_course_histogram(df: pd.DataFrame) -> None:
    houses = df[HG].dropna().unique().tolist()
    courses = [
        col for col in df.select_dtypes(include="number").columns if col != "Index"
    ]

    n_courses = len(courses)
    n_rows = math.floor(math.sqrt(n_courses))
    n_cols = math.ceil(n_courses / n_rows)

    house_dfs = {house: sub_df for house, sub_df in df.groupby(HG)}
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols)
    axes = axes.flatten()
    for ax, course in zip(axes, courses):
        col_data = df[course].dropna()
        r_min, r_max = col_data.min(), col_data.max()

        for house in houses:
            scores = house_dfs[house][course].dropna()
            ax.hist(
                scores,
                bins=10,
                range=(r_min, r_max),
                alpha=0.6,
                label=house,
                color=HOUSE_COLORS[house],
            )
        ax.set_title(course)
        ax.set_xlabel("Score")
        ax.set_ylabel("Number of students")

    handles, labels = axes[0].get_legend_handles_labels()

    fig.legend(handles, labels, loc="lower right")
    fig.subplots_adjust(
        left=0.05, right=0.95, bottom=0.05, top=0.90, wspace=0.35, hspace=0.45
    )
    fig.suptitle("Courses Scores Histogram per Hogwarts House")

    for j in range(n_courses, n_rows * n_cols):
        fig.delaxes(axes[j])

    plt.show()

import pandas as pd
import matplotlib.pyplot as plt


def get_ratings_barplot(df: pd.DataFrame):
    value_counts = df.groupby("rating").count().reset_index().iloc[:, :2]
    value_counts = value_counts.rename(columns={value_counts.columns[1]: "count"})
    all_values = pd.DataFrame({"rating": range(1, 6)})
    merged_data = all_values.merge(value_counts, how="left", on="rating")
    merged_data["count"] = merged_data["count"].fillna(0)
    fig, ax = plt.subplots()
    ax.bar(merged_data["rating"], merged_data["count"])
    ax.set_xlabel("Rating")
    ax.set_ylabel("Frequency")
    ax.set_title("Frecuency of Ratings")
    return fig, ax

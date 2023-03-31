import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

df_results = pd.read_csv("../../results/20212022/results.csv", sep=";")

print(df_results.head())
models_color = {}
for i, model in enumerate(df_results.model_class.unique()):
    models_color[model] = [
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red",
        "tab:purple",
        "tab:brown",
        "tab:pink",
        "tab:grey",
        "tab:olive",
        "tab:cyan",
    ][i]
fig, ax = plt.subplots()
for n_row, row in df_results.iterrows():
    if n_row < 200:
        rect = Rectangle(
            (n_row, 0),
            1,
            row["precision"]*100,
            edgecolor=models_color[row["model_class"]],
            facecolor=models_color[row["model_class"]],
            label=row["model_class"],
        )
        ax.add_patch(rect)

ax.autoscale()
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc=1)
plt.ylabel("Precision %")
plt.savefig("models_performances.png")
plt.show()

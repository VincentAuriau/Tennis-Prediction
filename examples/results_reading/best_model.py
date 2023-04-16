import os

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd

df_results = pd.read_csv("../../results/20212022_/results.csv", sep=";")

best_row = df_results.iloc[df_results.precision.argmax()]
print(best_row)

eval_id = best_row["eval_ID"]
best_results = pd.read_csv(
    os.path.join("../../results/20212022_", f"{eval_id}.csv"), sep=";"
)

fig, ax = plt.subplots()
df_ww = best_results.loc[best_results.Winner == 0].loc[best_results.y_pred == 0]
plt.scatter(df_ww.diff_rank, df_ww.Winner, c="tab:pink", label="Well Predicted")
df_wl = best_results.loc[best_results.Winner == 0].loc[best_results.y_pred == 1]
plt.scatter(df_wl.diff_rank, df_wl.Winner + 0.1, c="tab:blue", label="Predicted Wrong")
df_ll = best_results.loc[best_results.Winner == 1].loc[best_results.y_pred == 1]
plt.scatter(df_ll.diff_rank, df_ll.Winner, c="tab:orange", label="Well Wrong")
df_lw = best_results.loc[best_results.Winner == 1].loc[best_results.y_pred == 0]
plt.scatter(df_lw.diff_rank, df_lw.Winner - 0.1, c="tab:red", label="Predicted Wrong")
plt.legend()

plt.xlabel("Rank Player 0 - Rank Player 1")
plt.ylabel("Winner")
plt.show()

# Let's evaluate Symmetry
symmetric_same_results = 0
for i in range(int(len(best_results) / 2)):
    if best_results.iloc[2 * i]["y_pred"] != best_results.iloc[2 * i + 1]["y_pred"]:
        symmetric_same_results += 1
print(
    f"{(symmetric_same_results / (len(best_results) / 2))} Results are symmetrically predicted"
)

rank_categories = [1, 10, 50, 100, 300, 1000, 9999]

prediction_percentage = []

for cat_1 in range(len(rank_categories) - 1):
    lines = []
    nb_matches_lines = []
    for cat_2 in range(len(rank_categories) - 1):
        sub_df = best_results.loc[best_results.Ranking_1 >= rank_categories[cat_1]].loc[
            best_results.Ranking_1 < rank_categories[cat_1 + 1]
        ]
        sub_df = sub_df.loc[sub_df.Ranking_2 >= rank_categories[cat_2]].loc[
            sub_df.Ranking_2 < rank_categories[cat_2 + 1]
        ]
        sub_df["best_rank"] = sub_df.apply(
            lambda row: np.argmin([row["Ranking_1"], row["Ranking_2"]]), axis=1
        )

        if len(sub_df) > 0:
            best_player_w_p = np.sum(
                sub_df.Winner.values == sub_df.y_pred.values
            ) / len(sub_df)

        else:
            best_player_w_p = 0
        lines.append(best_player_w_p)
        nb_matches_lines.append(len(sub_df) / 2)
    prediction_percentage.append(lines)

colors = ["purple", "blue", "cyan", "green", "yellow", "orange", "red"]
fig, ax = plt.subplots()

for i, val1 in enumerate(prediction_percentage):
    for j, val2 in enumerate(val1):
        color = colors[int(val2 * (len(colors) - 1))]
        rect = plt.Rectangle((i, j), 1, 1, fc=color)
        ax.add_patch(rect)
        plt.text(i + 0.2, j + 0.35, np.round(val2 * 100, 2))

for i in range(len(rank_categories)):
    plt.plot([i, i], [0, len(rank_categories) - 1], c="k")
    plt.plot([0, len(rank_categories) - 1], [i, i], c="k")

plt.xticks(list(range(len(rank_categories))), labels=rank_categories)
plt.yticks(list(range(len(rank_categories))), labels=rank_categories)
plt.xlabel("Player 1 Rank Category")
plt.ylabel("Player 2 Rank Category")
plt.title("Precision Percentage")
plt.savefig("precision_percentage_players_ranks.png")
plt.show()

best_ranked_player_wins_results = pd.read_csv(
    os.path.join(
        "../../results/20212022_",
        f"{df_results.loc[df_results.model_class=='BestRankedPlayerWins'].eval_ID.values[0]}.csv",
    ),
    sep=";",
)
ticks = []
fig, ax = plt.subplots()
for surface, surface_code in {"Clay": 0, "Carpet": 1, "Hard": 2, "Grass": 3}.items():
    precision_model = best_results.loc[best_results.tournament_surface == surface_code]
    precision_brpw = best_ranked_player_wins_results.loc[
        best_ranked_player_wins_results.tournament_surface == surface_code
    ]

    if len(precision_model) > 0:
        precision_model = len(
            precision_model.loc[precision_model.y_pred == precision_model.Winner]
        ) / len(precision_model)
        prec_brpw = 0
        for n_row, row in precision_brpw.iterrows():
            if int(row["y_pred"][1]) == row["Winner"]:
                prec_brpw += 1
        precision_brpw = prec_brpw / len(precision_brpw)
    else:
        precision_model = 0
        precision_brpw = 0
    rect = Rectangle(
        (surface_code * 2, 0),
        1,
        precision_model,
        edgecolor="k",
        facecolor="tab:blue",
        label="Model - XGBoost",
    )
    ax.add_patch(rect)
    rect = Rectangle(
        (surface_code * 2 + 1, 0),
        1,
        precision_brpw,
        edgecolor="k",
        facecolor="tab:pink",
        label="Best Ranked Player Wins",
    )
    ax.add_patch(rect)
    ticks.append(surface)

ax.autoscale()
plt.xticks([1, 3, 5, 7], labels=ticks)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc=4)
plt.title("Win % for each surface")
plt.savefig("win_per_surface.png")
plt.show()

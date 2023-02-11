import os, sys

sys.path.append("../python")
sys.path.append("../")

import matplotlib.pyplot as plt
import numpy as np

from data.data_loader import matches_data_loader

data_df = matches_data_loader(
    path_to_data="../submodules/tennis_atp",
    path_to_cache="../cache",
    flush_cache=False,
    keep_values_from_year=2015,
    get_match_statistics=True,
    get_reversed_match_data=True,
)

print(data_df.head())
print(data_df.shape)

# Categories of Ranks : 1 - 10 - 50 - 100 - 300 - 1000
categories = [1, 10, 50, 100, 300, 1000, 9999]

best_ranked_player_win_percentage = []
categories_number_of_matches = []

for cat_1 in range(len(categories) - 1):
    lines = []
    nb_matches_lines = []
    for cat_2 in range(len(categories) - 1):
        sub_df = data_df.loc[data_df.Ranking_1 >= categories[cat_1]].loc[
            data_df.Ranking_1 < categories[cat_1 + 1]
        ]
        sub_df = sub_df.loc[sub_df.Ranking_2 >= categories[cat_2]].loc[
            sub_df.Ranking_2 < categories[cat_2 + 1]
        ]
        sub_df["best_rank"] = sub_df.apply(
            lambda row: np.argmin([row["Ranking_1"], row["Ranking_2"]]), axis=1
        )

        if len(sub_df) > 0:
            best_player_w_p = np.sum(
                sub_df.Winner.values == sub_df.best_rank.values
            ) / len(sub_df)

        else:
            best_player_w_p = 0
        lines.append(best_player_w_p)
        nb_matches_lines.append(len(sub_df) / 2)
    best_ranked_player_win_percentage.append(lines)
    categories_number_of_matches.append(nb_matches_lines)

colors = ["purple", "blue", "cyan", "green", "yellow", "orange", "red"]
fig, ax = plt.subplots()

for i, val1 in enumerate(best_ranked_player_win_percentage):
    for j, val2 in enumerate(val1):
        color = colors[int(val2 * (len(colors) - 1))]
        rect = plt.Rectangle((i, j), 1, 1, fc=color)
        ax.add_patch(rect)
        plt.text(i + 0.2, j + 0.35, np.round(val2 * 100, 2))

for i in range(len(categories)):
    plt.plot([i, i], [0, len(categories) - 1], c="k")
    plt.plot([0, len(categories) - 1], [i, i], c="k")

plt.xticks(list(range(len(categories))), labels=categories)
plt.yticks(list(range(len(categories))), labels=categories)
plt.xlabel("Player 1 Rank Category")
plt.ylabel("Player 2 Rank Category")
plt.title("Best player Win percentage per Rank Category")
plt.savefig("Best_player_win_percentage.png")
plt.show()


fig, ax = plt.subplots()

for i, val1 in enumerate(categories_number_of_matches):
    for j, val2 in enumerate(val1):
        color = colors[int(val2**0.5 / np.max(categories_number_of_matches)**0.5 * (len(colors) - 1))]
        rect = plt.Rectangle((i, j), 1, 1, fc=color)
        ax.add_patch(rect)
        plt.text(i + 0.2, j + 0.35, np.round(val2 * 100, 2))

for i in range(len(categories)):
    plt.plot([i, i], [0, len(categories) - 1], c="k")
    plt.plot([0, len(categories) - 1], [i, i], c="k")

plt.xticks(list(range(len(categories))), labels=categories)
plt.yticks(list(range(len(categories))), labels=categories)
plt.xlabel("Player 1 Rank Category")
plt.ylabel("Player 2 Rank Category")
plt.title("Number of matches recorded per Rank Category")
plt.savefig("nb_matches.png")
plt.show()

import ast
import os, sys

sys.path.append("../../python")
sys.path.append("../../")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd

from data.data_loader import matches_data_loader


data_df = matches_data_loader(
    path_to_data="../../submodules/tennis_atp",  # Path to tennis_atp submodule, keep as is if repo cloned with subdmodule
    path_to_cache="../../cache",  # Path to caching directory
    flush_cache=False,  # Whether or not to flush a potentially existing cache. Set to True if you want to create the data from scratch
    keep_values_from_year=2002,  # Returned data will date back to January 2002 up to today
    get_match_statistics=True,  # Whether to also retrun match statistics (time, score, etc...)
    get_reversed_match_data=True,  # Whether to duplicate the mathc row and exchange winner and loser positions
    include_davis_cup=True,  # Whether or not to include davis cup matches
    match_type=[
        "main_atp",
        "qualifying_challengers",
    ],  # Which match to keep. You can look at tennis_atp submodule to see possibilities
)

print(data_df.head())
print(data_df.shape)

# Creation of first figure
# Win percentages considering the ranks of players

# Rank categories
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
print(
    "Number of matches with player ranked 0:", len(data_df.loc[data_df.Ranking_1 == 0])
)
print(
    "Number of matches with player ranked > 9999:",
    len(data_df.loc[data_df.Ranking_1 > 9999]),
)

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

# Second figure
# Number of matches considering players ranks
fig, ax = plt.subplots()

for i, val1 in enumerate(categories_number_of_matches):
    for j, val2 in enumerate(val1):
        color = colors[
            int(
                val2**0.5
                / np.max(categories_number_of_matches) ** 0.5
                * (len(colors) - 1)
            )
        ]
        rect = plt.Rectangle((i, j), 1, 1, fc=color)
        ax.add_patch(rect)
        plt.text(i + 0.2, j + 0.35, int(val2))

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

#### Stan the man
# Statistics analysis of Stan Wawrinka over time
overall_v = []
last_hundred_v = []

overall_clay = []
overall_carpet = []
overall_grass = []
overall_hard = []

wins_clay = []
wins_carpet = []
wins_grass = []
wins_hard = []

dates = []
stan_df = data_df.loc[data_df.ID_1 == 104527]
stan_df = stan_df.reset_index()

stan_df.iloc[100].to_csv("single_row_example.csv")

for n_row, row in stan_df.iterrows():
    matches = [r[0] for r in ast.literal_eval(str(row["Matches_1"]))]

    if len(matches) > 0:
        overall_v.append(matches.count("V") / len(matches) * 100)
        last_hundred_v.append(matches[-100:].count("V") / len(matches[-100:]) * 100)

        if str(row["tournament_date"])[:4] not in [d[0] for d in dates]:
            dates.append((str(row["tournament_date"])[:4], n_row))
        overall_clay.append(row["Clay_Victories_Percentage_1"])
        overall_grass.append(row["Grass_Victories_Percentage_1"])
        overall_hard.append(row["Hard_Victories_Percentage_1"])
        overall_carpet.append(row["Carpet_Victories_Percentage_1"])

    wins_clay.append(list(row.Matches_Clay_1).count("V"))
    wins_carpet.append(list(row.Matches_Carpet_1).count("V"))
    wins_grass.append(list(row.Matches_Grass_1).count("V"))
    wins_hard.append(list(row.Matches_Hard_1).count("V"))

# % Victory over time and surfaces
plt.figure()
plt.plot(overall_v, label="overall")
plt.plot(last_hundred_v, label="last 100 matches")
plt.plot(overall_clay, label="overall clay")
plt.plot(overall_grass, label="overall grass")
plt.plot(overall_hard, label="overall hard")
plt.plot(overall_carpet, label="overall carpet")
plt.legend()
plt.xticks([d[1] for d in dates], [d[0] for d in dates], rotation="vertical")
plt.title("Stanislas Wawrinka win percentage on main ATP tournamnents")
plt.savefig("stan_the_man_win_percentage.png")
plt.show()


fig, ax1 = plt.subplots()
ax1.plot(overall_v, label="overall", c="k")
ax1.plot(last_hundred_v, label="last 100 matches", c="purple")
ax1.plot(overall_clay, label="overall clay", c="orange")
ax1.plot(overall_grass, label="overall grass", c="green")
ax1.plot(overall_hard, label="overall hard", c="blue")
ax1.plot(overall_carpet, label="overall carpet", c="gray")
ax1.set_ylabel("Win %")
plt.legend()

ax2 = ax1.twinx()
for i, (wcarpet, wgrass, wclay, whard) in enumerate(
    zip(wins_carpet, wins_grass, wins_clay, wins_hard)
):
    if i % 2 == 0:
        ax2.add_patch(
            Rectangle(
                (i, 0),
                width=2,
                height=wcarpet,
                edgecolor=None,
                facecolor="gray",
                alpha=0.2,
            )
        )
        ax2.add_patch(
            Rectangle(
                (i, wcarpet),
                width=2,
                height=wgrass,
                edgecolor=None,
                facecolor="green",
                alpha=0.2,
            )
        )
        ax2.add_patch(
            Rectangle(
                (i, wcarpet + wgrass),
                width=2,
                height=wclay,
                edgecolor=None,
                facecolor="orange",
                alpha=0.2,
            )
        )
        ax2.add_patch(
            Rectangle(
                (i, wcarpet + wgrass + wclay),
                width=2,
                height=whard,
                edgecolor=None,
                facecolor="blue",
                alpha=0.2,
            )
        )

ax2.set_yticks([0, 100, 200, 300, 400, 500, 600, 700])
ax2.set_ylabel("Number of victory for each surface")
plt.tight_layout()
ax1.set_xticks([d[1] for d in dates], [d[0] for d in dates], rotation="vertical")
plt.title("Stanislas Wawrinka victories on ATP tournamnents")
plt.savefig("stan_the_man_win_percentage.png")
plt.show()


aces = {"diff_aces": [], "winner": []}

for n_row, row in stan_df.iterrows():
    diff_aces = row["Aces_Percentage_1"] - row["Aces_Percentage_2"]
    winner = row["Winner"]
    aces["diff_aces"].append(diff_aces)
    aces["winner"].append(winner)

aces = pd.DataFrame(aces)
classes = [val * 2.5 for val in range(-6, 4, 1)]
fig, ax = plt.subplots(1)
for min_class, max_class in zip(classes[:-1], classes[1:]):
    values = aces.loc[aces.diff_aces < max_class].loc[aces.diff_aces > min_class]
    ax.add_patch(
        Rectangle(
            xy=(min_class, 0),
            width=2.5,
            height=len(values.loc[values.winner == 0]),
            edgecolor="k",
            facecolor="blue",
            label="Victory",
        )
    )
    ax.add_patch(
        Rectangle(
            xy=(min_class, len(values.loc[values.winner == 0])),
            width=2.5,
            height=len(values.loc[values.winner == 1]),
            edgecolor="k",
            facecolor="orange",
            label="Defeat",
        )
    )
ax.autoscale_view()
ax.set_xlabel("Career ace percentage difference with adversary")
ax.set_ylabel("Number of matches")
ax.set_title(
    "Histogram of career aces percentage difference for Stan Wawrinka, colored by match results",
    wrap=True,
)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.savefig("stanimal_aces_percentage_difference.png")
plt.show()

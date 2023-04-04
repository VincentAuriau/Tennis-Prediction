import ast
import os, sys

sys.path.append("../../python")
sys.path.append("../../")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

from data.data_loader import matches_data_loader
from history_modeling.match_representation import get_match_info, matches_info_norm

data_df = matches_data_loader(
    path_to_data="../../submodules/tennis_atp",
    path_to_cache="../../cache",
    flush_cache=False,
    keep_values_from_year=2023,
    get_match_statistics=True,
    get_reversed_match_data=True,
)

ten_matches_history = pd.concat(
    [get_match_info(data_df.iloc[i]) for i in range(len(data_df))], axis=0
)
ten_matches_history.reset_index(inplace=True, drop=True)
match_info = matches_info_norm(ten_matches_history, "20230401")

match_info = match_info.dropna().reset_index(drop=True)

X = match_info.values
pca = PCA(n_components=2)
X_r = pca.fit(X).transform(X)

plt.figure(figsize=(20, 12))

plt.subplot(2, 4, 1)
v_i = match_info.loc[match_info.result == 0].index.values
d_i = match_info.loc[match_info.result == 1].index.values
plt.scatter(X_r[v_i, 0], X_r[v_i, 1], label="Victories")
plt.scatter(X_r[d_i, 0], X_r[d_i, 1], label="Defeats")
plt.legend()
plt.title("Result")

plt.subplot(2, 4, 2)
c_i = match_info.loc[match_info.surface == 0.0].index.values
h_i = match_info.loc[match_info.surface == 2 / 3].index.values
g_i = match_info.loc[match_info.surface == 1.0].index.values
plt.scatter(X_r[c_i, 0], X_r[c_i, 1], label="Clay")
plt.scatter(X_r[h_i, 0], X_r[h_i, 1], label="Hard")
plt.scatter(X_r[g_i, 0], X_r[g_i, 1], label="Grass")
plt.legend()
plt.title("Surface")

plt.subplot(2, 4, 3)
plt.scatter(X_r[:, 0], X_r[:, 1], c=match_info.num_played_minutes)
plt.title("played minutes")

plt.subplot(2, 4, 4)
plt.scatter(X_r[:, 0], X_r[:, 1], c=match_info.adv_ranking)
plt.title("Ranking Adversary")

plt.subplot(2, 4, 5)
plt.scatter(X_r[:, 0], X_r[:, 1], c=match_info.num_won_sets)
plt.title("Won sets Number")
plt.subplot(2, 4, 6)
plt.scatter(X_r[:, 0], X_r[:, 1], c=match_info.num_lost_sets)
plt.title("Lost set Number")
plt.subplot(2, 4, 7)
plt.scatter(X_r[:, 0], X_r[:, 1], c=match_info.num_won_games)
plt.title("Won games Number")
plt.subplot(2, 4, 8)
plt.scatter(X_r[:, 0], X_r[:, 1], c=match_info.num_lost_games)
plt.title("Lost games Number")

plt.savefig("2d_pca_match_representation.png")
plt.show()


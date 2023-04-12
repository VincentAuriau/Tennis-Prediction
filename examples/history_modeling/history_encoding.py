import ast
import os, sys

sys.path.append("../../python")
sys.path.append("../../")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

from data.data_loader import matches_data_loader
from history_modeling.match_representation import create_timeless_dataset, create_dataset
from history_modeling.encoding_model import PCAMatchEncoder

from data.data_encoding import create_encoded_history

data_df = matches_data_loader(
    path_to_data="../../submodules/tennis_atp",
    path_to_cache="../../cache",
    flush_cache=False,
    keep_values_from_year=2022,
    get_match_statistics=True,
    get_reversed_match_data=True,
    include_davis_cup=False
)

columns = ["surface", "result", "adv_ranking", "adv_ranking_points", "num_won_sets",
           "num_lost_sets", "num_won_games", "num_lost_games", "num_tie_break_wons", "num_tie_break_lost"]
model = PCAMatchEncoder(num_pca_features=2, columns=columns)
model.fit(data_df, transform_data=True)

X_r, match_info = model.predict(data_df, transform_data=True)

history_df = create_encoded_history(data_df, model, 5)
history_df = pd.merge(data_df, history_df, on="id")
history_df = history_df.loc[history_df.tournament_year == 2023]
history_df.to_csv("history_df.csv", sep=";", index=False)

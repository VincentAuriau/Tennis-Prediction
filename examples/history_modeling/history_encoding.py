import ast
import os, sys

sys.path.append("../../python")
sys.path.append("../../")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data.data_loader import matches_data_loader
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

print("Data Loaded")
columns = ["surface", "result", "adv_ranking", "adv_ranking_points", "num_won_sets",
           "num_lost_sets", "num_won_games", "num_lost_games", "num_tie_break_wons", "num_tie_break_lost"]
model = PCAMatchEncoder(num_pca_features=2, columns=columns)
model.fit(data_df, transform_data=True)

print("Model Fitted, now predicting")
X_r, match_info = model.predict(data_df, transform_data=True)

history_df = create_encoded_history(data_df, model, 5)

cols = ['history_1', 'history_2']
print(pd.DataFrame(np.array(history_df["history_1"].values.tolist()).reshape((len(history_df), -1)).tolist()))
print(np.array(history_df["history_1"].values.tolist()).reshape((len(history_df), -1)).shape)
flatten_data = pd.concat([pd.DataFrame(np.array(history_df["history_1"].values.tolist()).reshape((len(history_df), -1)).tolist()).add_prefix(x) for x in cols], axis=1)
flatten_data.to_csv("flatten_data.csv", sep=";", index=False)
encoded_data = pd.concat([flatten_data, history_df.drop(cols, axis=1)], axis=1)
history_df = pd.merge(data_df, encoded_data, on=["id", "ID_1", "ID_2"])
history_df = history_df.loc[history_df.tournament_year == 2023]
history_df.to_csv("history_df.csv", sep=";", index=False)

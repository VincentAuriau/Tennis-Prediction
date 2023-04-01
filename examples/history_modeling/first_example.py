import ast
import os, sys

sys.path.append("../../python")
sys.path.append("../../")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd

from data.data_loader import matches_data_loader
from history_modeling.match_representation import get_match_info,  matches_info_norm

data_df = matches_data_loader(
    path_to_data="../../submodules/tennis_atp",
    path_to_cache="../../cache",
    flush_cache=False,
    keep_values_from_year=2023,
    get_match_statistics=True,
    get_reversed_match_data=True,
)

data_df = data_df.loc[data_df.ID_1 == 105173] # Adrian Mannarino
print(f"Adrian Mannarino has played {len(data_df)} matches in 2023 in our database")

ten_matches_history = pd.concat([get_match_info(data_df.iloc[i]) for i in range(10)], axis=0)
ten_matches_history.reset_index(inplace=True, drop=True)
match_info = matches_info_norm(ten_matches_history, data_df.iloc[10]["tournament_date"])

print(match_info.columns)
plt.figure()
plt.imshow(match_info.values)
plt.show()

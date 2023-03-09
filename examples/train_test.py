import os, sys

sys.path.append("../python")
sys.path.append("../")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from data.data_loader import matches_data_loader
from data.data_loader import encode_data

data_df = matches_data_loader(
    path_to_data="../submodules/tennis_atp",
    path_to_cache="../cache",
    flush_cache=False,
    keep_values_from_year=2022,
    get_match_statistics=True,
    get_reversed_match_data=False,
)

forgotten_columns = ["Versus_1", "Best_Rank_1", "Last_Tournament_Date"]

columns_m = [
    "tournament_level",
    "round",
    "best_of",
]
columns_1 = [
    "ID_1",
    "Ranking_1",
    "Ranking_Points_1",
    "Hand_1",
    "Height_1",
    "Versus_1",
    "Victories_Percentage_1",
    "Clay_Victories_Percentage_1",
    "Grass_Victories_Percentage_1",
    'Carpet_Victories_Percentage_1',
    'Hard_Victories_Percentage_1',
    "Aces_Percentage_1",
    "Doublefaults_Percentage_1",
    "First_Serve_Success_Percentage_1",
    "Winning_on_1st_Serve_Percentage_1",
    "Winning_on_2nd_Serve_Percentage_1",
    "Overall_Win_on_Serve_Percentage_1",
    "BreakPoint_Face_Percentage_1",
    "BreakPoint_Saved_Percentage_1",
    "Fatigue_1",
]
columns_2 = [
    "ID_2",
    "Ranking_2",
    "Ranking_Points_2",
    "Hand_2",
    "Height_2",
    "Versus_2",
    "Victories_Percentage_2",
    "Clay_Victories_Percentage_2",
    "Grass_Victories_Percentage_2",
    "Carpet_Victories_Percentage_2",
    "Hard_Victories_Percentage_2",
    "Aces_Percentage_2",
    "Doublefaults_Percentage_2",
    "First_Serve_Success_Percentage_2",
    "Winning_on_1st_Serve_Percentage_2",
    "Winning_on_2nd_Serve_Percentage_2",
    "Overall_Win_on_Serve_Percentage_2",
    "BreakPoint_Face_Percentage_2",
    "BreakPoint_Saved_Percentage_2",
    "Fatigue_2",
]

data_df = data_df[columns_m + columns_1 + columns_2]

print(data_df.head())
print(data_df.shape)

data_df = data_df[columns_m+columns_1+columns_2]
data_df = data_df.dropna(axis=0)
fdf = encode_data(data_df)
fdf.to_csv("../cache/test.csv")

fdf1 = fdf[columns_m + columns_1 + columns_2]
fdf2 = fdf[columns_m + columns_2 + columns_1]
fdf = pd.concat([fdf1, fdf2], axis=0)

fdf = fdf.drop(["ID_1", "Versus_1", "ID_2", "Versus_2"], axis=1)
X = fdf.values

y = np.concatenate([[0] * len(fdf1), [1] * len(fdf2)])
print(X)

model = RandomForestClassifier(n_estimators=1000, max_depth=7)
print("FIT")
print(X.shape, y.shape)
model.fit(X, y)

y_pred = model.predict(X)
print(len(y), np.sum(y == y_pred))
print(y_pred)
print(np.sum(y_pred))

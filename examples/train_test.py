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
    keep_values_from_year=2015,
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
    "Ranking Points_1",
    "Hand_1",
    "Height_1",
    "Versus_1",
    "Victories Percentage_1",
    "Clay victories Percentage_1",
    "Grass victories Percentage_1",
    "Aces Percentage_1",
    "Doublefaults Percentage_1",
    "First Serve Success Percentage_1",
    "Winning on 1st Serve Percentage_1",
    "Winning on 2nd Serve Percentage_1",
    "Overall Win on Serve Percentage_1",
    "BreakPoint Face Percentage_1",
    "BreakPoint Saved Percentage_1",
    "Fatigue_1",
]
columns_2 = [
    "ID_2",
    "Ranking_2",
    "Ranking Points_2",
    "Hand_2",
    "Height_2",
    "Versus_2",
    "Victories Percentage_2",
    "Clay victories Percentage_2",
    "Grass victories Percentage_2",
    "Aces Percentage_2",
    "Doublefaults Percentage_2",
    "First Serve Success Percentage_2",
    "Winning on 1st Serve Percentage_2",
    "Winning on 2nd Serve Percentage_2",
    "Overall Win on Serve Percentage_2",
    "BreakPoint Face Percentage_2",
    "BreakPoint Saved Percentage_2",
    "Fatigue_2",
]

data_df = data_df[columns_m + columns_1 + columns_2]

print(data_df.head())
print(data_df.shape)

print(encode_data(data_df.iloc[:10]))
fdf = encode_data(data_df)
fdf.to_csv("../cache/test.csv")

fdf1 = fdf[columns_m + columns_1 + columns_2]
fdf2 = fdf[columns_m + columns_2 + columns_1]
fdf = pd.concat([fdf1, fdf2], axis=0)
fdf.dropna(axis=0)

fdf = fdf.drop(["ID_1", "Versus_1", "ID_2", "Versus_2"], axis=1)
X = fdf.values
y = np.concatenate([[0] * len(fdf1), [1] * len(fdf2)])
print(X)
model = RandomForestClassifier(n_estimators=5000)
print("FIT")
print(X.shape, y.shape)
model.fit(X, y)

y_pred = model.predict(X)
print(len(y), np.sum(y == y_pred))

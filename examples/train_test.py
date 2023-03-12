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
    get_reversed_match_data=True,
)

forgotten_columns = ["Versus_1", "Best_Rank_1", "Last_Tournament_Date"]

columns_m = [
    "tournament_level",
    "round",
    "best_of",
    "Winner"
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

fdf = fdf.drop(["ID_1", "Versus_1", "ID_2", "Versus_2"], axis=1)
fdf["diff_ranking"] = fdf["Ranking_2"] - fdf["Ranking_1"]

y = fdf.Winner

fdf = fdf[["diff_ranking"]]
X = fdf.values

print(X)

model = RandomForestClassifier(n_estimators=1000, max_depth=None)
print("FIT")
print(X.shape, y.shape)
model.fit(X, y)

y_pred = model.predict(X)
print(len(y), np.sum(y == y_pred))
print(y_pred)
print(y)
print(np.sum(y_pred))

plt.figure()
plt.scatter(X, y)
plt.show()
"""
z = model.predict(np.expand_dims(list(range(-10000, 10001)), axis=1))
plt.figure()
plt.plot(list(range(-10000, 10001)), z)
plt.show()
"""
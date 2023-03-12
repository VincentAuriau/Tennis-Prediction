import os, sys

sys.path.append("../python")
sys.path.append("../")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from data.data_loader import matches_data_loader
from data.data_loader import encode_data
from evaluation.train_test import train_test_evaluation


train_years = [2022]
test_years = [2023]
model_class = RandomForestClassifier
model_params = {"n_estimators": 2000, "max_depth": None}
match_features = []
player_features = ["Ranking"]

test_score = train_test_evaluation(
    train_years=train_years,
    test_years=test_years,
    model_class=model_class,
    model_params=model_params,
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
)

print("Test Score", test_score)

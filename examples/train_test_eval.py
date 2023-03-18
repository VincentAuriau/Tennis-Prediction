import os, sys

sys.path.append("../python")
sys.path.append("../")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from data.data_loader import matches_data_loader
from data.data_loader import encode_data
from evaluation.train_test import train_test_evaluation


train_years = [2020, 2021]
test_years = [2022, 2023]


model_class = RandomForestClassifier
model_params = {"n_estimators": 2000, "max_depth": None}
match_features = []
player_features = ["Ranking"]
additional_features = ["diff_rank"]

test_score = train_test_evaluation(
    train_years=train_years,
    test_years=test_years,
    model_class=model_class,
    model_params=model_params,
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
)

print("Test Score", test_score)


model_class = RandomForestClassifier
model_params = {"n_estimators": 2000, "max_depth": None}
match_features = []
player_features = ["Ranking"]
additional_features = []

test_score = train_test_evaluation(
    train_years=train_years,
    test_years=test_years,
    model_class=model_class,
    model_params=model_params,
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
)

print("Test Score", test_score)


model_class = RandomForestClassifier
model_params = {"n_estimators": 2000, "max_depth": None}
match_features = []
player_features = []
additional_features = ["diff_rank"]

test_score = train_test_evaluation(
    train_years=train_years,
    test_years=test_years,
    model_class=model_class,
    model_params=model_params,
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
)

print("Test Score", test_score)


model_class = RandomForestClassifier
model_params = {"n_estimators": 1, "max_depth": 1}
match_features = []
player_features = []
additional_features = ["diff_rank"]

test_score = train_test_evaluation(
    train_years=train_years,
    test_years=test_years,
    model_class=model_class,
    model_params=model_params,
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
)

print("Test Score", test_score)


model_class = GradientBoostingClassifier
model_params = {"n_estimators": 100, "learning_rate": 1.0, "max_depth": 1}
match_features = []
player_features = []
additional_features = ["diff_rank"]

test_score = train_test_evaluation(
    train_years=train_years,
    test_years=test_years,
    model_class=model_class,
    model_params=model_params,
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
)

print("Test Score", test_score)


model_class = GradientBoostingClassifier
model_params = {"n_estimators": 1000, "learning_rate": 0.1, "max_depth": 4}
match_features = []
player_features = []
additional_features = ["diff_rank"]

test_score = train_test_evaluation(
    train_years=train_years,
    test_years=test_years,
    model_class=model_class,
    model_params=model_params,
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
)

print("Test Score", test_score)

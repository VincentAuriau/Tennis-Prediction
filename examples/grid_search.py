import os, sys

sys.path.append("../python")
sys.path.append("../")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from model.dumb_models import BestRankedPlayerWins
from model.lgbm import LightGBM
from model.sk_model import ScalerSVC

from data.data_loader import matches_data_loader
from data.data_loader import encode_data
from evaluation.train_test import train_test_evaluation


train_years = [2018, 2019, 2020]
test_years = [2021, 2022]


match_features = ["tournament_surface", "tournament_level"]
player_features = [
    "Ranking",
    "Ranking_Points",
    "Height",
    "Victories_Percentage",
    "Clay_Victories_Percentage",
    "Grass_Victories_Percentage",
    "Carpet_Victories_Percentage",
    "Hard_Victories_Percentage",
    "Aces_Percentage",
]
additional_features = ["diff_rank", "v_perc_versus"]


test_score = train_test_evaluation(
    train_years=train_years,
    test_years=test_years,
    model_class=BestRankedPlayerWins,
    model_params={},
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
    save_path="../results/201820192020_20212022",
)

lgbm_hyperparams = []
for num_leaves in [10, 100, 1000, 2000]:
    for min_data_leaf in [10, 100, 1000]:
        lgbm_hyperparams.append({"params": {
            "num_leaves": num_leaves,
            "objective": "binary",
            "min_data_in_leaf": min_data_leaf,
        }})
test_score = train_test_evaluation(
    train_years=train_years,
    test_years=test_years,
    model_class=LightGBM,
    model_params=lgbm_hyperparams,
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
    save_path="../results/20212022",
)


ada_hyperparams = []
for num_est in [10, 100, 1000, 2000]:
    for lr in [.1, 1., 2.]:
        ada_hyperparams.append({
            "n_estimators": num_est,
            "learning_rate": lr,
        })
test_score = train_test_evaluation(
    train_years=train_years,
    test_years=test_years,
    model_class=AdaBoostClassifier,
    model_params=ada_hyperparams,
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
    save_path="../results/20212022",
)

svc_hyperparams = []
for C in [.1, 1., 10., 100.]:
    for kernel in ["linear", "rbf"]:
        svc_hyperparams.append({
            "C": C,
            "kernel": kernel,
        })
test_score = train_test_evaluation(
    train_years=train_years,
    test_years=test_years,
    model_class=ScalerSVC,
    model_params=svc_hyperparams,
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
    save_path="../results/20212022",
)


for mx_depth in [1, 3, 5]:
    for n_est in [10, 100, 1000, 2000]:
        model_params = {"n_estimators": n_est, "max_depth": mx_depth}
        model_class = RandomForestClassifier

        test_score = train_test_evaluation(
            train_years=train_years,
            test_years=test_years,
            model_class=model_class,
            model_params=model_params,
            match_features=match_features,
            player_features=player_features,
            encoding_params={},
            additional_features=additional_features,
            save_path="../results/20212022",
        )
        print("~~ Current Score ~~", test_score)


for mx_depth in [1, 3, 5]:
    for n_est in [10, 100, 1000, 2000]:
        model_params = {"n_estimators": n_est, "max_depth": mx_depth}
        model_class = GradientBoostingClassifier

        test_score = train_test_evaluation(
            train_years=train_years,
            test_years=test_years,
            model_class=model_class,
            model_params=model_params,
            match_features=match_features,
            player_features=player_features,
            encoding_params={},
            additional_features=additional_features,
            save_path="../results/20212022",
        )
        print("~~ Current Score ~~", test_score)


test_score = train_test_evaluation(
    train_years=[2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
    test_years=test_years,
    model_class=LightGBM,
    model_params=lgbm_hyperparams,
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
    save_path="../results/20212022",
)
import os, sys

sys.path.append("../../python")
sys.path.append("../../../")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from model.xgboost import XGBoost
from history_modeling.encoding_model import PCAMatchEncoder
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
additional_features = ["diff_rank", "v_perc_versus", "nb_match_versus"]
xgb_hyperparams = {
    "params": {
        "eta": 0.3,
        "objective": "binary:logistic",
        "gamma": 10,
        "max_depth": 10,
        "min_child_weight": 8,
        "subsample": 1,
    }
}

xgb_hyperparams = []
for eta in [0.1, 0.3, 0.6]:
    for gamma in [0, 1, 10]:
        for max_depth in [2, 4, 6, 8, 10]:
            for min_child_weight in [1, 2, 8]:
                for subsample in [0.4, 0.8, 1]:
                    xgb_hyperparams.append(
                        {
                            "params": {
                                "eta": eta,
                                "objective": "binary:logistic",
                                "gamma": gamma,
                                "max_depth": max_depth,
                                "min_child_weight": min_child_weight,
                                "subsample": subsample,
                            }
                        }
                    )
test_score = train_test_evaluation(
    train_years=[2018, 2019, 2020],
    test_years=test_years,
    model_class=XGBoost,
    model_params=xgb_hyperparams,
    encoder_models=[
        (
            PCAMatchEncoder,
            {
                "num_pca_features": 2,
                "auto_transform": True,
                "columns": [
                    "surface",
                    "result",
                    "adv_ranking",
                    "adv_ranking_points",
                    "num_won_sets",
                    "num_lost_sets",
                    "num_won_games",
                    "num_lost_games",
                    "num_tie_break_wons",
                    "num_tie_break_lost",
                ],
            },
        )
    ],
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
    save_path="../../results/history_encoding",
    save_all_results=True,
)

import os, sys

sys.path.append("../python")
sys.path.append("../")

from model.deep_model import SimpleFullyConnected
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
    model_class=SimpleFullyConnected,
    model_params={"input_shape": 22,
                  "hidden_units": (22, 44, 44, 22, 11, 4),
                  "output_shape": 2,
                  "last_activation": "softmax",
                  "epochs": 100,
                  "reduced_lr_epochs": 50,
                  "loss": "categorical_crossentropy"},
    match_features=match_features,
    player_features=player_features,
    encoding_params={},
    additional_features=additional_features,
    save_path="../results/test",
    save_all_results=True
)

import matplotlib.pyplot as plt
import numpy as np

from data.data_loader import matches_data_loader
from data.data_loader import encode_data

default_columns_match = ["tournament_level", "round", "best_of"]

default_columns_player = [
    "ID",
    "Ranking",
    "Ranking_Points",
    "Hand",
    "Height",
    "Versus",
    "Victories_Percentage",
    "Clay_Victories_Percentage",
    "Grass_Victories_Percentage",
    "Carpet_Victories_Percentage",
    "Hard_Victories_Percentage",
    "Aces_Percentage",
    "Doublefaults_Percentage",
    "First_Serve_Success_Percentage",
    "Winning_on_1st_Serve_Percentage",
    "Winning_on_2nd_Serve_Percentage",
    "Overall_Win_on_Serve_Percentage",
    "BreakPoint_Face_Percentage",
    "BreakPoint_Saved_Percentage",
    "Fatigue",
]


def train_test_evaluation(
    train_years,
    test_years,
    model_class,
    model_params,
    match_features=default_columns_match,
    player_features=default_columns_player,
    encoding_params={},
):
    assert len(set(train_years).intersection(set(test_years))) == 0
    print("[+] Beginning Train/Test Evaluation")

    min_year = np.min(train_years + test_years)
    data_df = matches_data_loader(
        path_to_data="../submodules/tennis_atp",
        path_to_cache="../cache",
        flush_cache=False,
        keep_values_from_year=min_year,
        get_match_statistics=False,
        get_reversed_match_data=True,
    )

    p1_features = [feat + "_1" for feat in player_features]
    p2_features = [feat + "_2" for feat in player_features]

    data_df = data_df[
        match_features + p1_features + p2_features + ["Winner", "tournament_year"]
    ]
    train_data = data_df.loc[data_df.tournament_year.isin(train_years)]
    test_data = data_df.loc[data_df.tournament_year.isin(test_years)]

    train_data = encode_data(train_data, **encoding_params)
    test_data = encode_data(test_data, **encoding_params)

    model = model_class(**model_params)
    model.fit(
        train_data[match_features + p1_features + p2_features], train_data[["Winner"]]
    )

    preds = model.predict(test_data[match_features + p1_features + p2_features])

    return np.sum(preds == test_data["Winner"].values) / len(preds)

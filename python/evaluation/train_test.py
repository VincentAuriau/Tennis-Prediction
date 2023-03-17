import os

import numpy as np
import pandas as pd

from data.data_loader import matches_data_loader
from data.data_encoding import encode_data, create_additional_features

default_columns_match = ["tournament_level", "round", "best_of", "tournament_surface"]

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
    additional_features=[],
    save_path=None
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

    train_data = data_df.loc[data_df.tournament_year.isin(train_years)]
    test_data = data_df.loc[data_df.tournament_year.isin(test_years)]

    train_data = create_additional_features(train_data, additional_features)
    train_data = encode_data(train_data, **encoding_params)
    test_data = create_additional_features(test_data, additional_features)
    test_data = encode_data(test_data, **encoding_params)

    p1_features = [feat + "_1" for feat in player_features]
    p2_features = [feat + "_2" for feat in player_features]
    match_features.extend(additional_features)

    train_data = train_data[
        match_features + p1_features + p2_features + ["Winner", "tournament_year"]
    ]
    test_data = test_data[
        match_features + p1_features + p2_features + ["Winner", "tournament_year"]
    ]

    model = model_class(**model_params)
    model.fit(
        train_data[match_features + p1_features + p2_features], train_data["Winner"].values.ravel()
    )

    preds = model.predict(test_data[match_features + p1_features + p2_features])
    precision = np.sum(preds == test_data["Winner"].values) / len(preds)
    if save_path is not None:
        try:
            df_res = pd.read_csv(os.path.join(save_path, "results.csv"))
        except:
            os.makedirs(save_path, exist_ok=True)
            df_res = pd.DataFrame()

        df_curr = pd.DataFrame({
            "train_years": [train_years],
            "test_years": [test_years],
            "model_class": [str(model_class)],
            "model_params": [model_params],
            "match_features": [match_features],
            "player_features": [player_features],
            "encoding_params": [encoding_params],
            "additional_features": [additional_features],
            "precision": [precision]
        })

        df_res = pd.concat([df_res, df_curr], axis=1)
        df_res.to_csv(os.path.join(save_path, "results.csv"), index=False, sep=";")

    return precision

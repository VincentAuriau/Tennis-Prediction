import os
import time

import numpy as np
import pandas as pd

from data.data_loader import matches_data_loader
from data.data_encoding import (
    encode_data,
    create_additional_features,
    clean_missing_data,
    create_encoded_history,
)

absolute_path = os.path.dirname(os.path.abspath(__file__))
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
    encoder_models=[],
    history_encoder_years=1,
    match_features=default_columns_match,
    player_features=default_columns_player,
    encoding_params={},
    additional_features=[],
    save_path=None,
    save_all_results=False,
):
    global absolute_path
    assert len(set(train_years).intersection(set(test_years))) == 0
    print(f"[+] Beginning Train/Test Evaluation for model class {model_class}")

    min_year = np.min(train_years + test_years)
    min_year -= history_encoder_years
    print(f"[+] Loading Data from year {min_year}")
    data_df = matches_data_loader(
        path_to_data=os.path.join(absolute_path, "../../submodules/tennis_atp"),
        path_to_cache=os.path.join(absolute_path, "../../cache"),
        flush_cache=False,
        keep_values_from_year=min_year,
        get_match_statistics=False,
        get_reversed_match_data=True,
    )
    print(f"[+] Data Loaded, Now Encoding Data and create additional Features")

    historic_data = data_df.loc[data_df.tournament_year < min(train_years)]
    train_data = data_df.loc[data_df.tournament_year.isin(train_years)]
    test_data = data_df.loc[data_df.tournament_year.isin(test_years)]

    for (encoding_model, encoding_model_params) in encoder_models:
        print(f"[+] Training Encoder Model {encoding_model}")
        encoder = encoding_model(**encoding_model_params)
        encoder.fit(train_data)

        print(f"[+] Encoding using encoder {encoding_model}")
        encoded_data = create_encoded_history(data_df,
                                              encoder,
                                              num_matches=5,
                                              completing_value=0)
        # encoded_data = encoder.predict(pd.concat([historic_data, train_data, test_data], axis=0))
        train_data = pd.merge(train_data, encoded_data, on="id")
        # train_data = pd.concat([train_data, encoded_data.iloc[train_data.index]], axis=1)
        # print(test_data.index, encoded_data.index)
        # test_data = pd.concat([test_data, encoded_data.iloc[test_data.index]], axis=1)
        test_data = pd.merge(test_data, encoded_data, on="id")

    train_data = data_df.loc[data_df.tournament_year.isin(train_years)]
    test_data = data_df.loc[data_df.tournament_year.isin(test_years)]
    train_data = create_additional_features(train_data, additional_features)
    train_data = encode_data(train_data, **encoding_params)
    test_data = create_additional_features(test_data, additional_features)
    test_data = encode_data(test_data, **encoding_params)

    p1_features = [feat + "_1" for feat in player_features]
    p2_features = [feat + "_2" for feat in player_features]
    match_features = match_features.copy()
    match_features.extend(additional_features.copy())

    train_data = train_data[
        match_features + p1_features + p2_features + ["Winner", "tournament_year"]
    ]
    test_data = test_data[
        match_features + p1_features + p2_features + ["Winner", "tournament_year"]
    ]

    print(f"[+] Cleaning Data")
    train_data = clean_missing_data(train_data)
    test_data = clean_missing_data(test_data)
    print(f"Training on {len(train_data)} data and testing on {len(test_data)} data")

    print(f"[+] Data Ready, now beginning modelling")
    if isinstance(model_params, list):
        precisions = []
        for params_set in model_params:
            model = model_class(**params_set)
            t_fit = time.time()
            model.fit(
                train_data[match_features + p1_features + p2_features],
                train_data["Winner"].values.ravel(),
            )
            t_fit = time.time() - t_fit
            print(f"~~ Fit time: {np.round(t_fit, 0)}")

            preds = model.predict(test_data[match_features + p1_features + p2_features])
            precision = np.sum(np.squeeze(preds) == test_data["Winner"].values) / len(
                preds
            )
            precisions.append(precision)

            if save_path is not None:
                try:
                    df_res = pd.read_csv(
                        os.path.join(save_path, "results.csv"), sep=";"
                    )
                except:
                    print("save file not found")
                    os.makedirs(save_path, exist_ok=True)
                    df_res = pd.DataFrame()

                df_curr = pd.DataFrame(
                    {
                        "train_years": [train_years],
                        "test_years": [test_years],
                        "model_class": [model_class.__name__],
                        "model_params": [params_set],
                        "match_features": [match_features],
                        "player_features": [player_features],
                        "encoding_params": [encoding_params],
                        "additional_features": [additional_features.copy()],
                        "precision": [precision],
                        "fit_time": [np.round(t_fit, 0)],
                    }
                )

                if save_all_results:
                    eval_id = int(time.time() * 100)
                    df_curr["eval_ID"] = [eval_id]
                    test_data["y_pred"] = preds
                    test_data.to_csv(
                        os.path.join(save_path, f"{eval_id}.csv"), index=False, sep=";"
                    )

                df_res = pd.concat([df_res, df_curr], axis=0)
                df_res.to_csv(
                    os.path.join(save_path, "results.csv"), index=False, sep=";"
                )

        return precisions

    else:
        model = model_class(**model_params)
        t_fit = time.time()
        model.fit(
            train_data[match_features + p1_features + p2_features],
            train_data["Winner"].values.ravel(),
        )
        t_fit = time.time() - t_fit
        print(f"~~ Fit time: {np.round(t_fit, 0)}")


        print(f"[+] Fit ended, now predicting on test set")
        preds = model.predict(test_data[match_features + p1_features + p2_features])
        precision = np.sum(np.squeeze(preds) == test_data["Winner"].values) / len(preds)
        if save_path is not None:
            try:
                df_res = pd.read_csv(os.path.join(save_path, "results.csv"), sep=";")
            except:
                print("save file not found")
                os.makedirs(save_path, exist_ok=True)
                df_res = pd.DataFrame()

            df_curr = pd.DataFrame(
                {
                    "train_years": [train_years],
                    "test_years": [test_years],
                    "model_class": [model_class.__name__],
                    "model_params": [model_params],
                    "encoder_models": [encoder_models],
                    "history_encoder_years": [history_encoder_years],
                    "match_features": [match_features],
                    "player_features": [player_features],
                    "encoding_params": [encoding_params],
                    "additional_features": [additional_features.copy()],
                    "precision": [precision],
                    "fit_time": [np.round(t_fit, 0)],
                }
            )
            if save_all_results:
                print(f"[+] Saving Results")
                eval_id = int(time.time())
                df_curr["eval_ID"] = [eval_id]
                test_data["y_pred"] = preds
                test_data.to_csv(
                    os.path.join(save_path, f"{eval_id}.csv"), index=False, sep=";"
                )

            df_res = pd.concat([df_res, df_curr], axis=0)
            df_res.to_csv(os.path.join(save_path, "results.csv"), index=False, sep=";")

        return precision

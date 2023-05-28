import os
import sys

sys.path.append("../../python")
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
from history_modeling.encoding_model import IdentityEncoder
from model.deep_model import ConvolutionalHistoryAndFullyConnected


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

data_df = matches_data_loader(
    path_to_data=os.path.join(absolute_path, "../../submodules/tennis_atp"),
    path_to_cache=os.path.join(absolute_path, "../../cache"),
    flush_cache=False,
    keep_values_from_year=2022,
    get_match_statistics=False,
    get_reversed_match_data=True,
    include_davis_cup=False,
)
print(f"[+] Data Loaded, Now Encoding Data and create additional Features")
print(data_df.head())
print(data_df.columns)


history_columns = []
encoder_models = [(IdentityEncoder, {})]
for encoding_model, encoding_model_params in encoder_models:
    print(f"[+] Training Encoder Model {encoding_model}")
    encoder = encoding_model(**encoding_model_params)
    encoder.fit(data_df)

    print(f"[+] Encoding using encoder {encoding_model}")
    encoded_data = create_encoded_history(
        data_df, encoder, num_matches=5, completing_value=0
    )

    cols = ["history_1", "history_2"]

    flatten_data = pd.concat(
        [
            pd.DataFrame(
                np.array(encoded_data[x].values.tolist()).reshape(
                    (len(encoded_data), -1)
                )
            ).add_prefix(x)
            for x in cols
        ],
        axis=1,
    )
    encoded_data = pd.concat(
        [flatten_data, encoded_data.drop(cols, axis=1)], axis=1
    )
    enc_columns = encoded_data.columns
    enc_columns = list(set(enc_columns) - set(["id", "ID_1", "ID_2"]))
    history_columns.extend(enc_columns)

    data_df = pd.merge(data_df, encoded_data, on=["id", "ID_1", "ID_2"])

print(data_df.head())
print(data_df.columns)

model = ConvolutionalHistoryAndFullyConnected(num_history_signals=22, **{"output_shape": 2,
        "last_activation": "softmax",
        "epochs": 10,
        "reduced_lr_epochs": 10,
        "loss": "categorical_crossentropy"})
# model.instantiate_model()

print(model.model.summary())
print(model.summary())

print(data_df.head())

hist_cols = []
non_hist_cols = []
for col in data_df.columns:
    if "history" in col:
        hist_cols.append(col)
    else :
        non_hist_cols.append(col)
print(data_df[hist_cols])
print(data_df[hist_cols].head())

model.fit(data_df[["Ranking_1", "Ranking_2"]].values, data_df[hist_cols].values.reshape((len(data_df), 5, 22)), data_df["Winner"].values)

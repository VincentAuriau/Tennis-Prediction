import os
import sys

import matplotlib.pyplot as plt

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
    complete_missing_data,
)
from history_modeling.encoding_model import IdentityEncoder
from model.deep_model import ConvolutionalHistoryAndFullyConnected


absolute_path = os.path.dirname(os.path.abspath(__file__))
match_features = ["tournament_surface", "tournament_level", "round"]
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
encoding_params = {}

data_df = matches_data_loader(
    path_to_data=os.path.join(absolute_path, "../../submodules/tennis_atp"),
    path_to_cache=os.path.join(absolute_path, "../../cache"),
    flush_cache=False,
    keep_values_from_year=2022,
    get_match_statistics=True,
    get_reversed_match_data=True,
    include_davis_cup=False,
)
print(f"[+] Data Loaded, Now Encoding Data and create additional Features")
print(data_df.head())
print(data_df.columns)

# data_df = pd.concat([data_df.iloc[:1000], data_df.iloc[-1000:]])

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
    encoded_data = pd.concat([flatten_data, encoded_data.drop(cols, axis=1)], axis=1)
    enc_columns = encoded_data.columns
    enc_columns = list(set(enc_columns) - set(["id", "ID_1", "ID_2"]))
    history_columns.extend(enc_columns)

    data_df = pd.merge(data_df, encoded_data, on=["id", "ID_1", "ID_2"])

train_data = data_df.loc[data_df.tournament_year.isin([2022])]
test_data = data_df.loc[data_df.tournament_year.isin([2023])]
# train_data = data_df.loc[data_df.tournament_year.isin([2019, 2020, 2021])]
# test_data = data_df.loc[data_df.tournament_year.isin([2022, 2023])]
train_data = create_additional_features(train_data, additional_features)
train_data = encode_data(train_data, **encoding_params)
test_data = create_additional_features(test_data, additional_features)
test_data = encode_data(test_data, **encoding_params)

p1_features = [feat + "_1" for feat in player_features]
p2_features = [feat + "_2" for feat in player_features]
match_features = match_features.copy()

train_data_ = train_data[
    match_features + p1_features + p2_features + ["Winner", "tournament_year"]
]
test_data_ = test_data[
    match_features + p1_features + p2_features + ["Winner", "tournament_year"]
]

# train_data_ = clean_missing_data(train_data_)
# test_data_ = clean_missing_data(test_data_)

print(data_df.head())
print(data_df.columns)

model = ConvolutionalHistoryAndFullyConnected(
    num_history_signals=22,
    **{
        "input_shape": 23,
        "hidden_units": (22, 44, 22, 11, 4),
        "output_shape": 2,
        "last_activation": "softmax",
        "epochs": 100,
        "reduced_lr_epochs": 50,
        "loss": "categorical_crossentropy",
    },
)
# model.instantiate_model()

print(model.summary())

print(data_df.head())

hist_cols = []
for col in data_df.columns:
    if "history" in col:
        hist_cols.append(col)

print(len(train_data), len(hist_cols))

model.fit(
    train_data_.values,
    train_data[hist_cols].values.reshape((len(train_data), 5, 22)),
    train_data["Winner"].values,
)

y_pred = model.predict(
    test_data_.values, test_data[hist_cols].values.reshape((len(test_data), 5, 22))
)


print(np.sum(y_pred == test_data["Winner"]))

plt.plot(y_pred)
plt.show()

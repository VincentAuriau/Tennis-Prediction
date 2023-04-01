import os, sys

sys.path.append("../../python")
sys.path.append("../../")

import numpy as np

from data.data_loader import matches_data_loader
from model.dumb_models import RandomModel, BestRankedPlayerWins

data_df = matches_data_loader(
    path_to_data="../submodules/tennis_atp",
    path_to_cache="../cache",
    flush_cache=True,
    keep_values_from_year=2021,
    get_match_statistics=False,
)

random_model = RandomModel()
best_player_model = BestRankedPlayerWins()

random_predictions = []
best_player_predictions = []
ground_truths = []
for n_row, row in data_df.iterrows():
    r_prediction = random_model.predict(row)
    bp_prediction = best_player_model.predict(row)
    truth = row["Winner"]

    random_predictions.append(r_prediction)
    best_player_predictions.append(bp_prediction)
    ground_truths.append(truth)

ground_truths = np.array(ground_truths)
random_predictions = np.squeeze(np.array(random_predictions))
best_player_predictions = np.squeeze(best_player_predictions)

print("Among the", len(ground_truths), "matches analyzed, we have found:")

random_percentage = (
    np.sum(ground_truths == random_predictions) / len(random_predictions) * 100
)
print("Random Prediction Percentage:", np.round(random_percentage, 2), "%")
bp_percentage = (
    np.sum(ground_truths == best_player_predictions)
    / len(best_player_predictions)
    * 100
)
print("Best Ranked Player Prediction Percentage:", np.round(bp_percentage, 2), "%")

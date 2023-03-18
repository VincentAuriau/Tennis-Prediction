from abc import abstractmethod

import numpy as np


class DumbModel:
    def __init__(self):
        pass

    @abstractmethod
    def predict(self, X):
        pass


class BestRankedPlayerWins(DumbModel):
    def fit(self, X, y):
        pass

    def predict(self, X):
        y_pred = []
        for n_row, row in X.iterrows():
            rank_1 = row["Ranking_1"]
            rank_2 = row["Ranking_2"]
            y_pred.append([np.argmin([rank_1, rank_2])])
        return y_pred


class RandomModel(DumbModel):
    def predict(self, X):
        return np.random.randint(0, 2, 1)

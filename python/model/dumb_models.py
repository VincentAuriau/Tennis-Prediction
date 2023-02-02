from abc import abstractmethod

import numpy as np

class DumbModel:

    def __init__(self):
        pass

    @abstractmethod
    def predict(self, X):
        pass


class BestRankedPlayerWins(DumbModel):

    def predict(self, X):
        rank_1 = X["Ranking_1"]
        rank_2 = X["Ranking_2"]

        return np.argmin([rank_1, rank_2])

class RandomModel(DumbModel):

    def predict(self, X):
        return np.random.randint(0, 2, 1)

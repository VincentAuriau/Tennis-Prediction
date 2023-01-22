import numpy as np
import pandas as pd

class DumbModel:

    def __init__(self):
        pass

    @abstractmethod
    def predict(self, X):
        pass


class BestRankedPlayerWins(DumbModel):

    def predict(self, X):
        rank_1 = X["rank_1"]
        rank_2 = X["rank_2"]

        return np.armax([rank_1, rank_2])

class RandomModel(DumbModel):

    def predict(self, X):
        return np.random.randint(0, 1, 1)
    
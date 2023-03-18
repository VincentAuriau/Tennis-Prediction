import lightgbm as lgb
import numpy as np

from model.base_model import BaseModel


class LightGBM(BaseModel):
    def __init__(self, params, num_rounds=10):
        self.params = params
        self.num_rounds = num_rounds

    def fit(self, X, y):
        train_data = lgb.Dataset(X, label=y)
        self.model = lgb.train(self.params, train_data, self.num_rounds)
        return self.model

    def predict(self, X):
        return np.round(self.model.predict(X), 0)

    def save(self, path):
        self.model.save_model(path)

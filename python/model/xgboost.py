import xgboost as xgb
import numpy as np

from model.base_model import BaseModel


class XGBoost(BaseModel):
    def __init__(self, params, num_rounds=10):
        self.params = params
        self.num_rounds = num_rounds

    def fit(self, X, y, validation_data=None):
        train_data = xgb.DMatrix(X, label=y)
        if validation_data is not None:
            evallist = [(train_data, 'train'), (xgb.DMatrix(validation_data[0], label=validation_data[1]), 'eval')]
        else:
            evallist = []
        self.model = xgb.train(self.params, train_data, self.num_rounds, evals=evallist)
        return self.model

    def predict(self, X):
        X = xgb.DMatrix(X)
        return np.round(self.model.predict(X), 0)

    def save(self, path):
        self.model.save_model(path)

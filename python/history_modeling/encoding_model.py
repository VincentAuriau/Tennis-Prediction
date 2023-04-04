from abc import abstractmethod

import pandas as pd
from sklearn.decomposition import PCA

from history_modeling.match_representation import create_timeless_dataset


class MatchEncoder:

    def __init__(self, num_match_differences):
        self.num_match_differences = num_match_differences

    def select_data(self, X):
        assert isinstance(X, pd.DataFrame)

        X_transformed = create_timeless_dataset(X)
        X_transformed = X_transformed.dropna().reset_index(drop=True)
        return X_transformed

    @abstractmethod
    def predict(self, match_row):
        pass


class PCAMatchEncoder(MatchEncoder):

    def __init__(self, num_pca_features, auto_transform=False):
        self.num_pca_features = num_pca_features
        self.auto_transform = auto_transform

        self.model = self.instantiate_model()

    def instantiate_model(self):
        model = PCA(n_components=self.num_pca_features)
        return model

    def fit(self, X, transform_data=False):
        if transform_data or self.auto_transform:
            X = self.select_data(X)
        self.model.fit(X)

    def predict(self, X, transform_data=False):
        if transform_data or self.auto_transform:
            X = self.select_data(X)
            return self.model.transform(X), X
        else:
            return self.model.transform(X)

    def save_model(self):
        pass

class MatchesHistoryEncoder:

    def __init__(self, num_historic_matches, match_encoder):
        self.num_historic_matches = num_historic_matches
        self.match_encoder = match_encoder

    def select_data(self, X):
        return X

    @abstractmethod
    def predict(self, match_row):
        pass

from abc import abstractmethod

import pandas as pd
from sklearn.decomposition import PCA

from history_modeling.match_representation import create_timeless_dataset


class MatchEncoder:
    def __init__(self, num_match_differences):
        self.num_match_differences = num_match_differences

    def select_data(self, X, columns=None):
        assert isinstance(X, pd.DataFrame)

        if columns is not None:
            X_transformed = create_timeless_dataset(X, columns=columns)
        else:
            X_transformed = create_timeless_dataset(X)
        X_transformed = X_transformed.dropna().reset_index(drop=True)
        return X_transformed

    @abstractmethod
    def predict(self, match_row):
        pass


class PCAMatchEncoder(MatchEncoder):
    def __init__(
        self,
        num_pca_features,
        auto_transform=False,
        columns=[
            "surface",
            "result",
            "num_played_minutes",
            "adv_ranking",
            "adv_ranking_points",
            "num_won_sets",
            "num_lost_sets",
            "num_won_games",
            "num_lost_games",
            "num_tie_break_wons",
            "num_tie_break_lost",
        ],
    ):
        self.num_pca_features = num_pca_features
        self.auto_transform = auto_transform
        self.columns = columns

        self.model = self.instantiate_model()

    def instantiate_model(self):
        model = PCA(n_components=self.num_pca_features)
        return model

    def fit(self, X, transform_data=False):
        if transform_data or self.auto_transform:
            X = self.select_data(X, columns=self.columns)
        self.model.fit(X)

    def predict(self, X, transform_data=False):
        if transform_data or self.auto_transform:
            X = self.select_data(X, columns=self.columns)
            return self.model.transform(X), X
        else:
            return self.model.transform(X)

    def save_model(self):
        pass


class MatchesHistoryEncoder:
    def __init__(self, match_encoder, num_matches, add_days_difference):
        self.match_encoder = match_encoder
        self.num_matches = num_matches
        self.add_days_difference = add_days_difference

    @abstractmethod
    def predict(self, match_row):
        pass

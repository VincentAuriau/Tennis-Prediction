from abc import abstractmethod


class BaseModel:
    def __init__(self):
        pass

    @abstractmethod
    def fit(self, X):
        pass

    @abstractmethod
    def predict(self, X):
        pass

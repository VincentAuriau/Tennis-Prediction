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


class DeepBaseModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.instantiate_model()

    @abstractmethod
    def instantiate_model(self, X):
        pass

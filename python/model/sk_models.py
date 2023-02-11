from abc import abstractmethod

import numpy as np


class BaseModel:
    def __init__(self):
        pass

    @abstractmethod
    def predict(self, X):
        pass
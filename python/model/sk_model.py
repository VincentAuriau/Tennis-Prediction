import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from model.base_model import BaseModel

class ScalerSVC(BaseModel):

    def __init__(self, C=1.0, kernel="linear",
                 degree=3, gamma="scale", tol=1e-3):
        self.C = C
        self.kernel = kernel
        self.degree = degree
        self.gamma = gamma
        self.tol = tol

        self.model = SVC(C=C, kernel=kernel, degree=degree, gamma=gamma, tol=tol)
        self.scaler_x = StandardScaler()
        self.scaler_y = StandardScaler()

    def fit(self, X, y):
        self.scaler_x.fit(X)
        self.scaler_y.fit(y.reshape(-1, 1))
        self.model.fit(self.scaler_x.transform(X), self.scaler_y.transform(y.reshape(-1, 1)))

    def predict(self, X):
        return self.scaler_y.inverse_transform(self.model.predict(self.scaler_x.transform(X)).reshape(-1, 1))

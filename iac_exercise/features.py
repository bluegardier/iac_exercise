import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from iac_exercise.config.core import config


class TargetDiffTransformer(BaseEstimator, TransformerMixin):
    """
    Transformer which creates the target_dg variable.
    """

    def __init__(self, final_var: str, original_var: str):
        self.final_var = final_var
        self.original_var = original_var

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        X[config.model_config.target_dg] = X[self.final_var] - X[self.original_var]

        return X


class FakeVariableTransformer(BaseEstimator, TransformerMixin):
    """
    Transformer which creates the fake_var variable.
    """

    def __init__(self, ph_var: str, original_var: str):
        self.ph_var = ph_var
        self.original_var = original_var

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        X[config.model_config.fake_var] = np.exp(X[self.ph_var]) / X[self.original_var]

        return X

from typing import Dict

import mlflow
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split


class TrainerRegressor:
    """
    A class to train models with mlflow context.
    The class takes the input model and performs
    gridsearch as well. However, note that gridsearch_tuning
    is optional. If you opt to not use it, the optimal_param
    in mlflow_run method must be set to False.
    """

    def __init__(self, estimator, params: Dict = {}):
        try:
            self._model = estimator(**params)
            self._params = params
        except TypeError:
            self._model = estimator.set_params(**params)
            self._params = params

    @property
    def model(self):
        return self._model

    @property
    def params(self):
        return self._params

    def train_test_split(self, X: pd.DataFrame, y: pd.Series):
        """
        Performs the usual sklearn train_test_split method.
        Parameters
        ----------
        X : Dataframe without unwanted variables.
        y : a pd.Series with the target values.

        Returns
        -------

        """

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.75, random_state=16
        )

    def gridsearch_tuning(self, dict_params: Dict, kfold_num: int):
        """
        Performs the GridSearch within the model specifications.
        Saves the best model's configuration for later use.
        Parameters
        ----------
        dict_params : a Dict with a combination of parameters.
        kfold_num : number of kfold.

        Returns
        -------

        """

        self._dict_params = dict_params
        grid = GridSearchCV(self._model, self._dict_params, cv=kfold_num)
        grid.fit(self.X_train, self.y_train)

        self.best_params = grid.best_params_

        try:
            self._model_opt = self._model(**self.best_params)
        except TypeError:
            self._model_opt = self._model.set_params(**self.best_params)

    def mlflow_run(
        self,
        model_name: str,
        r_name: str = "default_experiment",
        optimal_param: bool = False,
    ):
        """
        Trains the model with mlflow context, logging the metrics.

        Parameters
        ----------
        model_name :  The model name for log recording.
        r_name : Run Name for the experiment.
        optimal_param : If set to True, uses the best model configuration
        calculated from gridsearch_tuning.

        Returns
        -------

        """
        with mlflow.start_run(run_name=r_name) as run:
            runID = run.info.run_uuid
            experimentID = run.info.experiment_id

            if optimal_param is True:
                self._model = self._model_opt
                kfold_scores = cross_val_score(
                    self._model, self.X_train, self.y_train, cv=10
                )

                mlflow.log_metric("average_accuracy", kfold_scores.mean())
                mlflow.log_metric("std_accuracy", kfold_scores.std())

            self._model.fit(self.X_train, self.y_train)
            self.y_pred = self._model.predict(self.X_test)

            mlflow.sklearn.log_model(self._model, model_name)
            mlflow.log_params(self._params)

            mae = metrics.mean_absolute_error(self.y_test, self.y_pred)
            mse = metrics.mean_squared_error(self.y_test, self.y_pred)
            rmse = np.sqrt(mse)
            r2 = metrics.r2_score(self.y_test, self.y_pred)

            mlflow.log_metric("mae", mae)
            mlflow.log_metric("mse", mse)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)

            print("-" * 100)
            print(
                "Inside MLflow Run with run_id {} and experiment_id {}".format(
                    runID, experimentID
                )
            )
            print("Mean Absolute Error    :", mae)
            print("Mean Squared Error     :", mse)
            print("Root Mean Squared Error:", rmse)
            print("R2                     :", r2)
            print("Best Parameters        :", self.best_params)

            return experimentID, runID

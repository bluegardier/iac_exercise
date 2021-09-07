from catboost import CatBoostRegressor
from feature_engine.imputation import MeanMedianImputer
from sklearn.pipeline import Pipeline

from iac_exercise import features
from iac_exercise.config.core import config

final_pipeline = [
    (
        config.model_config.mean_median_imputer_name,
        MeanMedianImputer(
            imputation_method=config.model_config.meam_median_imputation_method,
            variables=config.model_config.imputer_variables,
        ),
    ),
    (
        config.model_config.target_diff_transformer_name,
        features.TargetDiffTransformer(*config.model_config.diff_create_var),
    ),
    (
        config.model_config.fake_variable_transformer_name,
        features.FakeVariableTransformer(*config.model_config.fake_create_var),
    ),
    (
        config.model_config.catboost_model_name,
        CatBoostRegressor(**config.model_config.catboost_best_params),
    ),
]

exercise_pipeline = Pipeline(final_pipeline)

import typing as t

import pandas as pd

from iac_exercise.config.core import config
from iac_exercise.data_manager import load_pipeline

# TODO: FIX VERSION VARIABLE
_version = "0.0.1"
pipeline_file_name = f"{config.model_config.pipeline_save_file}{_version}.pkl"
_exercise_pipeline = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)
    predictions = _exercise_pipeline.predict(data)
    results = {
        "predictions": [pred for pred in predictions],
        "version": _version,
    }

    return results

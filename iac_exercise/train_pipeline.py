import pandas as pd
from pipeline import exercise_pipeline
from sklearn.model_selection import train_test_split

from iac_exercise.config.core import config
from iac_exercise.data_manager import load_dataset, save_pipeline


def _filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter dataframe of wrong values.
    Parameters
    ----------
    df : The original dataframe.

    Returns
    -------
    The dataframe with its data properly filtered.
    """
    df = df.copy()
    df = df[~df[config.model_config.filter_ph].isnull()]
    df = df[df[config.model_config.filter_ph] <= config.model_config.ph_limit]
    df = df[df[config.model_config.filter_ebc] <= config.model_config.ebc_limit]
    df = df[df[config.model_config.filter_ibu] <= config.model_config.ibu_limit]
    df = df[df[config.model_config.filter_srm] <= config.model_config.srm_limit]
    return df


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)

    data = _filter_dataframe(data)

    # divide train and test
    X = data.drop(config.model_config.to_drop_train, axis=1)
    y = data[config.model_config.target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config.model_config.test_size,
        random_state=config.model_config.random_state,
    )

    # fit model
    exercise_pipeline.fit(X_train, y_train)

    # persist trained model
    save_pipeline(pipeline_to_persist=exercise_pipeline)


if __name__ == "__main__":
    run_training()

from kedro.pipeline import Pipeline, node
from .nodes import validate_data, split_data


def create_pipeline(**kwargs):
    return Pipeline([
        node(validate_data, "wine_raw", "validated_data",
             name="validate_data", tags=["prepare"]),
        node(split_data,
             ["validated_data", "params:split_options"],
             ["train_data", "val_data", "test_data"],
             name="split_data", tags=["prepare"]),
    ])
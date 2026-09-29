from kedro.pipeline import Pipeline, node
from .nodes import train_model, evaluate_model

def create_pipeline(**kwargs):
    return Pipeline([
        node(train_model,
             ["train_data", "params:model_options"], "model",
             name="train_model", tags=["train"]),
        node(evaluate_model, ["model", "val_data"],
             ["metrics", "predictions"],
             name="evaluate_model", tags=["eval"]),
    ])
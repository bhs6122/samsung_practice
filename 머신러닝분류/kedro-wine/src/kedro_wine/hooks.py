import os

import mlflow
import mlflow.sklearn
from kedro.framework.hooks import hook_impl

class TrackingHooks:
    def __init__(self):
        self.owns_run = False

    @hook_impl
    def before_pipeline_run(self, run_params):
        uri = os.getenv("MLFLOW_TRACKING_URI")
        if not uri:
            return
        mlflow.set_tracking_uri(uri)
        mlflow.set_experiment("kedro-wine-class")
        mlflow.start_run(run_name=run_params.get("pipeline_name") or "default")
        self.owns_run = True

    @hook_impl
    def after_node_run(self, node, inputs, outputs):
        if not self.owns_run:
            return
        for name, value in inputs.items():
            if name.startswith("params:"):
                prefix = name.removeprefix("params:")
                mlflow.log_params({
                    f"{prefix}.{k}": v for k, v in value.items()
                })
        if "metrics" in outputs:
            mlflow.log_metrics(outputs["metrics"])
        if node.name == "train_model":
            self.log_model(inputs, outputs)

    def log_model(self, inputs, outputs):
        X = inputs["train_data"].drop(
            columns=["row_id", "target"]
        ).head(5)
        mlflow.sklearn.log_model(
            outputs["model"],
            name="model",
            input_example=X,
        )

    def finish(self, status):
        if self.owns_run:
            try:
                mlflow.end_run(status=status)
            finally:
                self.owns_run = False

    @hook_impl
    def after_pipeline_run(self):
        self.finish("FINISHED")

    @hook_impl
    def on_pipeline_error(self):
        self.finish("FAILED")
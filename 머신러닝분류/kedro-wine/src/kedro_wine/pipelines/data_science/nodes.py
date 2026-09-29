from sklearn.pipeline import Pipeline as SkPipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score


def train_model(train_data, options):
    model = SkPipeline([
        ("scale", StandardScaler()),
        ("classifier", LogisticRegression(
            C=options["C"], max_iter=options["max_iter"],
            random_state=options["seed"])),
    ])
    X = train_data.drop(columns=["row_id", "target"])
    return model.fit(X, train_data["target"])


def evaluate_model(model, data):
    X = data.drop(columns=["row_id", "target"])
    pred = model.predict(X)
    metrics = {
        "accuracy": float(accuracy_score(data["target"], pred)),
        "f1_macro": float(f1_score(
            data["target"], pred, average="macro")),
    }
    predictions = data[["row_id", "target"]].copy()
    predictions["prediction"] = pred
    return metrics, predictions
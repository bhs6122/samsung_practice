from sklearn.model_selection import train_test_split


def validate_data(data):
    required = {"row_id", "target"}
    if not required.issubset(data.columns):
        raise ValueError("Missing required columns")
    if data.empty or data.isna().any().any():
        raise ValueError("Empty data or missing values")
    if not data["row_id"].is_unique:
        raise ValueError("Duplicate row_id")
    return data.copy()


def split_data(data, options):
    dev, test = train_test_split(
        data, test_size=options["test_size"],
        random_state=options["seed"],
        stratify=data["target"],
    )
    train, val = train_test_split(
        dev, test_size=options["val_size"],
        random_state=options["seed"],
        stratify=dev["target"],
    )
    return train, val, test
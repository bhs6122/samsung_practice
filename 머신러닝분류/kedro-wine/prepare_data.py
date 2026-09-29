from pathlib import Path
from sklearn.datasets import load_wine

data = load_wine(as_frame=True).frame
data.insert(0, "row_id", range(len(data)))
path = Path("data/01_raw/wine.csv")
path.parent.mkdir(parents=True, exist_ok=True)
data.to_csv(path, index=False)
print(data.shape)
print(data["target"].value_counts().sort_index())

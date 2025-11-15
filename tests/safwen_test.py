import os
import sys
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_loader import load_iris_as_dataframe, get_dataset_info  # noqa: E402
from src.model import IrisClassifier  # noqa: E402


def test_df_columns_and_rows():
    df_iris = load_iris_as_dataframe()

    expected_cols = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)",
        "target",
        "species",
    ]

    for col in expected_cols:
        assert col in df_iris.columns, f"column {col} is missing"

    assert len(df_iris) == 150
    assert set(df_iris["target"].unique()) == {0, 1, 2}


def test_dataset_info_values():
    info = get_dataset_info()

    assert info["n_samples"] == 150
    assert info["n_features"] == 4
    assert info["n_classes"] == 3

    class_dist = info["class_distribution"]
    assert sum(class_dist.values()) == info["n_samples"]
    assert set(class_dist.keys()) == {0, 1, 2}


def test_predict_before_training_gives_error():
    clf = IrisClassifier()
    x_sample = np.array([[5.1, 3.5, 1.4, 0.2]])

    try:
        clf.predict(x_sample)
        assert False, "predict should raise ValueError when model is not trained"
    except ValueError as e:
        assert "trained" in str(e).lower()

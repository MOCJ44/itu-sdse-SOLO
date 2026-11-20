"""Model test: the trained model must reproduce the reference results.

Both tests skip when there is nothing to test yet, so `uv run pytest`
passes on a fresh clone before the first training run.
"""
import base64
import json
from pathlib import Path

import mlflow.pyfunc
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
RESULTS_PATH = ROOT / "artifacts" / "model_results.json"
MODEL_PATH = ROOT / "models" / "model"
TEST_DATA_DIR = ROOT / "data" / "test"

# Placeholder; set from the difference the first CI run shows (week 3)
TOLERANCE = 0.02


def _reference_results():
    """Load the reference results (both reference runs are identical)."""
    reference_path = sorted(ROOT.glob("tests/fixtures/*/artifacts/model_results.json"))[0]
    return json.loads(reference_path.read_text())


def test_metrics_match_reference():
    if not RESULTS_PATH.exists():
        pytest.skip("No training results in artifacts/model_results.json")
    results = json.loads(RESULTS_PATH.read_text())
    reference = _reference_results()
    for metric in ("roc_auc", "accuracy"):
        assert abs(results[metric] - reference[metric]) <= TOLERANCE, metric


def test_model_answers_test_images():
    if not (MODEL_PATH / "MLmodel").exists():
        pytest.skip("No exported model in models/model")
    model = mlflow.pyfunc.load_model(str(MODEL_PATH))
    filenames = pd.read_csv(TEST_DATA_DIR / "metadata.csv")["filename"]
    images = [base64.b64encode((TEST_DATA_DIR / name).read_bytes()).decode() for name in filenames]

    output = model.predict({"instances": images})

    assert {"predictions", "confidences"} <= set(output)
    assert len(output["predictions"]) == len(images) == 10


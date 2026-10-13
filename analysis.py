"""Reproducible audit of the published student stress CSV.

This script examines associations and model sensitivity. It cannot recover the
original questionnaire or establish how the target labels were generated.
"""

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate

TARGET = "stress_level"
PRESSURE = "blood_pressure"


def audit(path: Path) -> dict:
    data = pd.read_csv(path)
    if TARGET not in data or PRESSURE not in data:
        raise ValueError(f"CSV must contain {TARGET} and {PRESSURE}")
    if data.columns.duplicated().any():
        raise ValueError("Duplicate column names")
    if data.isna().any().any():
        raise ValueError("Missing values require an explicit preprocessing plan")
    if set(data[TARGET].unique()) != {0, 1, 2}:
        raise ValueError("Expected the published 0/1/2 target")
    if not all(pd.api.types.is_numeric_dtype(t) for t in data.dtypes):
        raise ValueError("This audit requires numeric predictors")

    x = data.drop(columns=TARGET)
    y = data[TARGET]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    experiments = {}
    for name, predictors in (("all_features", x), ("without_blood_pressure", x.drop(columns=PRESSURE))):
        model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=1)
        scores = cross_validate(model, predictors, y, cv=cv, scoring=("accuracy", "f1_macro"), n_jobs=1)
        experiments[name] = {
            "accuracy_mean": round(float(scores["test_accuracy"].mean()), 4),
            "accuracy_sd": round(float(scores["test_accuracy"].std()), 4),
            "macro_f1_mean": round(float(scores["test_f1_macro"].mean()), 4),
        }
    baseline = cross_validate(DummyClassifier(strategy="most_frequent"), x, y, cv=cv, scoring="accuracy")
    return {
        "rows": len(data),
        "predictor_count": x.shape[1],
        "missing_cells": int(data.isna().sum().sum()),
        "duplicate_rows": int(data.duplicated().sum()),
        "target_counts": {str(k): int(v) for k, v in y.value_counts().sort_index().items()},
        "blood_pressure_by_stress_level": {
            str(k): {str(c): int(v) for c, v in row.items()}
            for k, row in pd.crosstab(data[PRESSURE], y).to_dict(orient="index").items()
        },
        "majority_baseline_accuracy": round(float(baseline["test_score"].mean()), 4),
        "models": experiments,
        "interpretation": "Associations and predictive performance do not establish label construction or causal effects.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).with_name("StressLevelDataset.csv"))
    parser.add_argument("--output", type=Path, help="Optional path for a JSON report")
    args = parser.parse_args()
    result = json.dumps(audit(args.data), indent=2)
    if args.output:
        args.output.write_text(result + "\n", encoding="utf-8")
    print(result)

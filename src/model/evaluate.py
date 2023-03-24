#!/usr/bin/env python
import pandas as pd
import json

from sklearn.metrics import (
    roc_curve,
    auc,
    confusion_matrix,
)
from clize import run


def evaluate(
    src_true_values: str, src_preds: str, target: str, scenario: str, model_type: str
):

    """Evaluate model performance"""
    # Load predictions
    predictions = pd.read_csv(
        src_preds + "/" + scenario + "/predictions_" + model_type + ".csv", sep=";"
    )
    predictions.pop("Unnamed: 0")
    # Load true labels
    y_true = pd.read_csv(src_true_values + "/" + scenario + "/y_test.csv", sep=";")
    y_true.pop("Unnamed: 0")

    # Confusion Matrix
    cm = confusion_matrix(y_true=y_true, y_pred=predictions["predictions"])
    true_negative = cm[0, 0]
    false_positive = cm[0, 1]
    false_negative = cm[1, 0]
    true_positive = cm[1, 1]

    # Metrics
    FPR = false_positive / (false_positive + true_negative)
    FNR = false_negative / (true_positive + false_negative)
    RCL = true_positive / (true_positive + false_negative)
    PRC = true_positive / (true_positive + false_positive)
    ACC = (true_positive + true_negative) / (
        true_positive + false_positive + false_negative + true_negative
    )
    F1 = 2 * (PRC * RCL) / (PRC + RCL)
    
    
    # ROC AUC
    scores = predictions["scores"]
    fpr_, tpr_, _ = roc_curve(y_true, scores)
    AUC = auc(fpr_, tpr_)
    results = pd.concat(
        [y_true["exploit"], predictions["predictions"]],
        axis=1,
        keys=["y_true", "predictions"],
    )

    results = results.rename(
        columns={"y_true": "actual", "predictions": "predicted"}
    )
    results.to_csv(
        target + "/" + scenario + "/results_" + model_type + ".csv",
        sep=";",
        index=False,
    )

    with open(
        target + "/" + scenario + "/metrics_" + model_type + ".json", "w"
    ) as output:
        json.dump(
            {
                "FPR": FPR,
                "FNR": FNR,
                "RCL": RCL,
                "PRC": PRC,
                "ACC": ACC,
                "F1": F1,
                "AUC": AUC,
            },
            output,
            indent=4,
        )

    return


if __name__ == "__main__":
    run(evaluate)

import numpy as np
import pandas as pd
from pgmpy.inference import VariableElimination
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    precision_recall_curve,
    average_precision_score,
)

def predict_bn(model, test_df: pd.DataFrame, target: str):
    infer = VariableElimination(model)
    feature_cols = [c for c in test_df.columns if c != target]

    y_true, y_pred, y_proba = [], [], []

    for _, row in test_df.iterrows():
        evidence = {col: row[col] for col in feature_cols}
        q = infer.query(variables=[target], evidence=evidence, show_progress=False)

        prob_1 = float(q.values[1])
        y_proba.append(prob_1)

        idx = int(np.argmax(q.values))
        pred_state = int(q.state_names[target][idx])
        y_pred.append(pred_state)

        y_true.append(int(row[target]))

    return np.array(y_true), np.array(y_pred), np.array(y_proba)

def compute_metrics(y_true, y_pred, y_proba) -> dict:
    acc = float(np.mean(y_true == y_pred))
    roc_auc = float(roc_auc_score(y_true, y_proba))
    ap = float(average_precision_score(y_true, y_proba))
    report = classification_report(y_true, y_pred, digits=4, output_dict=True)

    prec, rec, _ = precision_recall_curve(y_true, y_proba)

    return {
        "accuracy": acc,
        "roc_auc": roc_auc,
        "pr_auc_average_precision": ap,
        "classification_report": report,
        "pr_curve_points": {
            "precision": prec.tolist(),
            "recall": rec.tolist(),
        },
    }

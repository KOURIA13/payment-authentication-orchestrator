from __future__ import annotations

import os
import pandas as pd


def add_business_scores(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    strategy_cost = {
        "NO_STEP_UP": 5,
        "3DS_FRICTIONLESS": 20,
        "3DS_CHALLENGE": 55,
        "PASSKEY": 18,
        "SOFT_DECLINE_RETRY_WITH_AUTH": 45,
    }

    result["strategy_cost_score"] = result["recommended_strategy"].map(strategy_cost)

    result["business_value_score"] = (
        0.45 * result["pred_approval_proba"]
        - 0.25 * result["pred_abandon_proba"]
        - 0.20 * result["pred_fraud_proba"]
        - 0.10 * result["strategy_cost_score"]
    ).round(2)

    return result


def evaluate_and_save(df: pd.DataFrame, metrics: dict, output_dir: str, output_file: str) -> None:
    print("\n====== AUTHENTICATION ORCHESTRATOR RESULTS ======")
    print(f"Transactions: {len(df)}")

    for target, target_metrics in metrics.items():
        print(f"\nModel: {target}")
        print(f"AUC: {target_metrics['auc']}")
        print(target_metrics["report"])

    print("\nRecommended strategies:")
    print(df["recommended_strategy"].value_counts())

    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"\nSaved to {output_file}")
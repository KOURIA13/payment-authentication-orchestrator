from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split


FEATURE_COLS = [
    "amount_eur",
    "cross_border",
    "device_type_encoded",
    "browser_type_encoded",
    "merchant_category_encoded",
    "card_scheme_encoded",
    "returning_user",
    "tokenized",
    "passkey_available",
    "exemption_possible",
    "previous_soft_decline",
    "previous_challenge_success",
    "failed_auth_attempts_30d",
    "issuer_behavior_encoded",
    "risk_proxy",
    "friction_proxy",
]


def train_models(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    X = df[FEATURE_COLS].copy()

    metrics = {}
    result = df.copy()

    targets = {
        "approved": "pred_approval_proba",
        "abandoned": "pred_abandon_proba",
        "fraud_flag": "pred_fraud_proba",
    }

    for target, output_col in targets.items():
        y = df[target].copy()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=y
        )

        clf = RandomForestClassifier(
            n_estimators=250,
            max_depth=10,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced",
        )
        clf.fit(X_train, y_train)

        proba = clf.predict_proba(X)[:, 1]
        preds = clf.predict(X_test)
        test_proba = clf.predict_proba(X_test)[:, 1]

        result[output_col] = (proba * 100).round(2)

        metrics[target] = {
            "auc": round(roc_auc_score(y_test, test_proba), 3),
            "report": classification_report(y_test, preds, output_dict=False),
        }

    return result, metrics
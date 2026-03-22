from __future__ import annotations

import pandas as pd


def decide_authentication_strategy(row: pd.Series) -> str:
    approval = row["pred_approval_proba"]
    abandon = row["pred_abandon_proba"]
    fraud = row["pred_fraud_proba"]

    passkey_available = row["passkey_available"]
    exemption_possible = row["exemption_possible"]
    previous_soft_decline = row["previous_soft_decline"]
    tokenized = row["tokenized"]
    returning_user = row["returning_user"]

    if previous_soft_decline == 1:
        return "SOFT_DECLINE_RETRY_WITH_AUTH"

    if fraud >= 70:
        return "3DS_CHALLENGE"

    if abandon >= 60 and passkey_available == 1:
        return "PASSKEY"

    if fraud < 25 and approval >= 75 and exemption_possible == 1 and tokenized == 1 and returning_user == 1:
        return "NO_STEP_UP"

    if fraud < 45 and approval >= 65:
        return "3DS_FRICTIONLESS"

    if passkey_available == 1 and abandon >= 40:
        return "PASSKEY"

    return "3DS_CHALLENGE"


def apply_policy(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["recommended_strategy"] = result.apply(decide_authentication_strategy, axis=1)

    def decision_reason(row: pd.Series) -> str:
        strat = row["recommended_strategy"]
        if strat == "NO_STEP_UP":
            return "Low risk, high approval, strong trust signals"
        if strat == "3DS_FRICTIONLESS":
            return "Moderate risk with acceptable approval probability"
        if strat == "3DS_CHALLENGE":
            return "Higher risk or issuer sensitivity requires stronger authentication"
        if strat == "PASSKEY":
            return "High friction risk, passkey available to reduce abandonment"
        if strat == "SOFT_DECLINE_RETRY_WITH_AUTH":
            return "Retrying after previous soft decline with stronger auth"
        return "Default policy"

    result["decision_reason"] = result.apply(decision_reason, axis=1)
    return result
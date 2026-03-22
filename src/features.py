from __future__ import annotations

import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    features = df.copy()

    device_map = {"mobile": 0, "desktop": 1, "tablet": 2}
    browser_map = {"chrome": 0, "safari": 1, "firefox": 2, "edge": 3, "app_webview": 4}
    category_map = {"marketplace": 0, "saas": 1, "travel": 2, "retail": 3, "subscriptions": 4}
    scheme_map = {"visa": 0, "mc": 1, "amex": 2}
    issuer_map = {"friendly": 0, "neutral": 1, "strict": 2}

    features["device_type_encoded"] = features["device_type"].map(device_map)
    features["browser_type_encoded"] = features["browser_type"].map(browser_map)
    features["merchant_category_encoded"] = features["merchant_category"].map(category_map)
    features["card_scheme_encoded"] = features["card_scheme"].map(scheme_map)
    features["issuer_behavior_encoded"] = features["issuer_behavior"].map(issuer_map)

    features["risk_proxy"] = (
        features["cross_border"] * 2
        + (1 - features["returning_user"]) * 2
        + (1 - features["tokenized"]) * 2
        + features["failed_auth_attempts_30d"] * 3
        + features["previous_soft_decline"] * 4
    )

    features["friction_proxy"] = (
        (features["device_type"] == "mobile").astype(int) * 2
        + (features["browser_type"] == "app_webview").astype(int) * 3
        + (1 - features["returning_user"]) * 2
        + (1 - features["passkey_available"]) * 1
    )

    return features
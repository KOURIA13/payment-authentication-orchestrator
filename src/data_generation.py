from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class AuthConfig:
    n_samples: int = 12000
    random_state: int = 42
    output_dir: str = "outputs"
    output_file: str = "outputs/authentication_decisions.csv"


def generate_authentication_data(cfg: AuthConfig) -> pd.DataFrame:
    rng = np.random.default_rng(cfg.random_state)

    merchant_countries = ["FR", "NL", "DE", "ES", "IT", "BE", "UK"]
    issuer_countries = ["FR", "NL", "DE", "ES", "IT", "BE", "UK", "US"]
    device_types = ["mobile", "desktop", "tablet"]
    browser_types = ["chrome", "safari", "firefox", "edge", "app_webview"]
    merchant_categories = ["marketplace", "saas", "travel", "retail", "subscriptions"]
    card_schemes = ["visa", "mc", "amex"]
    issuer_behaviors = ["friendly", "neutral", "strict"]

    rows = []

    for i in range(cfg.n_samples):
        amount_eur = round(max(1.5, rng.normal(85, 60)), 2)
        merchant_country = rng.choice(merchant_countries)
        issuer_country = rng.choice(issuer_countries)
        cross_border = 1 if merchant_country != issuer_country else 0

        device_type = rng.choice(device_types, p=[0.52, 0.40, 0.08])
        browser_type = rng.choice(browser_types, p=[0.42, 0.20, 0.12, 0.10, 0.16])
        merchant_category = rng.choice(merchant_categories, p=[0.25, 0.22, 0.10, 0.28, 0.15])
        card_scheme = rng.choice(card_schemes, p=[0.52, 0.40, 0.08])

        returning_user = int(rng.random() < 0.58)
        tokenized = int(rng.random() < 0.54)
        passkey_available = int(rng.random() < 0.28)
        exemption_possible = int(rng.random() < 0.45)
        previous_soft_decline = int(rng.random() < 0.08)
        previous_challenge_success = int(rng.random() < 0.22)
        failed_auth_attempts_30d = int(rng.poisson(0.35))

        issuer_behavior = rng.choice(issuer_behaviors, p=[0.35, 0.45, 0.20])
        issuer_strictness = {"friendly": 0.2, "neutral": 0.5, "strict": 0.8}[issuer_behavior]

        base_risk = 0.10
        if amount_eur > 150:
            base_risk += 0.08
        if cross_border == 1:
            base_risk += 0.06
        if returning_user == 0:
            base_risk += 0.05
        if tokenized == 0:
            base_risk += 0.04
        if failed_auth_attempts_30d >= 2:
            base_risk += 0.09
        if browser_type == "app_webview":
            base_risk += 0.04
        if merchant_category == "travel":
            base_risk += 0.05

        base_risk += issuer_strictness * 0.06
        risk_score = min(base_risk, 0.95)

        base_friction = 0.08
        if device_type == "mobile":
            base_friction += 0.05
        if browser_type == "app_webview":
            base_friction += 0.08
        if returning_user == 0:
            base_friction += 0.05
        if amount_eur > 150:
            base_friction += 0.03
        if issuer_behavior == "strict":
            base_friction += 0.08

        friction_score = min(base_friction, 0.95)

        # synthetic outcome labels
        approval_probability = 0.82
        approval_probability -= risk_score * 0.32
        approval_probability -= friction_score * 0.12
        approval_probability += 0.06 if tokenized == 1 else 0
        approval_probability += 0.05 if returning_user == 1 else 0
        approval_probability += 0.03 if previous_challenge_success == 1 else 0
        approval_probability -= 0.12 if previous_soft_decline == 1 else 0
        approval_probability = min(max(approval_probability, 0.05), 0.98)

        abandon_probability = 0.05
        abandon_probability += friction_score * 0.45
        abandon_probability += 0.07 if device_type == "mobile" else 0
        abandon_probability += 0.05 if browser_type == "app_webview" else 0
        abandon_probability += 0.05 if returning_user == 0 else 0
        abandon_probability -= 0.06 if passkey_available == 1 else 0
        abandon_probability = min(max(abandon_probability, 0.01), 0.95)

        fraud_probability = min(max(risk_score * 0.85, 0.01), 0.98)

        approved = 1 if rng.random() < approval_probability else 0
        abandoned = 1 if rng.random() < abandon_probability else 0
        fraud_flag = 1 if rng.random() < fraud_probability else 0

        rows.append(
            {
                "transaction_id": f"TX_{i+1:07d}",
                "amount_eur": amount_eur,
                "merchant_country": merchant_country,
                "issuer_country": issuer_country,
                "cross_border": cross_border,
                "device_type": device_type,
                "browser_type": browser_type,
                "merchant_category": merchant_category,
                "card_scheme": card_scheme,
                "returning_user": returning_user,
                "tokenized": tokenized,
                "passkey_available": passkey_available,
                "exemption_possible": exemption_possible,
                "previous_soft_decline": previous_soft_decline,
                "previous_challenge_success": previous_challenge_success,
                "failed_auth_attempts_30d": failed_auth_attempts_30d,
                "issuer_behavior": issuer_behavior,
                "risk_score_label": round(risk_score * 100, 2),
                "friction_score_label": round(friction_score * 100, 2),
                "approved": approved,
                "abandoned": abandoned,
                "fraud_flag": fraud_flag,
            }
        )

    return pd.DataFrame(rows)
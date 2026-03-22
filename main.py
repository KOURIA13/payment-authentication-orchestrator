from __future__ import annotations

from src.data_generation import AuthConfig, generate_authentication_data
from src.features import build_features
from src.model import train_models
from src.policy import apply_policy
from src.scoring import add_business_scores, evaluate_and_save


def main() -> None:
    cfg = AuthConfig()

    df = generate_authentication_data(cfg)
    df = build_features(df)
    df, metrics = train_models(df)
    df = apply_policy(df)
    df = add_business_scores(df)

    evaluate_and_save(
        df=df,
        metrics=metrics,
        output_dir=cfg.output_dir,
        output_file=cfg.output_file,
    )


if __name__ == "__main__":
    main()
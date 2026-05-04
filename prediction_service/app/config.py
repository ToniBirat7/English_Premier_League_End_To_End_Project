import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    mlflow_tracking_uri: str
    registered_model_name: str
    model_version: str
    postgres_host: str
    postgres_port: int
    postgres_database: str
    postgres_user: str
    postgres_password: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            mlflow_tracking_uri=os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow:5000"),
            registered_model_name=os.environ.get("REGISTERED_MODEL_NAME", "Best_XGBoost_Model"),
            model_version=os.environ.get("MODEL_VERSION", "2"),
            postgres_host=os.environ.get("POSTGRES_HOST", "postgres"),
            postgres_port=int(os.environ.get("POSTGRES_PORT", "5432")),
            postgres_database=os.environ.get("POSTGRES_DATABASE", "epl_postgres"),
            postgres_user=os.environ.get("POSTGRES_USER", "postgres"),
            postgres_password=os.environ.get("POSTGRES_PASSWORD", "postgres"),
        )

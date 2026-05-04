import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient

from app import main as main_module
from app.config import Settings
from app.featurizer import MODEL_FEATURE_ORDER


class _StubModel:
    def predict(self, X):
        # Return a 2-prob array per row to exercise the prob_H >= prob_NH branch.
        return np.array([[0.7, 0.3]] * len(X))


@pytest.fixture
def client(monkeypatch):
    settings = Settings(
        mlflow_tracking_uri="http://stub",
        registered_model_name="Best_XGBoost_Model",
        model_version="2",
        postgres_host="stub", postgres_port=5432, postgres_database="d",
        postgres_user="u", postgres_password="p",
    )

    def _stub_features(home, away, season, matchweek, settings):
        row = {c: 0.0 if not c.startswith(("HM", "AM")) else False for c in MODEL_FEATURE_ORDER}
        return pd.DataFrame([row])[MODEL_FEATURE_ORDER]

    monkeypatch.setattr(main_module, "build_feature_row", _stub_features)

    main_module.app.state.settings = settings
    main_module.app.state.model = _StubModel()

    with TestClient(main_module.app) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["model_version"] == "2"


def test_predict(client):
    r = client.post(
        "/predict",
        json={"home_team": "Arsenal", "away_team": "Chelsea", "season": "2023-24", "matchweek": 10},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["prediction"] == "H"
    assert body["prob_H"] == pytest.approx(0.7)
    assert body["prob_NH"] == pytest.approx(0.3)
    assert body["model_version"] == "2"

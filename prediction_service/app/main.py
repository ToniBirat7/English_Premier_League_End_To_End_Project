import logging
from contextlib import asynccontextmanager

import mlflow
import numpy as np
from fastapi import FastAPI, HTTPException

from .config import Settings
from .featurizer import build_feature_row
from .schemas import HealthResponse, MatchInput, PredictionResponse

logger = logging.getLogger("prediction_service")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings.from_env()
    app.state.settings = settings

    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    model_uri = f"models:/{settings.registered_model_name}/{settings.model_version}"
    logger.info(f"Loading model from {model_uri} via {settings.mlflow_tracking_uri}")
    app.state.model = mlflow.pyfunc.load_model(model_uri)
    logger.info("Model loaded")
    yield


app = FastAPI(title="EPL Prediction Service", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings: Settings = app.state.settings
    return HealthResponse(status="ok", model_version=settings.model_version)


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: MatchInput) -> PredictionResponse:
    settings: Settings = app.state.settings
    try:
        features = build_feature_row(
            home=payload.home_team,
            away=payload.away_team,
            season=payload.season,
            matchweek=payload.matchweek,
            settings=settings,
        )
    except Exception as e:
        logger.exception("featurizer failed")
        raise HTTPException(status_code=502, detail=f"feature lookup failed: {e}")

    try:
        raw = app.state.model.predict(features)
    except Exception as e:
        logger.exception("model predict failed")
        raise HTTPException(status_code=500, detail=f"model predict failed: {e}")

    arr = np.asarray(raw)
    if arr.ndim == 2 and arr.shape[1] == 2:
        prob_h, prob_nh = float(arr[0, 0]), float(arr[0, 1])
    else:
        # XGBClassifier wrapped via pyfunc returns class labels (encoded ints).
        # Map: LabelEncoder sorts targets {"H", "NH"} -> H=0, NH=1.
        label = int(arr.flat[0])
        prob_h = 1.0 if label == 0 else 0.0
        prob_nh = 1.0 - prob_h

    pred = "H" if prob_h >= prob_nh else "NH"
    return PredictionResponse(
        prob_H=prob_h, prob_NH=prob_nh, prediction=pred, model_version=settings.model_version,
    )

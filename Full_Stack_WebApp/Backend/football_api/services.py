import requests
from django.conf import settings
from src_logger import logger


def predict_match(home_team: str, away_team: str, season: str, matchweek: int) -> dict | None:
    """
    Call the FastAPI prediction service to get match outcome probabilities.
    Returns dict with prob_H, prob_NH, prediction, model_version on success.
    Returns None on connection error or timeout.
    """
    try:
        url = f"{settings.PREDICTION_SERVICE_URL}/predict"
        payload = {
            "home_team": home_team,
            "away_team": away_team,
            "season": season,
            "matchweek": matchweek,
        }
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, requests.Timeout) as e:
        logger.warning(f"Failed to fetch prediction for {home_team} vs {away_team}: {e}")
        return None

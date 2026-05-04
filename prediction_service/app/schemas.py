from typing import Literal
from pydantic import BaseModel, Field


class MatchInput(BaseModel):
    home_team: str = Field(..., description="Home team name as stored in football_api_match.home_team")
    away_team: str = Field(..., description="Away team name as stored in football_api_match.away_team")
    season: str = Field(..., description="Season label, e.g. '2023-24'")
    matchweek: int = Field(..., ge=1, le=38, description="Matchweek number this prediction is for (1-38)")


class PredictionResponse(BaseModel):
    prob_H: float
    prob_NH: float
    prediction: Literal["H", "NH"]
    model_version: str


class HealthResponse(BaseModel):
    status: Literal["ok"]
    model_version: str

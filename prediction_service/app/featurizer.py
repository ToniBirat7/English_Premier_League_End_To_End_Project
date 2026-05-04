"""Feature reconstruction for /predict.

Vendors the small bits of preprocess_features / get_points / only_hw needed
to produce a model_columns row from raw match history pulled from the Django
Postgres table football_api_match.

Known limitation: the training pipeline applies sklearn.preprocessing.scale
(z-score) to HTGD/ATGD/HTP/ATP after the divide-by-matchweek step, but the
fitted scaler is NOT persisted by data_transformation. We replicate only the
divide-by-matchweek scaling here, which is the deterministic part of training
preprocessing. Predictions will still be directionally correct but not
identical to a re-trained holdout. Persisting the scaler is tracked as
deferred work.
"""

from __future__ import annotations

import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

from .config import Settings

MODEL_FEATURE_ORDER = [
    "HTP", "ATP", "HTGD", "ATGD", "DiffFormPts",
    "HM1_D", "HM1_L", "HM1_M", "HM1_W",
    "HM2_D", "HM2_L", "HM2_M", "HM2_W",
    "HM3_D", "HM3_L", "HM3_M", "HM3_W",
    "AM1_D", "AM1_L", "AM1_M", "AM1_W",
    "AM2_D", "AM2_L", "AM2_M", "AM2_W",
    "AM3_D", "AM3_L", "AM3_M", "AM3_W",
]


def _result_for_team(row: dict, team: str) -> str:
    if row["ftr"] == "D":
        return "D"
    if row["ftr"] == "H":
        return "W" if row["home_team"] == team else "L"
    return "W" if row["away_team"] == team else "L"


def _points(result: str) -> int:
    return {"W": 3, "D": 1, "L": 0, "M": 0}[result]


def _open_conn(settings: Settings):
    return psycopg2.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_database,
        user=settings.postgres_user,
        password=settings.postgres_password,
    )


def _fetch_recent(cur, team: str, season: str, before_mw: int, n: int) -> list[dict]:
    cur.execute(
        """
        SELECT date, home_team, away_team, fthg, ftag, ftr, matchweek
        FROM football_api_match
        WHERE season = %s
          AND matchweek < %s
          AND (home_team = %s OR away_team = %s)
        ORDER BY date DESC, matchweek DESC
        LIMIT %s
        """,
        (season, before_mw, team, team, n),
    )
    return list(cur.fetchall())


def _cumulative_stats(cur, team: str, season: str, before_mw: int) -> dict:
    cur.execute(
        """
        SELECT
          COALESCE(SUM(CASE WHEN home_team = %s THEN fthg ELSE ftag END), 0) AS goals_for,
          COALESCE(SUM(CASE WHEN home_team = %s THEN ftag ELSE fthg END), 0) AS goals_against,
          COALESCE(SUM(CASE
                WHEN ftr = 'D' THEN 1
                WHEN (ftr = 'H' AND home_team = %s) OR (ftr = 'A' AND away_team = %s) THEN 3
                ELSE 0
              END), 0) AS points
        FROM football_api_match
        WHERE season = %s
          AND matchweek < %s
          AND (home_team = %s OR away_team = %s)
        """,
        (team, team, team, team, season, before_mw, team, team),
    )
    return dict(cur.fetchone())


def build_feature_row(home: str, away: str, season: str, matchweek: int, settings: Settings) -> pd.DataFrame:
    """Query Postgres for both teams' recent form and return a single-row
    DataFrame whose columns are MODEL_FEATURE_ORDER (the model_columns block
    from astro_airflow_mlflow/schema.yaml)."""
    with _open_conn(settings) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            home_recent = _fetch_recent(cur, home, season, matchweek, 5)
            away_recent = _fetch_recent(cur, away, season, matchweek, 5)
            home_stats = _cumulative_stats(cur, home, season, matchweek)
            away_stats = _cumulative_stats(cur, away, season, matchweek)

    home_results = [_result_for_team(r, home) for r in home_recent]
    away_results = [_result_for_team(r, away) for r in away_recent]
    while len(home_results) < 5:
        home_results.append("M")
    while len(away_results) < 5:
        away_results.append("M")

    htgd = float(home_stats["goals_for"]) - float(home_stats["goals_against"])
    atgd = float(away_stats["goals_for"]) - float(away_stats["goals_against"])
    htp = float(home_stats["points"])
    atp = float(away_stats["points"])

    htform = sum(_points(r) for r in home_results)
    atform = sum(_points(r) for r in away_results)
    diff_form_pts = float(htform - atform)

    mw_divisor = float(max(matchweek, 1))
    row = {
        "HTP": htp / mw_divisor,
        "ATP": atp / mw_divisor,
        "HTGD": htgd / mw_divisor,
        "ATGD": atgd / mw_divisor,
        "DiffFormPts": diff_form_pts / mw_divisor,
    }
    for i, val in [(1, home_results[0]), (2, home_results[1]), (3, home_results[2])]:
        for opt in ("D", "L", "M", "W"):
            row[f"HM{i}_{opt}"] = (val == opt)
    for i, val in [(1, away_results[0]), (2, away_results[1]), (3, away_results[2])]:
        for opt in ("D", "L", "M", "W"):
            row[f"AM{i}_{opt}"] = (val == opt)

    df = pd.DataFrame([row])
    return df[MODEL_FEATURE_ORDER]

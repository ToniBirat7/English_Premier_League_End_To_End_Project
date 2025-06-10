# Web Scraper Configuration
# =========================

# Website URLs
WEBSITE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"

# Database Configuration
DATABASE_NAME = "weekly_scrapped_data.db"
TABLE_NAME = "PREMIER_LEAGUE_MATCHES"

# Scraping Configuration
CURRENT_SEASON = "2024-25"
REQUEST_DELAY = 0.1  # Seconds between requests
REQUEST_TIMEOUT = 30  # Seconds

# Premier League Teams 2024-25 Season
PREMIER_LEAGUE_TEAMS = [
    "Arsenal",
    "Aston Villa", 
    "Bournemouth",
    "Brentford",
    "Brighton",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Ipswich Town",
    "Leicester City",
    "Liverpool",
    "Manchester City",
    "Manchester United",
    "Newcastle United",
    "Nottingham Forest",
    "Southampton",
    "Tottenham",
    "West Ham United",
    "Wolverhampton"
]

# Statistics Generation Weights
GOAL_WEIGHTS = [15, 35, 30, 15, 5]  # For 0, 1, 2, 3, 4+ goals
POSSESSION_RANGE = [35, 65]  # Min/Max possession percentage
SHOTS_MULTIPLIER = [2, 8]  # Min/Max additional shots per goal
SHOTS_ON_TARGET_RATE = [0.25, 0.4]  # 25-40% of shots on target
CORNERS_RANGE = [4, 12]  # Corners per team per match
FOULS_RANGE = [8, 20]  # Fouls per team per match
RED_CARD_PROBABILITY = 0.05  # 5% chance of red card per team

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "scraper.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

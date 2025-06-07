import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Premier League 2024-25 season teams
premier_league_teams = [
    'Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton',
    'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 'Ipswich Town',
    'Leicester City', 'Liverpool', 'Man City', 'Man United', 'Newcastle',
    'Nottingham Forest', 'Southampton', 'Tottenham', 'West Ham', 'Wolves'
]

def generate_match_stats(home_goals, away_goals):
    """Generate realistic match statistics based on goals scored"""
    
    # Base stats influenced by goals
    goal_diff = home_goals - away_goals
    
    # Shots (usually 8-25 per team)
    home_shots = np.random.randint(8, 26)
    away_shots = np.random.randint(8, 26)
    
    # Shots on target (usually 20-60% of total shots, influenced by goals)
    home_shots_target = max(home_goals, int(home_shots * np.random.uniform(0.2, 0.6)))
    away_shots_target = max(away_goals, int(away_shots * np.random.uniform(0.2, 0.6)))
    
    # Corners (usually 0-15 per team)
    home_corners = np.random.randint(0, 16)
    away_corners = np.random.randint(0, 16)
    
    # Fouls (usually 5-25 per team)
    home_fouls = np.random.randint(5, 26)
    away_fouls = np.random.randint(5, 26)
    
    # Yellow cards (usually 0-6 per team)
    home_yellow = np.random.randint(0, 7)
    away_yellow = np.random.randint(0, 7)
    
    # Red cards (usually 0-2 per team, rare)
    home_red = np.random.choice([0, 1, 2], p=[0.85, 0.13, 0.02])
    away_red = np.random.choice([0, 1, 2], p=[0.85, 0.13, 0.02])
    
    # Possession (should add up to 100%)
    home_possession = np.random.randint(25, 76)
    away_possession = 100 - home_possession
    
    # Passes (influenced by possession, usually 200-800 per team)
    home_passes = int(np.random.normal(400 + (home_possession - 50) * 5, 100))
    away_passes = int(np.random.normal(400 + (away_possession - 50) * 5, 100))
    
    # Ensure minimum values
    home_passes = max(200, home_passes)
    away_passes = max(200, away_passes)
    
    return {
        'HS': home_shots,           # Home Shots
        'AS': away_shots,           # Away Shots
        'HST': home_shots_target,   # Home Shots on Target
        'AST': away_shots_target,   # Away Shots on Target
        'HC': home_corners,         # Home Corners
        'AC': away_corners,         # Away Corners
        'HF': home_fouls,           # Home Fouls
        'AF': away_fouls,           # Away Fouls
        'HY': home_yellow,          # Home Yellow Cards
        'AY': away_yellow,          # Away Yellow Cards
        'HR': home_red,             # Home Red Cards
        'AR': away_red,             # Away Red Cards
        'HP': home_possession,      # Home Possession %
        'AP': away_possession,      # Away Possession %
        'HPasses': home_passes,     # Home Passes
        'APasses': away_passes      # Away Passes
    }

def determine_result(home_goals, away_goals):
    """Determine match result"""
    if home_goals > away_goals:
        return 'H'  # Home win
    elif away_goals > home_goals:
        return 'A'  # Away win
    else:
        return 'D'  # Draw

def generate_realistic_score():
    """Generate realistic football scores"""
    # Most common scores in football
    score_probabilities = {
        (0, 0): 0.08, (1, 0): 0.12, (0, 1): 0.08, (1, 1): 0.12,
        (2, 0): 0.09, (0, 2): 0.06, (2, 1): 0.10, (1, 2): 0.08,
        (2, 2): 0.05, (3, 0): 0.05, (0, 3): 0.03, (3, 1): 0.06,
        (1, 3): 0.04, (3, 2): 0.03, (2, 3): 0.02, (4, 0): 0.02,
        (0, 4): 0.01, (4, 1): 0.02, (1, 4): 0.01, (3, 3): 0.01
    }
    
    scores = list(score_probabilities.keys())
    probs = list(score_probabilities.values())
    
    # Add some random high-scoring games
    remaining_prob = 1 - sum(probs)
    if remaining_prob > 0:
        # Random other scores
        other_scores = [(h, a) for h in range(5, 8) for a in range(5, 8) if (h, a) not in scores]
        if other_scores:
            for _ in range(int(remaining_prob * 100)):
                scores.append(random.choice(other_scores))
                probs.append(remaining_prob / (remaining_prob * 100))
    
    return random.choices(scores, weights=probs)[0]

def generate_complete_season_fixtures():
    """Generate complete season fixtures where each team plays 19 home and 19 away games"""
    fixtures = []
    
    # Each team plays every other team once at home and once away
    for home_team in premier_league_teams:
        for away_team in premier_league_teams:
            if home_team != away_team:  # Team can't play against itself
                fixtures.append((home_team, away_team))
    
    # Shuffle fixtures to simulate realistic fixture scheduling
    random.shuffle(fixtures)
    
    return fixtures

def generate_season_schedule(season_year, fixtures):
    """Generate realistic match schedule for a complete season"""
    # Season start and end dates
    season_dates = {
        "2019-20": (datetime(2019, 8, 10), datetime(2020, 7, 26)),
        "2020-21": (datetime(2020, 9, 12), datetime(2021, 5, 23)),
        "2021-22": (datetime(2021, 8, 13), datetime(2022, 5, 22)),
        "2022-23": (datetime(2022, 8, 6), datetime(2023, 5, 28)),
        "2023-24": (datetime(2023, 8, 12), datetime(2024, 5, 19)),
        "2024-25": (datetime(2024, 8, 17), datetime(2025, 5, 25))
    }
    
    start_date, end_date = season_dates.get(season_year, (datetime(2024, 8, 17), datetime(2025, 5, 25)))
    
    # Calculate total matchweeks (38 matchweeks for Premier League)
    total_matchweeks = 38
    matches_per_week = 10  # 10 matches per week (20 teams, each plays once per week)
    
    scheduled_matches = []
    current_matchweek = 1
    fixture_index = 0
    
    # Distribute fixtures across 38 matchweeks
    while current_matchweek <= total_matchweeks and fixture_index < len(fixtures):
        # Calculate date for this matchweek
        weeks_elapsed = current_matchweek - 1
        
        # Most matches on weekends, some midweek
        if current_matchweek % 3 == 0:  # Every 3rd week has midweek games
            base_date = start_date + timedelta(weeks=weeks_elapsed, days=2)  # Tuesday
        else:
            base_date = start_date + timedelta(weeks=weeks_elapsed, days=5)  # Saturday
        
        # Add some random variation to dates
        date_variation = random.randint(-1, 2)  # -1 to +2 days variation
        match_date = base_date + timedelta(days=date_variation)
        
        # Ensure date is within season bounds
        if match_date > end_date:
            match_date = end_date - timedelta(days=random.randint(0, 7))
        
        # Schedule 10 matches for this matchweek
        week_matches = []
        for _ in range(matches_per_week):
            if fixture_index < len(fixtures):
                home_team, away_team = fixtures[fixture_index]
                week_matches.append((match_date, home_team, away_team, current_matchweek))
                fixture_index += 1
                
                # Add slight time variation for same-day matches
                match_date += timedelta(hours=random.choice([0, 2, 3]))
        
        scheduled_matches.extend(week_matches)
        current_matchweek += 1
    
    return scheduled_matches

def generate_season_data(season_year):
    """Generate complete season data"""
    print(f"Generating {season_year} season data...")
    
    # Generate complete fixture list (380 matches per season)
    fixtures = generate_complete_season_fixtures()
    
    # Generate schedule
    scheduled_matches = generate_season_schedule(season_year, fixtures)
    
    # Generate match data
    matches = []
    for i, (match_date, home_team, away_team, matchweek) in enumerate(scheduled_matches):
        # Generate score
        home_goals, away_goals = generate_realistic_score()
        
        # Determine result
        result = determine_result(home_goals, away_goals)
        
        # Generate additional stats
        stats = generate_match_stats(home_goals, away_goals)
        
        # Create match record
        match = {
            'Season': season_year,
            'Matchweek': matchweek,
            'Date': match_date.strftime('%d/%m/%y'),
            'HomeTeam': home_team,
            'AwayTeam': away_team,
            'FTHG': home_goals,      # Full Time Home Goals
            'FTAG': away_goals,      # Full Time Away Goals
            'FTR': result,           # Full Time Result
            'HS': stats['HS'],       # Home Shots
            'AS': stats['AS'],       # Away Shots
            'HST': stats['HST'],     # Home Shots on Target
            'AST': stats['AST'],     # Away Shots on Target
            'HC': stats['HC'],       # Home Corners
            'AC': stats['AC'],       # Away Corners
            'HF': stats['HF'],       # Home Fouls
            'AF': stats['AF'],       # Away Fouls
            'HY': stats['HY'],       # Home Yellow Cards
            'AY': stats['AY'],       # Away Yellow Cards
            'HR': stats['HR'],       # Home Red Cards
            'AR': stats['AR'],       # Away Red Cards
            'HP': stats['HP'],       # Home Possession %
            'AP': stats['AP'],       # Away Possession %
            'HPasses': stats['HPasses'],  # Home Passes
            'APasses': stats['APasses']   # Away Passes
        }
        
        matches.append(match)
        
        if (i + 1) % 100 == 0:
            print(f"  Generated {i + 1} matches for {season_year}...")
    
    print(f"  Completed {season_year}: {len(matches)} matches generated")
    return matches

def verify_season_completeness(df, season):
    """Verify that each team plays exactly 38 matches in the season"""
    season_data = df[df['Season'] == season]
    
    print(f"\n=== {season} Season Verification ===")
    
    for team in premier_league_teams:
        home_matches = len(season_data[season_data['HomeTeam'] == team])
        away_matches = len(season_data[season_data['AwayTeam'] == team])
        total_matches = home_matches + away_matches
        
        print(f"{team:18} - Home: {home_matches:2d}, Away: {away_matches:2d}, Total: {total_matches:2d}")
        
        if total_matches != 38:
            print(f"  ⚠️  WARNING: {team} has {total_matches} matches instead of 38!")
    
    total_season_matches = len(season_data)
    expected_matches = 380  # 20 teams × 19 opponents each = 380 total matches
    print(f"\nTotal matches in {season}: {total_season_matches} (Expected: {expected_matches})")

def main():
    """Main function to generate and save the dataset"""
    
    print("=== Premier League Multi-Season Complete Dataset Generator ===")
    print(f"Teams in the league: {len(premier_league_teams)}")
    print(f"Teams: {', '.join(premier_league_teams)}")
    print(f"Matches per team per season: 38")
    print(f"Total matches per season: 380 (each team plays 19 others twice)")
    print()
    
    # Generate 6 seasons to get over 3000 rows
    seasons = ["2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
    all_matches = []
    
    for season in seasons:
        season_data = generate_season_data(season)
        all_matches.extend(season_data)
    
    # Create DataFrame
    df = pd.DataFrame(all_matches)
    
    # Sort by season and date
    df['DateObj'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    df = df.sort_values(['Season', 'DateObj']).reset_index(drop=True)
    df = df.drop('DateObj', axis=1)  # Remove temporary column
    
    # Display basic statistics
    print("\n=== Dataset Statistics ===")
    print(f"Total matches generated: {len(df)}")
    print(f"Seasons: {df['Season'].unique()}")
    print(f"Expected total: {len(seasons) * 380} matches")
    
    for season in seasons:
        season_data = df[df['Season'] == season]
        print(f"\n{season} Season:")
        print(f"  Matches: {len(season_data)}")
        print(f"  Date range: {season_data['Date'].min()} to {season_data['Date'].max()}")
        print(f"  Matchweeks: {season_data['Matchweek'].min()} to {season_data['Matchweek'].max()}")
    
    # Result distribution across all seasons
    print("\n=== Overall Result Distribution ===")
    result_counts = df['FTR'].value_counts()
    for result, count in result_counts.items():
        result_name = {'H': 'Home Wins', 'A': 'Away Wins', 'D': 'Draws'}[result]
        print(f"{result_name}: {count} ({count/len(df)*100:.1f}%)")
    
    # Goal statistics
    print("\n=== Goal Statistics ===")
    print(f"Average goals per match: {(df['FTHG'] + df['FTAG']).mean():.2f}")
    print(f"Highest scoring match: {df['FTHG'].max()}-{df['FTAG'].max()}")
    
    # Verify each team plays 38 matches per season (sample verification)
    verify_season_completeness(df, "2023-24")
    verify_season_completeness(df, "2024-25")
    
    # Save to CSV
    output_file = 'premier_league_6_seasons_complete.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✅ Complete dataset saved to: {output_file}")
    print(f"📊 Dataset contains {len(df)} total matches across {len(seasons)} seasons")
    
    # Display sample data from different seasons
    print("\n=== Sample Data (2019-20) ===")
    sample_2019 = df[df['Season'] == '2019-20'].head(5)
    print(sample_2019[['Season', 'Matchweek', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']].to_string(index=False))
    
    print("\n=== Sample Data (2024-25) ===")
    sample_2024 = df[df['Season'] == '2024-25'].head(5)
    print(sample_2024[['Season', 'Matchweek', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']].to_string(index=False))
    
    # Feature description
    print("\n=== Feature Descriptions ===")
    features = {
        'Season': 'Season year (2019-20 to 2024-25)',
        'Matchweek': 'Matchweek number (1-38)',
        'Date': 'Match date (dd/mm/yy)',
        'HomeTeam': 'Home team name',
        'AwayTeam': 'Away team name', 
        'FTHG': 'Full Time Home Goals',
        'FTAG': 'Full Time Away Goals',
        'FTR': 'Full Time Result (H=Home Win, D=Draw, A=Away Win)',
        'HS': 'Home Team Shots',
        'AS': 'Away Team Shots',
        'HST': 'Home Team Shots on Target',
        'AST': 'Away Team Shots on Target',
        'HC': 'Home Team Corners',
        'AC': 'Away Team Corners',
        'HF': 'Home Team Fouls',
        'AF': 'Away Team Fouls',
        'HY': 'Home Team Yellow Cards',
        'AY': 'Away Team Yellow Cards',
        'HR': 'Home Team Red Cards',
        'AR': 'Away Team Red Cards',
        'HP': 'Home Team Possession %',
        'AP': 'Away Team Possession %',
        'HPasses': 'Home Team Total Passes',
        'APasses': 'Away Team Total Passes'
    }
    
    for feature, description in features.items():
        print(f"{feature:10} - {description}")

if __name__ == "__main__":
    main()
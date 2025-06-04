import pandas as pd
import random
from itertools import combinations
from datetime import datetime, timedelta

# Get unique teams from the dataset
teams = ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton', 
     'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 
     'Liverpool', 'Luton Town', 'Man City', 'Man United', 'Newcastle', 
     'Nottingham Forest', 'Sheffield United', 'Tottenham', 'West Ham', 'Wolves']

# Create fixture list
fixtures = []
fixture_id = 1

# Generate round-robin fixtures (each team plays each other twice - home and away)
for round_num in range(2):  # Two rounds for home and away
  team_pairs = list(combinations(teams, 2))
  random.shuffle(team_pairs)  # Randomize fixture order
  
  for home_team, away_team in team_pairs:
    if round_num == 1:  # Second round - swap home and away
      home_team, away_team = away_team, home_team
    
    fixtures.append({
      'FixtureID': fixture_id,
      'HomeTeam': home_team,
      'AwayTeam': away_team,
      'Round': round_num + 1
    })
    fixture_id += 1

# Create a DataFrame and distribute fixtures across 38 matchweeks
fixtures_df = pd.DataFrame(fixtures)

# Distribute fixtures across 38 matchweeks (10 matches per week for 20 teams)
matchweeks = []
matches_per_week = 10
current_week = 1
start_date = datetime(2025, 5, 25)  # Premier League season start

for i in range(0, len(fixtures_df), matches_per_week):
  week_fixtures = fixtures_df.iloc[i:i+matches_per_week].copy()
  
  # Assign matchweek and dates
  for j, (idx, fixture) in enumerate(week_fixtures.iterrows()):
    match_date = start_date + timedelta(weeks=current_week-1, days=random.randint(0, 6))
    
    fixture_data = {
      'Matchweek': current_week,
      'Date': match_date.strftime('%d/%m/%Y'),
      'Time': f"{random.choice(['12:30', '15:00', '17:30', '20:00'])}",
      'HomeTeam': fixture['HomeTeam'],
      'AwayTeam': fixture['AwayTeam'],
      'Venue': f"{fixture['HomeTeam']} Stadium",
      'Status': 'Scheduled'
    }
    matchweeks.append(fixture_data)
  
  current_week += 1

# Create final fixtures DataFrame
fixture_schedule = pd.DataFrame(matchweeks)

# Save to CSV
fixture_schedule.to_csv('Dummy_Datasets/WebScrapping_Matches/premier_league_fixtures_2024-25.csv', index=False)

print(f"Generated {len(fixture_schedule)} fixtures across {fixture_schedule['Matchweek'].max()} matchweeks")
print("\nSample fixtures:")
print(fixture_schedule.head(10))

# Verify each team plays 38 matches
team_match_counts = {}
for _, row in fixture_schedule.iterrows():
  home_team = row['HomeTeam']
  away_team = row['AwayTeam']
  
  team_match_counts[home_team] = team_match_counts.get(home_team, 0) + 1
  team_match_counts[away_team] = team_match_counts.get(away_team, 0) + 1

print(f"\nMatch count verification:")
for team, count in sorted(team_match_counts.items()):
  print(f"{team}: {count} matches")
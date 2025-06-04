import pandas as pd
import numpy as np

# Create a sample dataset for 20 Premier League teams

# Define the 20 Premier League teams for 2023-24 season
teams = [
  'Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton',
  'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham',
  'Liverpool', 'Luton Town', 'Man City', 'Man United', 'Newcastle',
  'Nottingham Forest', 'Sheffield United', 'Tottenham', 'West Ham', 'Wolves'
]

# Set random seed for reproducibility
np.random.seed(42)

# Create realistic data based on typical Premier League statistics
# Assuming we're around matchweek 20 of the season
data = {
  'Team': teams,
  'HTP': np.round(np.random.uniform(0.8, 2.8, 20), 2),  # Home Team Points (normalized by MW)
  'ATP': np.round(np.random.uniform(0.8, 2.8, 20), 2),  # Away Team Points (normalized by MW)
  'HTGD': np.round(np.random.uniform(-1.5, 2.0, 20), 2),  # Home Team Goal Difference (normalized)
  'ATGD': np.round(np.random.uniform(-1.5, 2.0, 20), 2),  # Away Team Goal Difference (normalized)
  'DiffFormPts': np.random.randint(-12, 13, 20),  # Form Points Difference (last 5 matches)
  'HM1': np.random.choice(['W', 'D', 'L'], 20),  # Last match result
  'HM2': np.random.choice(['W', 'D', 'L'], 20),  # 2nd last match result
  'HM3': np.random.choice(['W', 'D', 'L'], 20),  # 3rd last match result
  'AM1': np.random.choice(['W', 'D', 'L'], 20),  # Away team last match
  'AM2': np.random.choice(['W', 'D', 'L'], 20),  # Away team 2nd last match
  'AM3': np.random.choice(['W', 'D', 'L'], 20),  # Away team 3rd last match
}

# Adjust some values to make them more realistic for top/bottom teams
# Top teams (higher points and goal difference)
top_teams = ['Man City', 'Arsenal', 'Liverpool', 'Newcastle']
for team in top_teams:
  idx = teams.index(team)
  data['HTP'][idx] = np.round(np.random.uniform(2.0, 2.8, 1)[0], 2)
  data['ATP'][idx] = np.round(np.random.uniform(2.0, 2.8, 1)[0], 2)
  data['HTGD'][idx] = np.round(np.random.uniform(0.5, 2.0, 1)[0], 2)
  data['ATGD'][idx] = np.round(np.random.uniform(0.5, 2.0, 1)[0], 2)
  data['DiffFormPts'][idx] = np.random.randint(3, 13, 1)[0]

# Bottom teams (lower points and goal difference)
bottom_teams = ['Sheffield United', 'Burnley', 'Luton Town']
for team in bottom_teams:
  idx = teams.index(team)
  data['HTP'][idx] = np.round(np.random.uniform(0.8, 1.4, 1)[0], 2)
  data['ATP'][idx] = np.round(np.random.uniform(0.8, 1.4, 1)[0], 2)
  data['HTGD'][idx] = np.round(np.random.uniform(-1.5, -0.5, 1)[0], 2)
  data['ATGD'][idx] = np.round(np.random.uniform(-1.5, -0.5, 1)[0], 2)
  data['DiffFormPts'][idx] = np.random.randint(-12, -3, 1)[0]

# Create DataFrame
premier_league_data = pd.DataFrame(data)

# Sort by HTP (Home Team Points) to show league table order
premier_league_data = premier_league_data.sort_values('HTP', ascending=False).reset_index(drop=True)

# Save to CSV
premier_league_data.to_csv('./Dummy_Datasets/Input_Features_For_EPL_Teams/premier_league_teams_sample.csv', index=False)

print("Premier League Teams Sample Dataset Created!")
print(f"Shape: {premier_league_data.shape}")
print("\nFirst 10 teams:")
print(premier_league_data.head(10))
print("\nDataset saved as 'premier_league_teams_sample.csv'")
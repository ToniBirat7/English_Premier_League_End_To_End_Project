#!/usr/bin/env python
"""
Simple script to load CSV data into the Django database
Run this after setting up Django: python load_csv_data.py
"""

import os
import sys
import django
import pandas as pd
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'football_backend.settings')
django.setup()

from football_api.models import Match, Team

def load_data():
    """Load CSV data into the database"""
    csv_file = 'Dummy_Datasets/premier_league_6_seasons_complete.csv'
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        print(f"   Current directory: {os.getcwd()}")
        return
    
    print(f"📖 Reading CSV file: {csv_file}")
    df = pd.read_csv(csv_file)
    
    print(f"📊 Found {len(df)} matches in CSV")
    print(f"🏆 Seasons: {df['Season'].unique()}")
    
    # Clear existing data
    print("🗑️ Clearing existing match data...")
    Match.objects.all().delete()
    
    matches_created = 0
    teams_created = set()
    
    for _, row in df.iterrows():
        try:
            # Parse date from DD/MM/YY format to proper date object
            date = datetime.strptime(row['Date'], '%d/%m/%y').date()
            
            # Create match
            match = Match.objects.create(
                date=date,
                home_team=row['HomeTeam'],
                away_team=row['AwayTeam'],
                fthg=int(row['FTHG']),
                ftag=int(row['FTAG']),
                ftr=row['FTR'],
                season=row['Season'],
                matchweek=int(row['Matchweek'])
            )
            
            matches_created += 1
            teams_created.add(row['HomeTeam'])
            teams_created.add(row['AwayTeam'])
            
        except Exception as e:
            print(f"❌ Error creating match: {e}")
            print(f"   Row data: {row.to_dict()}")
    
    # Create team objects
    print(f"👥 Creating team objects for {len(teams_created)} teams...")
    for team_name in teams_created:
        team, created = Team.objects.get_or_create(
            name=team_name,
            defaults={
                'short_name': team_name[:3].upper(),
            }
        )
        if created:
            print(f"   ✅ Created team: {team_name}")
    
    print(f"✅ Successfully loaded {matches_created} matches!")
    print(f"👥 Created/found {len(teams_created)} teams")
    
    # Show some stats
    print("\n📈 Database Statistics:")
    print(f"   Total matches: {Match.objects.count()}")
    print(f"   Total teams: {Team.objects.count()}")
    print(f"   Seasons: {', '.join(Match.objects.values_list('season', flat=True).distinct().order_by('season'))}")

if __name__ == '__main__':
    load_data()

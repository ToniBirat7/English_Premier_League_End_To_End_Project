#!/usr/bin/env python
"""
Simple script to verify the loaded data
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'football_backend.settings')
django.setup()

from football_api.models import Match, Team

def verify_data():
    """Verify the loaded data"""
    print('✅ Data Verification Report')
    print('=' * 40)
    
    # Basic counts
    match_count = Match.objects.count()
    team_count = Team.objects.count()
    
    print(f'📊 Total matches: {match_count}')
    print(f'👥 Total teams: {team_count}')
    
    if match_count > 0:
        # Show sample matches
        print('\n📋 Sample matches:')
        for match in Match.objects.all()[:5]:
            print(f'   {match.date} | {match.home_team} {match.fthg}-{match.ftag} {match.away_team} | {match.season}')
        
        # Show date range
        earliest = Match.objects.earliest('date')
        latest = Match.objects.latest('date')
        print(f'\n📅 Date range: {earliest.date} to {latest.date}')
        
        # Show seasons
        seasons = Match.objects.values_list('season', flat=True).distinct().order_by('season')
        print(f'\n🏆 Seasons: {", ".join(seasons)}')
        
        # Show teams
        teams = Team.objects.values_list('name', flat=True).order_by('name')
        print(f'\n👥 Teams: {", ".join(teams)}')
    else:
        print('❌ No matches found in database')

if __name__ == '__main__':
    verify_data()

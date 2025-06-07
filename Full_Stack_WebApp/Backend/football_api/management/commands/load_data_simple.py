import os
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from football_api.models import Match, Team


class Command(BaseCommand):
    help = 'Load Premier League match data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-file',
            type=str,
            help='Path to specific CSV file to load',
        )
        parser.add_argument(
            '--clear-data',
            action='store_true',
            help='Clear existing data before loading',
        )

    def handle(self, *args, **options):
        if options['clear_data']:
            self.stdout.write('Clearing existing data...')
            Match.objects.all().delete()
            Team.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Existing data cleared'))

        csv_file = options.get('csv_file')
        if not csv_file:
            self.stdout.write(self.style.ERROR('❌ Please provide --csv-file argument'))
            return

        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'❌ File not found: {csv_file}'))
            return

        self.stdout.write(f'Loading data from {csv_file}...')
        
        matches_loaded = 0
        teams_set = set()

        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                with transaction.atomic():
                    for row in reader:
                        try:
                            # Parse date
                            date_str = row['Date'].strip()
                            date_obj = self.parse_date(date_str)
                            
                            if not date_obj:
                                continue

                            # Get team names
                            home_team = row['HomeTeam'].strip()
                            away_team = row['AwayTeam'].strip()
                            teams_set.add(home_team)
                            teams_set.add(away_team)

                            # Determine season
                            season = self.get_season_from_date(date_obj)
                            
                            # Create match
                            match, created = Match.objects.get_or_create(
                                date=date_obj,
                                home_team=home_team,
                                away_team=away_team,
                                defaults={
                                    'fthg': int(row['FTHG']),
                                    'ftag': int(row['FTAG']),
                                    'ftr': row['FTR'].strip(),
                                    'season': season,
                                    'matchweek': 1,  # Simplified for now
                                }
                            )
                            
                            if created:
                                matches_loaded += 1

                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f'⚠️  Error processing row: {e}'))
                            continue

            # Create teams
            teams_created = 0
            for team_name in teams_set:
                team, created = Team.objects.get_or_create(
                    name=team_name,
                    defaults={'short_name': team_name[:3].upper()}
                )
                if created:
                    teams_created += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Loaded {matches_loaded} matches and {teams_created} teams'
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error loading data: {e}'))

    def parse_date(self, date_str):
        """Parse date string in various formats"""
        date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y', '%m/%d/%Y']
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        return None

    def get_season_from_date(self, date_obj):
        """Determine season from date"""
        year = date_obj.year
        if date_obj.month >= 8:
            return f"{year}-{str(year + 1)[2:]}"
        else:
            return f"{year - 1}-{str(year)[2:]}"

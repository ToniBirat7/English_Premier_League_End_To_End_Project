import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from football_api.models import Team, Match


class Command(BaseCommand):
    help = 'Load Premier League data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-path',
            type=str,
            help='Path to the CSV file (relative to project root)',
            default='Dummy_Datasets/premier_league_6_seasons_complete.csv'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force deletion of existing data without confirmation',
        )

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        
        # Build full path - if it's relative, make it relative to the Full_Stack_WebApp directory
        if not os.path.isabs(csv_path):
            # Go up to Backend, then up to Full_Stack_WebApp, then to the CSV path
            project_root = os.path.dirname(os.path.dirname(settings.BASE_DIR))
            full_csv_path = os.path.join(project_root, csv_path)
        else:
            full_csv_path = csv_path
        
        if not os.path.exists(full_csv_path):
            self.stdout.write(
                self.style.ERROR(f'CSV file not found: {full_csv_path}')
            )
            return

        self.stdout.write(f'Loading data from: {full_csv_path}')
        
        # Clear existing data
        if not options['force']:
            if input("This will delete all existing data. Continue? (y/N): ").lower() != 'y':
                self.stdout.write('Operation cancelled.')
                return
        
        self.stdout.write('Clearing existing data...')
        Match.objects.all().delete()
        Team.objects.all().delete()
        
        teams_created = set()
        matches_created = 0
        
        with open(full_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    # Parse date (CSV uses DD/MM/YY format like '15/08/19')
                    date_str = row['Date']
                    try:
                        # Try DD/MM/YY format first
                        date_obj = datetime.strptime(date_str, '%d/%m/%y').date()
                    except ValueError:
                        # Fallback to DD/MM/YYYY format
                        date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
                    
                    # Get team names
                    home_team_name = row['HomeTeam'].strip()
                    away_team_name = row['AwayTeam'].strip()
                    
                    # Create teams if they don't exist (for the Team model)
                    if home_team_name not in teams_created:
                        Team.objects.get_or_create(
                            name=home_team_name,
                            defaults={'short_name': home_team_name[:3].upper()}
                        )
                        teams_created.add(home_team_name)
                    
                    if away_team_name not in teams_created:
                        Team.objects.get_or_create(
                            name=away_team_name,
                            defaults={'short_name': away_team_name[:3].upper()}
                        )
                        teams_created.add(away_team_name)
                    
                    # Get match data
                    fthg = int(row['FTHG'])
                    ftag = int(row['FTAG'])
                    ftr = row['FTR']
                    
                    # Use season from CSV if available, otherwise determine from date
                    if 'Season' in row and row['Season']:
                        season = row['Season']
                    else:
                        # Determine season from date
                        year = date_obj.year
                        month = date_obj.month
                        
                        if month >= 8:  # August or later = start of new season
                            season = f"{year}-{str(year + 1)[2:]}"
                        else:  # Before August = end of previous season
                            season = f"{year - 1}-{str(year)[2:]}"
                    
                    # Get matchweek from CSV if available
                    matchweek = int(row.get('Matchweek', row.get('Wk', 1)))
                    
                    # Create match (using CharField for team names as per current model)
                    match, created = Match.objects.get_or_create(
                        date=date_obj,
                        home_team=home_team_name,
                        away_team=away_team_name,
                        defaults={
                            'fthg': fthg,
                            'ftag': ftag,
                            'ftr': ftr,
                            'season': season,
                            'matchweek': matchweek
                        }
                    )
                    
                    if created:
                        matches_created += 1
                    
                    matches_created += 1
                    
                    if matches_created % 100 == 0:
                        self.stdout.write(f'Processed {matches_created} matches...')
                
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error processing row: {row}')
                    )
                    self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
                    continue
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded {len(teams_created)} teams and {matches_created} matches'
            )
        )
        
        # Show some statistics
        self.stdout.write('\nData Summary:')
        self.stdout.write(f'Teams: {Team.objects.count()}')
        self.stdout.write(f'Matches: {Match.objects.count()}')
        self.stdout.write(f'Seasons: {Match.objects.values_list("season", flat=True).distinct().count()}')
        
        seasons = list(Match.objects.values_list('season', flat=True).distinct().order_by('season'))
        self.stdout.write(f'Available seasons: {", ".join(seasons)}')

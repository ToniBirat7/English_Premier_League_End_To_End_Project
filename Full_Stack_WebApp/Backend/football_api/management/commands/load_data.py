import os
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from football_api.models import Match, Team


class Command(BaseCommand):
    help = 'Load Premier League match data from CSV files'

    def handle(self, *args, **options):
        self.stdout.write('Hello from load_data command!')
        return
        if options['clear_data']:
            self.stdout.write('Clearing existing data...')
            Match.objects.all().delete()
            Team.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Existing data cleared'))

        if options['csv_file']:
            # Load single file
            self.load_csv_file(options['csv_file'])
        else:
            # Load from data directory
            data_dir = options['data_dir']
            if not os.path.exists(data_dir):
                self.stdout.write(
                    self.style.ERROR(f'❌ Data directory not found: {data_dir}')
                )
                return

            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            if not csv_files:
                self.stdout.write(
                    self.style.ERROR(f'❌ No CSV files found in: {data_dir}')
                )
                return

            self.stdout.write(f'Found {len(csv_files)} CSV files to load...')
            
            for csv_file in sorted(csv_files):
                file_path = os.path.join(data_dir, csv_file)
                self.load_csv_file(file_path)

        # Create team records for all teams found in matches
        self.create_teams()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Data loading completed! '
                f'Loaded {Match.objects.count()} matches and {Team.objects.count()} teams'
            )
        )

    def load_csv_file(self, file_path):
        """Load matches from a single CSV file"""
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'❌ File not found: {file_path}')
            )
            return

        filename = os.path.basename(file_path)
        self.stdout.write(f'Loading data from {filename}...')

        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                # Detect the CSV dialect
                sample = csvfile.read(1024)
                csvfile.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter

                reader = csv.DictReader(csvfile, delimiter=delimiter)
                
                # Check if required columns exist
                required_columns = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
                if not all(col in reader.fieldnames for col in required_columns):
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Missing required columns in {filename}. '
                            f'Required: {required_columns}, Found: {reader.fieldnames}'
                        )
                    )
                    return

                matches_loaded = 0
                with transaction.atomic():
                    for row in reader:
                        try:
                            # Parse date - try different formats
                            date_str = row['Date'].strip()
                            date_obj = self.parse_date(date_str)
                            
                            if not date_obj:
                                self.stdout.write(
                                    self.style.WARNING(f'⚠️  Invalid date format: {date_str}')
                                )
                                continue

                            # Determine season from date
                            season = self.get_season_from_date(date_obj)
                            
                            # Calculate matchweek (approximate)
                            matchweek = self.calculate_matchweek(date_obj, season)

                            # Create match record
                            match, created = Match.objects.get_or_create(
                                date=date_obj,
                                home_team=row['HomeTeam'].strip(),
                                away_team=row['AwayTeam'].strip(),
                                defaults={
                                    'fthg': int(row['FTHG']),
                                    'ftag': int(row['FTAG']),
                                    'ftr': row['FTR'].strip(),
                                    'season': season,
                                    'matchweek': matchweek,
                                }
                            )
                            
                            if created:
                                matches_loaded += 1

                        except (ValueError, KeyError) as e:
                            self.stdout.write(
                                self.style.WARNING(f'⚠️  Error processing row: {e}')
                            )
                            continue

                self.stdout.write(
                    self.style.SUCCESS(f'✅ Loaded {matches_loaded} matches from {filename}')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error loading {filename}: {e}')
            )

    def parse_date(self, date_str):
        """Parse date string in various formats"""
        date_formats = [
            '%Y-%m-%d',      # 2019-08-09
            '%d/%m/%Y',      # 09/08/2019
            '%d/%m/%y',      # 09/08/19
            '%m/%d/%Y',      # 08/09/2019
            '%d-%m-%Y',      # 09-08-2019
            '%Y/%m/%d',      # 2019/08/09
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        return None

    def get_season_from_date(self, date_obj):
        """Determine season from date (e.g., Aug 2019 -> 2019-20)"""
        year = date_obj.year
        if date_obj.month >= 8:  # Season starts in August
            return f"{year}-{str(year + 1)[2:]}"
        else:  # First half of year belongs to previous season
            return f"{year - 1}-{str(year)[2:]}"

    def calculate_matchweek(self, date_obj, season):
        """Calculate approximate matchweek based on date"""
        # Premier League typically starts in mid-August
        season_start_year = int(season.split('-')[0])
        season_start = datetime(season_start_year, 8, 15).date()
        
        if date_obj < season_start:
            # Handle dates before typical season start
            return 1
        
        days_diff = (date_obj - season_start).days
        week_number = (days_diff // 7) + 1
        
        # Cap at 38 matchweeks
        return min(max(week_number, 1), 38)

    def create_teams(self):
        """Create Team records for all teams found in matches"""
        team_names = set()
        
        # Get all unique team names from matches
        for match in Match.objects.all():
            team_names.add(match.home_team)
            team_names.add(match.away_team)

        teams_created = 0
        for team_name in team_names:
            team, created = Team.objects.get_or_create(
                name=team_name,
                defaults={
                    'short_name': team_name[:3].upper(),
                    'city': '',  # Will be populated later
                    'stadium': '',  # Will be populated later
                }
            )
            if created:
                teams_created += 1

        self.stdout.write(
            self.style.SUCCESS(f'✅ Created {teams_created} new team records')
        )

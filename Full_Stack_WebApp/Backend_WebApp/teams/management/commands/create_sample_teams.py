from django.core.management.base import BaseCommand
from teams.models import Team

class Command(BaseCommand):
    help = 'Creates sample Premier League teams'

    def handle(self, *args, **kwargs):
        teams_data = [
            {
                'name': 'Arsenal',
                'short_name': 'ARS',
                'stadium': 'Emirates Stadium',
                'city': 'London',
                'founded_year': 1886,
                'website': 'https://www.arsenal.com'
            },
            {
                'name': 'Chelsea',
                'short_name': 'CHE',
                'stadium': 'Stamford Bridge',
                'city': 'London',
                'founded_year': 1905,
                'website': 'https://www.chelseafc.com'
            },
            {
                'name': 'Liverpool',
                'short_name': 'LIV',
                'stadium': 'Anfield',
                'city': 'Liverpool',
                'founded_year': 1892,
                'website': 'https://www.liverpoolfc.com'
            },
            {
                'name': 'Manchester City',
                'short_name': 'MCI',
                'stadium': 'Etihad Stadium',
                'city': 'Manchester',
                'founded_year': 1880,
                'website': 'https://www.mancity.com'
            },
            {
                'name': 'Manchester United',
                'short_name': 'MUN',
                'stadium': 'Old Trafford',
                'city': 'Manchester',
                'founded_year': 1878,
                'website': 'https://www.manutd.com'
            }
        ]

        for team_data in teams_data:
            Team.objects.get_or_create(
                name=team_data['name'],
                defaults=team_data
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created team "{team_data["name"]}"')
            ) 
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Match(models.Model):
    """
    Model to store Premier League match data
    """
    RESULT_CHOICES = [
        ('H', 'Home Win'),
        ('A', 'Away Win'),
        ('D', 'Draw'),
    ]
    
    date = models.DateField(help_text="Match date")
    home_team = models.CharField(max_length=100, help_text="Home team name")
    away_team = models.CharField(max_length=100, help_text="Away team name")
    fthg = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text="Full Time Home Goals"
    )
    ftag = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text="Full Time Away Goals"
    )
    ftr = models.CharField(
        max_length=1,
        choices=RESULT_CHOICES,
        help_text="Full Time Result"
    )
    season = models.CharField(
        max_length=10,
        help_text="Season in format 2019-20"
    )
    matchweek = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(38)],
        help_text="Match week number"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'home_team']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['home_team']),
            models.Index(fields=['away_team']),
            models.Index(fields=['season']),
            models.Index(fields=['matchweek']),
        ]
        unique_together = ['date', 'home_team', 'away_team']

    def __str__(self):
        return f"{self.home_team} {self.fthg}-{self.ftag} {self.away_team} ({self.date})"

    @property
    def home_win(self):
        return self.ftr == 'H'
    
    @property
    def away_win(self):
        return self.ftr == 'A'
    
    @property
    def draw(self):
        return self.ftr == 'D'


class Team(models.Model):
    """
    Model to store team information
    """
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10)
    logo_url = models.URLField(blank=True, null=True)
    founded = models.IntegerField(blank=True, null=True)
    stadium = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_matches_played(self, season=None):
        """Get total matches played by this team"""
        queryset = Match.objects.filter(
            models.Q(home_team=self.name) | models.Q(away_team=self.name)
        )
        if season:
            queryset = queryset.filter(season=season)
        return queryset.count()
    
    def get_wins(self, season=None):
        """Get total wins by this team"""
        home_wins = Match.objects.filter(home_team=self.name, ftr='H')
        away_wins = Match.objects.filter(away_team=self.name, ftr='A')
        
        if season:
            home_wins = home_wins.filter(season=season)
            away_wins = away_wins.filter(season=season)
            
        return home_wins.count() + away_wins.count()
    
    def get_draws(self, season=None):
        """Get total draws by this team"""
        queryset = Match.objects.filter(
            models.Q(home_team=self.name) | models.Q(away_team=self.name),
            ftr='D'
        )
        if season:
            queryset = queryset.filter(season=season)
        return queryset.count()
    
    def get_losses(self, season=None):
        """Get total losses by this team"""
        home_losses = Match.objects.filter(home_team=self.name, ftr='A')
        away_losses = Match.objects.filter(away_team=self.name, ftr='H')
        
        if season:
            home_losses = home_losses.filter(season=season)
            away_losses = away_losses.filter(season=season)
            
        return home_losses.count() + away_losses.count()
    
    def get_goals_for(self, season=None):
        """Get total goals scored by this team"""
        home_goals = Match.objects.filter(home_team=self.name)
        away_goals = Match.objects.filter(away_team=self.name)
        
        if season:
            home_goals = home_goals.filter(season=season)
            away_goals = away_goals.filter(season=season)
            
        home_total = sum(match.fthg for match in home_goals)
        away_total = sum(match.ftag for match in away_goals)
        
        return home_total + away_total
    
    def get_goals_against(self, season=None):
        """Get total goals conceded by this team"""
        home_goals = Match.objects.filter(home_team=self.name)
        away_goals = Match.objects.filter(away_team=self.name)
        
        if season:
            home_goals = home_goals.filter(season=season)
            away_goals = away_goals.filter(season=season)
            
        home_total = sum(match.ftag for match in home_goals)
        away_total = sum(match.fthg for match in away_goals)
        
        return home_total + away_total
    
    def get_points(self, season=None):
        """Get total points for this team (3 for win, 1 for draw)"""
        wins = self.get_wins(season)
        draws = self.get_draws(season)
        return (wins * 3) + draws

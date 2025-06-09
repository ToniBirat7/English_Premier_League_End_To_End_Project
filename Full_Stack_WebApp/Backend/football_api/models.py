from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Match(models.Model):
    """
    Simplified Premier League Match model
    Stores only essential match data: Date, HomeTeam, AwayTeam, FTHG, FTAG, FTR
    """
    
    # Match Result Choices
    RESULT_CHOICES = [
        ('H', 'Home Win'),
        ('A', 'Away Win'),
        ('D', 'Draw'),
    ]
    
    # Essential match data
    date = models.DateField(help_text="Match date")
    home_team = models.CharField(max_length=50, help_text="Home team name")
    away_team = models.CharField(max_length=50, help_text="Away team name")
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
        help_text="Full Time Result (H/A/D)"
    )
    
    # Additional metadata for organization
    season = models.CharField(max_length=7, help_text="Season (e.g., '2023-24')")
    matchweek = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(38)],
        help_text="Match week number"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', 'home_team']
        verbose_name = "Match"
        verbose_name_plural = "Matches"
        unique_together = ['date', 'home_team', 'away_team']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['season']),
            models.Index(fields=['home_team']),
            models.Index(fields=['away_team']),
        ]
    
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
    
    @property
    def total_goals(self):
        return self.fthg + self.ftag
    
    @property
    def result_display(self):
        """Return a human-readable result description"""
        if self.ftr == 'H':
            return f"{self.home_team} {self.fthg}-{self.ftag} {self.away_team} (Home Win)"
        elif self.ftr == 'A':
            return f"{self.home_team} {self.fthg}-{self.ftag} {self.away_team} (Away Win)"
        else:
            return f"{self.home_team} {self.fthg}-{self.ftag} {self.away_team} (Draw)"


class Team(models.Model):
    """
    Premier League Team model for additional team information
    """
    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=3, unique=True)
    logo_url = models.URLField(blank=True, null=True)
    founded = models.IntegerField(blank=True, null=True)
    stadium = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Team"
        verbose_name_plural = "Teams"
    
    def __str__(self):
        return self.name
    
    def get_matches_played(self, season=None):
        queryset = Match.objects.filter(
            models.Q(home_team=self.name) | models.Q(away_team=self.name)
        )
        if season:
            queryset = queryset.filter(season=season)
        return queryset.count()
    
    def get_wins(self, season=None):
        queryset = Match.objects.filter(
            models.Q(home_team=self.name, ftr='H') | 
            models.Q(away_team=self.name, ftr='A')
        )
        if season:
            queryset = queryset.filter(season=season)
        return queryset.count()
    
    def get_draws(self, season=None):
        queryset = Match.objects.filter(
            models.Q(home_team=self.name, ftr='D') | 
            models.Q(away_team=self.name, ftr='D')
        )
        if season:
            queryset = queryset.filter(season=season)
        return queryset.count()
    
    def get_losses(self, season=None):
        queryset = Match.objects.filter(
            models.Q(home_team=self.name, ftr='A') | 
            models.Q(away_team=self.name, ftr='H')
        )
        if season:
            queryset = queryset.filter(season=season)
        return queryset.count()
    
    def get_goals_for(self, season=None):
        home_goals = Match.objects.filter(home_team=self.name)
        away_goals = Match.objects.filter(away_team=self.name)
        
        if season:
            home_goals = home_goals.filter(season=season)
            away_goals = away_goals.filter(season=season)
        
        home_total = sum(match.fthg for match in home_goals)
        away_total = sum(match.ftag for match in away_goals)
        return home_total + away_total
    
    def get_goals_against(self, season=None):
        home_goals = Match.objects.filter(home_team=self.name)
        away_goals = Match.objects.filter(away_team=self.name)
        
        if season:
            home_goals = home_goals.filter(season=season)
            away_goals = away_goals.filter(season=season)
        
        home_total = sum(match.ftag for match in home_goals)
        away_total = sum(match.fthg for match in away_goals)
        return home_total + away_total
    
    def get_points(self, season=None):
        wins = self.get_wins(season)
        draws = self.get_draws(season)
        return (wins * 3) + draws

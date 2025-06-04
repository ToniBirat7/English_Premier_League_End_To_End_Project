from django.db import models
from django.utils import timezone

class Match(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('finished', 'Finished'),
        ('postponed', 'Postponed'),
        ('cancelled', 'Cancelled'),
    ]

    home_team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='away_matches')
    match_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    stadium = models.CharField(max_length=100)
    season = models.CharField(max_length=9)  # Format: 2023-2024
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-match_date']
        verbose_name_plural = 'Matches'

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.match_date.strftime('%Y-%m-%d %H:%M')}"

    @property
    def is_live(self):
        return self.status == 'live'

    @property
    def is_finished(self):
        return self.status == 'finished' 
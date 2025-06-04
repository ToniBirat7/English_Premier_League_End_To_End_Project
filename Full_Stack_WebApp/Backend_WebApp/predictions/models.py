from django.db import models
from matches.models import Match

class Prediction(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='predictions')
    home_win_probability = models.FloatField()
    draw_probability = models.FloatField()
    away_win_probability = models.FloatField()
    predicted_score_home = models.IntegerField()
    predicted_score_away = models.IntegerField()
    confidence_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Predictions'

    def __str__(self):
        return f"Prediction for {self.match} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @property
    def predicted_winner(self):
        if self.home_win_probability > self.away_win_probability and self.home_win_probability > self.draw_probability:
            return self.match.home_team
        elif self.away_win_probability > self.home_win_probability and self.away_win_probability > self.draw_probability:
            return self.match.away_team
        else:
            return "Draw" 
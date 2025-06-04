from rest_framework import serializers
from .models import Prediction
from matches.models import Match
from matches.serializers import MatchSerializer

class PredictionSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    match_id = serializers.PrimaryKeyRelatedField(
        queryset=Match.objects.all(),
        source='match',
        write_only=True
    )

    class Meta:
        model = Prediction
        fields = [
            'id', 'match', 'match_id', 'home_win_probability',
            'draw_probability', 'away_win_probability',
            'predicted_score_home', 'predicted_score_away',
            'confidence_score', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at'] 
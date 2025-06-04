from rest_framework import serializers
from .models import Match
from teams.models import Team
from teams.serializers import TeamSerializer

class MatchSerializer(serializers.ModelSerializer):
    home_team = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        required=True
    )
    away_team = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        required=True
    )
    home_team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='home_team',
        write_only=True
    )
    away_team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='away_team',
        write_only=True
    )

    class Meta:
        model = Match
        fields = [
            'id', 'home_team', 'away_team', 'home_team_id', 'away_team_id',
            'match_date', 'status', 'home_score', 'away_score',
            'stadium', 'season', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at'] 
from rest_framework import serializers
from django.db import models
from .models import Match, Team


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model with computed statistics"""
    wins = serializers.ReadOnlyField()
    losses = serializers.ReadOnlyField()
    draws = serializers.ReadOnlyField()
    goals_for = serializers.ReadOnlyField()
    goals_against = serializers.ReadOnlyField()
    goal_difference = serializers.ReadOnlyField()
    points = serializers.ReadOnlyField()
    matches_played = serializers.ReadOnlyField()

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'wins', 'losses', 'draws', 
            'goals_for', 'goals_against', 'goal_difference', 
            'points', 'matches_played'
        ]


class MatchSerializer(serializers.ModelSerializer):
    """Serializer for Match model with team details"""
    result_display = serializers.ReadOnlyField()

    class Meta:
        model = Match
        fields = [
            'id', 'date', 'home_team', 'away_team', 
            'fthg', 'ftag', 'ftr', 'result_display',
            'season', 'matchweek'
        ]


class MatchDetailSerializer(serializers.ModelSerializer):
    """Detailed match serializer with full team information"""
    home_team_name = serializers.CharField(source='home_team', read_only=True)
    away_team_name = serializers.CharField(source='away_team', read_only=True)
    result_display = serializers.ReadOnlyField()

    class Meta:
        model = Match
        fields = [
            'id', 'date', 'home_team_name', 'away_team_name',
            'fthg', 'ftag', 'ftr', 'result_display',
            'season', 'matchweek'
        ]


class TeamStandingSerializer(serializers.ModelSerializer):
    """Serializer for league table standings"""
    wins = serializers.ReadOnlyField()
    losses = serializers.ReadOnlyField()
    draws = serializers.ReadOnlyField()
    goals_for = serializers.ReadOnlyField()
    goals_against = serializers.ReadOnlyField()
    goal_difference = serializers.ReadOnlyField()
    points = serializers.ReadOnlyField()
    matches_played = serializers.ReadOnlyField()
    
    # Additional computed fields for standings
    form = serializers.SerializerMethodField()
    
    def get_form(self, obj):
        """Get last 5 matches form"""
        recent_matches = Match.objects.filter(
            models.Q(home_team=obj) | models.Q(away_team=obj)
        ).order_by('-date')[:5]
        
        form_list = []
        for match in reversed(recent_matches):
            if match.home_team == obj:
                if match.ftr == 'H':
                    form_list.append('W')
                elif match.ftr == 'A':
                    form_list.append('L')
                else:
                    form_list.append('D')
            else:  # away team
                if match.ftr == 'A':
                    form_list.append('W')
                elif match.ftr == 'H':
                    form_list.append('L')
                else:
                    form_list.append('D')
        
        return ''.join(form_list)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'matches_played', 'wins', 'draws', 'losses',
            'goals_for', 'goals_against', 'goal_difference', 'points', 'form'
        ]

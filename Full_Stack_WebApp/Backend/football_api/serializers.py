from rest_framework import serializers
from .models import Match, Team


class MatchSerializer(serializers.ModelSerializer):
    """
    Serializer for Match model with additional computed fields
    """
    home_win = serializers.ReadOnlyField()
    away_win = serializers.ReadOnlyField()
    draw = serializers.ReadOnlyField()
    
    class Meta:
        model = Match
        fields = [
            'id', 'date', 'home_team', 'away_team', 'fthg', 'ftag', 'ftr',
            'season', 'matchweek', 'home_win', 'away_win', 'draw',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MatchListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing matches
    """
    class Meta:
        model = Match
        fields = [
            'id', 'date', 'home_team', 'away_team', 'fthg', 'ftag', 'ftr', 'season'
        ]


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for Team model
    """
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'short_name', 'logo_url', 'founded', 'stadium', 'city'
        ]


class TeamStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for Team model with statistics
    """
    matches_played = serializers.SerializerMethodField()
    wins = serializers.SerializerMethodField()
    draws = serializers.SerializerMethodField()
    losses = serializers.SerializerMethodField()
    goals_for = serializers.SerializerMethodField()
    goals_against = serializers.SerializerMethodField()
    goal_difference = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'short_name', 'logo_url', 'stadium', 'city',
            'matches_played', 'wins', 'draws', 'losses', 'goals_for',
            'goals_against', 'goal_difference', 'points'
        ]
    
    def get_season(self):
        """Get season from context if provided"""
        return self.context.get('season')
    
    def get_matches_played(self, obj):
        return obj.get_matches_played(self.get_season())
    
    def get_wins(self, obj):
        return obj.get_wins(self.get_season())
    
    def get_draws(self, obj):
        return obj.get_draws(self.get_season())
    
    def get_losses(self, obj):
        return obj.get_losses(self.get_season())
    
    def get_goals_for(self, obj):
        return obj.get_goals_for(self.get_season())
    
    def get_goals_against(self, obj):
        return obj.get_goals_against(self.get_season())
    
    def get_goal_difference(self, obj):
        goals_for = obj.get_goals_for(self.get_season())
        goals_against = obj.get_goals_against(self.get_season())
        return goals_for - goals_against
    
    def get_points(self, obj):
        return obj.get_points(self.get_season())


class LeagueTableSerializer(serializers.Serializer):
    """
    Serializer for league table data
    """
    position = serializers.IntegerField()
    team = TeamSerializer()
    matches_played = serializers.IntegerField()
    wins = serializers.IntegerField()
    draws = serializers.IntegerField()
    losses = serializers.IntegerField()
    goals_for = serializers.IntegerField()
    goals_against = serializers.IntegerField()
    goal_difference = serializers.IntegerField()
    points = serializers.IntegerField()
    form = serializers.ListField(child=serializers.CharField(), required=False)


class FixtureSerializer(serializers.ModelSerializer):
    """
    Serializer for upcoming fixtures
    """
    class Meta:
        model = Match
        fields = [
            'id', 'date', 'home_team', 'away_team', 'season', 'matchweek'
        ]

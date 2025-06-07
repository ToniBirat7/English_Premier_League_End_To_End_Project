from django.shortcuts import render
from django.db.models import Q, Count, Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict

from .models import Match, Team
from .serializers import (
    MatchSerializer, MatchListSerializer, TeamSerializer, 
    TeamStatsSerializer, LeagueTableSerializer, FixtureSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class MatchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Premier League matches
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['season', 'home_team', 'away_team', 'ftr', 'matchweek']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MatchListSerializer
        return MatchSerializer
    
    def get_queryset(self):
        queryset = Match.objects.all()
        
        # Filter by date range
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
            
        # Filter by team (either home or away)
        team = self.request.query_params.get('team')
        if team:
            queryset = queryset.filter(Q(home_team=team) | Q(away_team=team))
            
        return queryset.order_by('-date', 'home_team')
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent matches (last 10)"""
        recent_matches = Match.objects.order_by('-date')[:10]
        serializer = MatchListSerializer(recent_matches, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_season(self, request):
        """Get matches grouped by season"""
        season = request.query_params.get('season')
        if not season:
            return Response({'error': 'Season parameter is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        matches = Match.objects.filter(season=season).order_by('matchweek', 'date')
        serializer = MatchListSerializer(matches, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def fixtures(self, request):
        """Get upcoming fixtures (future matches without results)"""
        # For demo purposes, we'll show matches from the latest season
        latest_season = Match.objects.order_by('-date').first()
        if not latest_season:
            return Response([])
            
        # Get some matches and pretend they're fixtures
        fixtures = Match.objects.filter(season=latest_season.season).order_by('date')[:20]
        serializer = FixtureSerializer(fixtures, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    def get_serializer_class(self):
        if self.action in ['stats', 'league_table']:
            return TeamStatsSerializer
        return TeamSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['season'] = self.request.query_params.get('season')
        return context
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get detailed statistics for a specific team"""
        team = self.get_object()
        season = request.query_params.get('season')
        
        serializer = TeamStatsSerializer(team, context={'season': season})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        """Get all matches for a specific team"""
        team = self.get_object()
        season = request.query_params.get('season')
        
        queryset = Match.objects.filter(
            Q(home_team=team.name) | Q(away_team=team.name)
        )
        
        if season:
            queryset = queryset.filter(season=season)
            
        queryset = queryset.order_by('-date')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MatchListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MatchListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def league_table(self, request):
        """Generate league table for a specific season"""
        season = request.query_params.get('season')
        
        if not season:
            # Get the latest season
            latest_match = Match.objects.order_by('-date').first()
            if not latest_match:
                return Response([])
            season = latest_match.season
        
        # Get all teams that played in this season
        team_names = set()
        matches = Match.objects.filter(season=season)
        for match in matches:
            team_names.add(match.home_team)
            team_names.add(match.away_team)
        
        # Calculate stats for each team
        table_data = []
        for team_name in team_names:
            # Try to get team object, create basic one if not exists
            try:
                team_obj = Team.objects.get(name=team_name)
            except Team.DoesNotExist:
                team_obj = Team(name=team_name, short_name=team_name[:3].upper())
            
            stats = {
                'team': team_obj,
                'matches_played': team_obj.get_matches_played(season) if hasattr(team_obj, 'get_matches_played') else 0,
                'wins': team_obj.get_wins(season) if hasattr(team_obj, 'get_wins') else 0,
                'draws': team_obj.get_draws(season) if hasattr(team_obj, 'get_draws') else 0,
                'losses': team_obj.get_losses(season) if hasattr(team_obj, 'get_losses') else 0,
                'goals_for': team_obj.get_goals_for(season) if hasattr(team_obj, 'get_goals_for') else 0,
                'goals_against': team_obj.get_goals_against(season) if hasattr(team_obj, 'get_goals_against') else 0,
                'points': team_obj.get_points(season) if hasattr(team_obj, 'get_points') else 0,
            }
            stats['goal_difference'] = stats['goals_for'] - stats['goals_against']
            table_data.append(stats)
        
        # Sort by points, then goal difference, then goals for
        table_data.sort(key=lambda x: (-x['points'], -x['goal_difference'], -x['goals_for']))
        
        # Add positions
        for i, team_stats in enumerate(table_data, 1):
            team_stats['position'] = i
        
        serializer = LeagueTableSerializer(table_data, many=True)
        return Response(serializer.data)


class StatsViewSet(viewsets.ViewSet):
    """
    ViewSet for general statistics and analytics
    """
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get general overview statistics"""
        season = request.query_params.get('season')
        
        queryset = Match.objects.all()
        if season:
            queryset = queryset.filter(season=season)
        
        total_matches = queryset.count()
        total_goals = queryset.aggregate(
            total=Sum('fthg') + Sum('ftag')
        )['total'] or 0
        
        home_wins = queryset.filter(ftr='H').count()
        away_wins = queryset.filter(ftr='A').count()
        draws = queryset.filter(ftr='D').count()
        
        avg_goals_per_match = round(total_goals / total_matches, 2) if total_matches > 0 else 0
        
        # Get top scorers (teams with most goals)
        team_goals = defaultdict(int)
        for match in queryset:
            team_goals[match.home_team] += match.fthg
            team_goals[match.away_team] += match.ftag
        
        top_scorers = sorted(team_goals.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return Response({
            'total_matches': total_matches,
            'total_goals': total_goals,
            'average_goals_per_match': avg_goals_per_match,
            'home_wins': home_wins,
            'away_wins': away_wins,
            'draws': draws,
            'home_win_percentage': round((home_wins / total_matches) * 100, 1) if total_matches > 0 else 0,
            'away_win_percentage': round((away_wins / total_matches) * 100, 1) if total_matches > 0 else 0,
            'draw_percentage': round((draws / total_matches) * 100, 1) if total_matches > 0 else 0,
            'top_scoring_teams': [{'team': team, 'goals': goals} for team, goals in top_scorers],
            'season': season
        })
    
    @action(detail=False, methods=['get'])
    def seasons(self, request):
        """Get list of available seasons"""
        seasons = Match.objects.values_list('season', flat=True).distinct().order_by('-season')
        return Response(list(seasons))

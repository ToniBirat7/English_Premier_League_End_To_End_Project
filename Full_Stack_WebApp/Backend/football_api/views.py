from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Match, Team
from .serializers import (
    MatchSerializer, MatchDetailSerializer, 
    TeamSerializer, TeamStandingSerializer
)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Team model with standings and statistics"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def standings(self, request):
        """Get league table standings sorted by points"""
        season = request.query_params.get('season', None)
        teams = self.get_queryset()
        
        if season:
            # Filter teams that played in the specified season
            teams = teams.filter(
                Q(home_matches__season=season) | Q(away_matches__season=season)
            ).distinct()
        
        # Sort by points (descending), then goal difference, then goals for
        teams_data = []
        for team in teams:
            team_stats = {
                'id': team.id,
                'name': team.name,
                'matches_played': team.matches_played,
                'wins': team.wins,
                'draws': team.draws,
                'losses': team.losses,
                'goals_for': team.goals_for,
                'goals_against': team.goals_against,
                'goal_difference': team.goal_difference,
                'points': team.points,
            }
            teams_data.append(team_stats)
        
        # Sort by points, goal difference, goals for
        teams_data.sort(
            key=lambda x: (-x['points'], -x['goal_difference'], -x['goals_for'])
        )
        
        # Add position
        for i, team in enumerate(teams_data, 1):
            team['position'] = i
        
        return Response(teams_data)

    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        """Get all matches for a specific team"""
        team = self.get_object()
        matches = Match.objects.filter(
            Q(home_team=team) | Q(away_team=team)
        ).order_by('-date')
        
        # Apply season filter if provided
        season = request.query_params.get('season', None)
        if season:
            matches = matches.filter(season=season)
        
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Match model with filtering and search"""
    queryset = Match.objects.all().select_related('home_team', 'away_team')
    serializer_class = MatchSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['season', 'matchweek', 'ftr']
    ordering_fields = ['date', 'matchweek']
    ordering = ['-date']

    def get_serializer_class(self):
        """Use detailed serializer for individual match retrieval"""
        if self.action == 'retrieve':
            return MatchDetailSerializer
        return MatchSerializer

    def get_queryset(self):
        """Custom queryset with optional filtering"""
        queryset = super().get_queryset()
        
        # Filter by teams
        home_team = self.request.query_params.get('home_team', None)
        away_team = self.request.query_params.get('away_team', None)
        team = self.request.query_params.get('team', None)
        
        if home_team:
            queryset = queryset.filter(home_team__name__icontains=home_team)
        
        if away_team:
            queryset = queryset.filter(away_team__name__icontains=away_team)
        
        if team:
            queryset = queryset.filter(
                Q(home_team__name__icontains=team) | 
                Q(away_team__name__icontains=team)
            )
        
        # Filter by date range
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        return queryset

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent matches (last 10)"""
        matches = self.get_queryset()[:10]
        serializer = self.get_serializer(matches, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming matches (future dates)"""
        from django.utils import timezone
        matches = self.get_queryset().filter(date__gt=timezone.now().date())[:10]
        serializer = self.get_serializer(matches, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_matchweek(self, request):
        """Get matches grouped by matchweek"""
        season = request.query_params.get('season', None)
        matchweek = request.query_params.get('matchweek', None)
        
        queryset = self.get_queryset()
        
        if season:
            queryset = queryset.filter(season=season)
        
        if matchweek:
            queryset = queryset.filter(matchweek=matchweek)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get match statistics summary"""
        queryset = self.get_queryset()
        season = request.query_params.get('season', None)
        
        if season:
            queryset = queryset.filter(season=season)
        
        stats = {
            'total_matches': queryset.count(),
            'home_wins': queryset.filter(ftr='H').count(),
            'away_wins': queryset.filter(ftr='A').count(),
            'draws': queryset.filter(ftr='D').count(),
            'total_goals': sum(match.fthg + match.ftag for match in queryset),
            'average_goals_per_match': 0,
        }
        
        if stats['total_matches'] > 0:
            stats['average_goals_per_match'] = round(
                stats['total_goals'] / stats['total_matches'], 2
            )
        
        return Response(stats)

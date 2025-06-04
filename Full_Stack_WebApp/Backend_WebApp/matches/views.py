from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Match
from .serializers import MatchSerializer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['home_team__name', 'away_team__name', 'stadium', 'season']
    ordering_fields = ['match_date', 'created_at', 'updated_at']
    ordering = ['-match_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset 
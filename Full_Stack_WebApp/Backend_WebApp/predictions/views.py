from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Prediction
from .serializers import PredictionSerializer

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['match__home_team__name', 'match__away_team__name']
    ordering_fields = ['created_at', 'confidence_score']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        match_id = self.request.query_params.get('match_id', None)
        if match_id:
            queryset = queryset.filter(match_id=match_id)
        return queryset 
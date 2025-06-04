from rest_framework import viewsets, filters
from rest_framework.response import Response
from .models import Team
from .serializers import TeamSerializer
import logging

logger = logging.getLogger(__name__)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'short_name', 'city', 'stadium']
    ordering_fields = ['name', 'city', 'founded_year']
    ordering = ['name']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 
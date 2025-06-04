from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Team
from .serializers import TeamSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'short_name', 'city', 'stadium']
    ordering_fields = ['name', 'city', 'founded_year']
    ordering = ['name'] 
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatchViewSet, TeamViewSet, StatsViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'matches', MatchViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'stats', StatsViewSet, basename='stats')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),
]

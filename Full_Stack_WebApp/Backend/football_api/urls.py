from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'teams', views.TeamViewSet)
router.register(r'matches', views.MatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

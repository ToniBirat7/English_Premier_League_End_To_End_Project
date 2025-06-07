from django.contrib import admin
from .models import Match, Team


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['date', 'home_team', 'away_team', 'fthg', 'ftag', 'ftr', 'season', 'matchweek']
    list_filter = ['season', 'ftr', 'matchweek', 'date']
    search_fields = ['home_team', 'away_team']
    ordering = ['-date', 'home_team']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Match Information', {
            'fields': ('date', 'season', 'matchweek')
        }),
        ('Teams', {
            'fields': ('home_team', 'away_team')
        }),
        ('Result', {
            'fields': ('fthg', 'ftag', 'ftr')
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'city', 'stadium', 'founded']
    search_fields = ['name', 'city', 'stadium']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'short_name', 'logo_url')
        }),
        ('Details', {
            'fields': ('founded', 'stadium', 'city')
        }),
    )

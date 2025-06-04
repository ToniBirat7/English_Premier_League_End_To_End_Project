from rest_framework import serializers
from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'short_name', 'logo', 'stadium',
            'city', 'founded_year', 'website'
        ]
        read_only_fields = ['id'] 
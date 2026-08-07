from rest_framework import serializers
from .models import Incident

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = [
            'id', 'title', 'description', 'location', 
            'category', 'status', 'is_tfgbv', 'evidence_file', 
            'created_at', 'updated_at'
        ]
        # Read-only fields that citizens shouldn't spoof on creation
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

class IncidentUpdateSerializer(serializers.ModelSerializer):
    """Specialized serializer for Fact-Checkers to update status/tags"""
    class Meta:
        model = Incident
        fields = ['status', 'is_tfgbv']
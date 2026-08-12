from rest_framework import serializers
from .models import Incident, SocialPost


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = [
            # Auto-generated & Status fields
            'id', 
            'status', 
            'created_at', 
            'updated_at',
            
            # Base text fields (Default language)
            'title', 
            'claim',
            'description', 
            
            # English Translations
            'title_en', 
            'claim_en',
            'summary_en',
            
            # Yoruba Translations
            'title_yo', 
            'claim_yo',
            'summary_yo',
            
            # Pidgin Translations
            'title_pcm', 
            'claim_pcm',
            'summary_pcm',
            
            # Incident Details & Metadata
            'location', 
            'category', 
            'is_tfgbv', 
            'is_anonymous',
            'evidence_file'
        ]
        
        # Read-only fields that citizens shouldn't spoof on creation
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class IncidentUpdateSerializer(serializers.ModelSerializer):
    """Specialized serializer for Fact-Checkers to update status/tags"""
    class Meta:
        model = Incident
        # We only expose the fields fact-checkers are allowed to change
        fields = ['status', 'is_tfgbv']


class SocialPostSerializer(serializers.ModelSerializer):
    """Serializer for the Social Listening feed"""
    class Meta:
        model = SocialPost
        fields = '__all__'
from rest_framework import serializers
from .models import Incident, SocialPost


class IncidentSerializer(serializers.ModelSerializer):
    # Optional: Alias field in case frontend posts 'image' instead of 'evidence_file'
    image = serializers.FileField(source='evidence_file', required=False, allow_null=True, write_only=True)

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
            'evidence_file',
            'image',  # Write-only alias for evidence_file
        ]
        
        # Read-only fields that citizens shouldn't spoof on creation
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

        # Make public form fields optional so Django doesn't reject missing/empty inputs
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True, 'default': ''},
            'claim': {'required': False, 'allow_blank': True, 'default': ''},
            'location': {'required': False, 'allow_blank': True, 'default': ''},
            'category': {'required': False, 'allow_blank': True},
            'is_anonymous': {'required': False},
            'is_tfgbv': {'required': False},
            'evidence_file': {'required': False, 'allow_null': True},
        }

    def validate(self, attrs):
        """
        Fallback logic: If frontend sends 'claim' (WETIN DEM TALK) or 'title' 
        but leaves 'description' empty, automatically use 'claim' as the description.
        """
        if not attrs.get('description'):
            attrs['description'] = attrs.get('claim') or attrs.get('title') or ''
        return super().validate(attrs)


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
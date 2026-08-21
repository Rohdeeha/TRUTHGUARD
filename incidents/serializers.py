from rest_framework import serializers
from .models import Incident, FactCheckArticle, SocialPost

class IncidentSerializer(serializers.ModelSerializer):
    # 1. WRITE-ONLY ALIASES: Accepts 'image' or 'media' from frontend FormData
    image = serializers.FileField(source='evidence_file', required=False, allow_null=True, write_only=True)
    media = serializers.FileField(source='evidence_file', required=False, allow_null=True, write_only=True)

    # 2. READ-ONLY URL GETTERS: Always outputs complete HTTPS URLs
    evidence_file = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    # 3. HUMAN-READABLE DISPLAY LABELS
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Incident
        fields = [
            'id', 
            'status', 
            'status_display',
            'created_at', 
            'updated_at',
            'claim',
            'who_said_it',
            'where_and_when',
            'location', 
            'category', 
            'category_display',
            'is_tfgbv', 
            'is_anonymous',
            'evidence_file',
            'image_url',
            'image', 
            'media', 
        ]
        
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

        extra_kwargs = {
            'claim': {'required': False, 'allow_blank': True, 'default': ''},
            'location': {'required': False, 'allow_blank': True, 'default': ''},
            'category': {'required': False, 'allow_blank': True},
            'is_anonymous': {'required': False},
            'is_tfgbv': {'required': False},
        }

    def get_evidence_file(self, obj):
        if not obj.evidence_file:
            return None
            
        try:
            url = obj.evidence_file.url
        except Exception:
            url = str(obj.evidence_file)

        if url.startswith('http://') or url.startswith('https://'):
            return url

        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(url)

        return f"https://truthguard-api-sut7.onrender.com{url}"

    def get_image_url(self, obj):
        return self.get_evidence_file(obj)


class FactCheckArticleSerializer(serializers.ModelSerializer):
    """Serializer for the published fact-check feed"""
    # related_incidents is a ManyToMany field, so we must use many=True
    incident_details = IncidentSerializer(source='related_incidents', many=True, read_only=True)
    
    # Updated to match your model's 'featured_image' name
    featured_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FactCheckArticle
        fields = [
            'id',
            'title',
            'byline',               # Now pulling directly from your model's byline field
            'verdict',
            'content',
            'featured_image',       # Corrected from cover_image
            'featured_image_url',   # Corrected from cover_image_url
            'related_incidents',    # Corrected from incident
            'incident_details',
            'fact_checker',         # Corrected from author
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_featured_image_url(self, obj):
        if not obj.featured_image:
            return None
        try:
            url = obj.featured_image.url
        except Exception:
            url = str(obj.featured_image)
            
        if url.startswith('http://') or url.startswith('https://'):
            return url
            
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(url)
            
        return f"https://truthguard-api-sut7.onrender.com{url}"


class IncidentUpdateSerializer(serializers.ModelSerializer):
    """Specialized serializer for Fact-Checkers to update status/tags"""
    class Meta:
        model = Incident
        fields = ['status', 'is_tfgbv']


class SocialPostSerializer(serializers.ModelSerializer):
    """Serializer for the Social Listening feed"""
    class Meta:
        model = SocialPost
        fields = '__all__'
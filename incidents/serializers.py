from rest_framework import serializers
from .models import Incident, SocialPost


class IncidentSerializer(serializers.ModelSerializer):
    # 1. WRITE-ONLY ALIASES: Accepts 'image' or 'media' from frontend FormData
    image = serializers.FileField(source='evidence_file', required=False, allow_null=True, write_only=True)
    media = serializers.FileField(source='evidence_file', required=False, allow_null=True, write_only=True)

    # 2. READ-ONLY URL GETTERS: Always outputs complete HTTPS URLs
    evidence_file = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField() # Extra helper field for frontend

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
            
            # Media Output Fields (Read-Only)
            'evidence_file',
            'image_url',
            
            # Media Input Aliases (Write-Only)
            'image', 
            'media', 
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
        }

    def get_evidence_file(self, obj):
        """Safely extracts full HTTPS Cloudinary URL string or appends API domain"""
        if not obj.evidence_file:
            return None
            
        try:
            url = obj.evidence_file.url
        except Exception:
            url = str(obj.evidence_file)

        # 1. If it's already an absolute URL (Cloudinary), return as is
        if url.startswith('http://') or url.startswith('https://'):
            return url

        # 2. If it's a relative path, construct absolute URI using request context
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(url)

        # 3. Fallback: Prepend backend Render domain
        return f"https://truthguard-api-sut7.onrender.com{url}"

    def get_image_url(self, obj):
        """Alias URL helper for frontend team convenience"""
        return self.get_evidence_file(obj)

    def validate(self, attrs):
        """
        Fallback logic: If frontend sends 'claim' or 'title' 
        but leaves 'description' empty, automatically use 'claim' as description.
        """
        if not attrs.get('description'):
            attrs['description'] = attrs.get('claim') or attrs.get('title') or ''
        return super().validate(attrs)


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
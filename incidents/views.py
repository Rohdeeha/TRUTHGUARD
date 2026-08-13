import io
import requests
import cloudinary.utils
from django.conf import settings
from django.db.models import Count, F
from django.db.models.functions import TruncDate, TruncHour
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsFactChecker, IsTFGBVLegalExpert
from .models import Incident, SocialPost
from .serializers import (
    IncidentSerializer,
    IncidentUpdateSerializer,
    SocialPostSerializer,
)
from .utils import hash_phone_number, sanitize_and_upload_image


class DebunkedFeedPagination(PageNumberPagination):
    """Custom pagination setting 10 items per page for the public feed."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class CitizenIncidentCreateView(generics.CreateAPIView):
    """Task 1 & 2: Public, unauthenticated endpoint for citizens to submit reports."""
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [AllowAny]


class PublicDebunkedFeedView(generics.ListAPIView):
    """Task 3 & 4: Public feed showing debunked/false incidents with pagination (10/page)."""
    queryset = Incident.objects.filter(
        status__in=['FALSE', 'MISLEADING', 'VERIFIED_FALSE', 'Debunked', 'Debunked False']
    ).order_by('-created_at')
    serializer_class = IncidentSerializer
    permission_classes = [AllowAny]
    pagination_class = DebunkedFeedPagination


class KanbanTriageView(generics.ListAPIView):
    """
    Internal Triage Queue for Fact-Checkers / Situation Room.
    Temporarily set permission_classes to AllowAny so missing JWT tokens on frontend don't block requests.
    """
    serializer_class = IncidentSerializer
    permission_classes = [AllowAny]  # TODO: Revert to [IsAuthenticated] or [IsFactChecker] when auth flow is active
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location', 'category']
    filterset_fields = ['status', 'is_tfgbv']

    def get_queryset(self):
        queryset = Incident.objects.all().order_by('-created_at')
        
        # If frontend requests a specific status filter (e.g. ?status=Pending Review)
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status__iexact=status_param)
            
        return queryset


class IncidentStatusUpdateView(generics.UpdateAPIView):
    """Allows Fact-Checkers to patch ticket states (e.g., Pending -> Verified)."""
    queryset = Incident.objects.all()
    serializer_class = IncidentUpdateSerializer
    permission_classes = [AllowAny]  # TODO: Revert to [IsAuthenticated] in production
    http_method_names = ['patch']


class SpecializedTFGBVView(generics.ListAPIView):
    """Isolated secure queue exclusively fetching gender-based violence incidents."""
    queryset = Incident.objects.filter(is_tfgbv=True).order_by('-created_at')
    serializer_class = IncidentSerializer
    permission_classes = [AllowAny]


class SocialListeningFeedView(generics.ListAPIView):
    """Feed displaying real-time flagged social media posts for fact-checkers."""
    queryset = SocialPost.objects.filter(is_flagged=True).order_by('-posted_at')
    serializer_class = SocialPostSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['platform', 'sentiment']
    search_fields = ['content', 'keyword_tracked']


class IncidentAnalyticsView(APIView):
    """
    Analytics Dashboard View:
    Returns category percentage breakdown, hourly reporting trends,
    daily volume trends, and overall status summaries.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        total_incidents = Incident.objects.count() or 1  # Prevents division by zero

        # 1. Category Percentage Breakdown
        category_counts = (
            Incident.objects.values('category')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        category_breakdown = [
            {
                "category": item["category"],
                "count": item["count"],
                "percentage": round((item["count"] / total_incidents) * 100, 2)
            }
            for item in category_counts
        ]

        # 2. Hourly Report Volume
        hourly_volume = (
            Incident.objects.annotate(hour=TruncHour('created_at'))
            .values('hour')
            .annotate(count=Count('id'))
            .order_by('hour')
        )

        # 3. Daily Report Volume 
        volume_trend = (
            Incident.objects.annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        # 4. Status Summary 
        status_counts = (
            Incident.objects.values('status')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return Response({
            "total_incidents": total_incidents,
            "categories": category_breakdown,
            "hourly_volume": list(hourly_volume),
            "volume_trend": list(volume_trend),
            "status_summary": list(status_counts)
        })


class GenerateDebunkCardView(APIView):
    """
    Accepts a 'claim' and a 'fact', and returns a dynamically generated
    Cloudinary image URL with text overlaid on a base template.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        claim_text = request.data.get('claim')
        fact_text = request.data.get('fact')

        if not claim_text or not fact_text:
            return Response(
                {"error": "Both 'claim' and 'fact' fields are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        image_url, options = cloudinary.utils.cloudinary_url(
            "debunk_template",
            transformation=[
                {
                    "overlay": {"font_family": "Arial", "font_size": 35, "font_weight": "bold", "text": f"CLAIM: {claim_text}"},
                    "color": "#D32F2F", 
                    "y": -100,
                    "width": 600,
                    "crop": "fit"
                },
                {
                    "overlay": {"font_family": "Arial", "font_size": 35, "font_weight": "bold", "text": f"FACT: {fact_text}"},
                    "color": "#2E7D32", 
                    "y": 100,
                    "width": 600,
                    "crop": "fit"
                }
            ]
        )

        return Response({
            "message": "Debunk card generated successfully!",
            "card_url": image_url
        }, status=status.HTTP_200_OK)


class WhatsAppWebhookView(APIView):
    """
    Webhook listener for WhatsApp Cloud API.
    Handles Meta verification challenge (GET) and parses messages/media into Incident tickets (POST).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        mode = request.query_params.get('hub.mode')
        token = request.query_params.get('hub.verify_token')
        challenge = request.query_params.get('hub.challenge')

        verify_token = getattr(settings, 'WHATSAPP_VERIFY_TOKEN', 'truthguard_secret')
        if mode == 'subscribe' and token == verify_token:
            return Response(int(challenge), status=status.HTTP_200_OK)
        return Response({"error": "Verification token mismatch"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        data = request.data
        try:
            entries = data.get('entry', [])
            for entry in entries:
                changes = entry.get('changes', [])
                for change in changes:
                    value = change.get('value', {})
                    messages = value.get('messages', [])

                    for msg in messages:
                        phone_raw = msg.get('from', '')
                        hashed_phone = hash_phone_number(phone_raw)
                        msg_type = msg.get('type')
                        
                        body_text = ""
                        evidence_url = None

                        if msg_type == 'text':
                            body_text = msg.get('text', {}).get('body', '')

                        elif msg_type == 'image':
                            caption = msg.get('image', {}).get('caption', '')
                            body_text = caption or "Image report submitted via WhatsApp"
                            media_id = msg.get('image', {}).get('id')

                            headers = {"Authorization": f"Bearer {getattr(settings, 'WHATSAPP_ACCESS_TOKEN', '')}"}
                            media_res = requests.get(f"https://graph.facebook.com/v18.0/{media_id}", headers=headers)
                            
                            if media_res.status_code == 200:
                                download_url = media_res.json().get('url')
                                img_res = requests.get(download_url, headers=headers)
                                if img_res.status_code == 200:
                                    img_buffer = io.BytesIO(img_res.content)
                                    evidence_url = sanitize_and_upload_image(img_buffer)

                        if body_text:
                            Incident.objects.create(
                                title=f"WhatsApp Report [{hashed_phone[:8]}]",
                                description=body_text,
                                location="WhatsApp Webhook",
                                is_anonymous=True,
                                category="OTHER",
                                evidence_file=evidence_url
                            )

            return Response({"status": "SUCCESS"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
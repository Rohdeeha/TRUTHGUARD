import io
import requests
import cloudinary.utils
from django.conf import settings
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncHour
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from core.permissions import IsFactChecker, IsTFGBVLegalExpert
from .models import Incident, SocialPost, FactCheckArticle
from .serializers import (
    IncidentSerializer,
    IncidentUpdateSerializer,
    SocialPostSerializer,
    FactCheckArticleSerializer,
)
from .utils import hash_phone_number, sanitize_and_upload_image


class DebunkedFeedPagination(PageNumberPagination):
    """Custom pagination setting 10 items per page for the public feed."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class CitizenIncidentCreateView(generics.CreateAPIView):
    """Public, unauthenticated endpoint for citizens to submit reports."""
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)


class PublicDebunkedFeedView(generics.ListAPIView):
    """Public feed showing published fact-checks from the FactCheckArticle model."""
    queryset = FactCheckArticle.objects.select_related('fact_checker').order_by('-created_at')
    serializer_class = FactCheckArticleSerializer
    permission_classes = [AllowAny]
    pagination_class = DebunkedFeedPagination


class KanbanTriageView(generics.ListAPIView):
    """Internal Triage Queue for Fact-Checkers / Situation Room."""
    serializer_class = IncidentSerializer
    permission_classes = [AllowAny]  # TODO: Revert to [IsAuthenticated] in production
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['claim', 'who_said_it', 'where_and_when', 'location', 'category']
    filterset_fields = ['status', 'is_tfgbv']

    def get_queryset(self):
        queryset = Incident.objects.all().order_by('-created_at')
        
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status__iexact=status_param)
            
        return queryset


class IncidentStatusUpdateView(generics.UpdateAPIView):
    """Allows Fact-Checkers to patch ticket states."""
    queryset = Incident.objects.all()
    serializer_class = IncidentUpdateSerializer
    permission_classes = [AllowAny]  # TODO: Revert to [IsAuthenticated] in production
    http_method_names = ['patch']

    def perform_update(self, serializer):
        if self.request.user and self.request.user.is_authenticated:
            serializer.save(fact_checker=self.request.user)
        else:
            serializer.save()


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
    """Analytics Dashboard View: category breakdown, volume trends, and status summaries."""
    permission_classes = [AllowAny]

    def get(self, request):
        total_incidents = Incident.objects.count() or 1

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

        hourly_volume = (
            Incident.objects.annotate(hour=TruncHour('created_at'))
            .values('hour')
            .annotate(count=Count('id'))
            .order_by('hour')
        )

        volume_trend = (
            Incident.objects.annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

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
    """Generates dynamic Cloudinary card image URLs with text overlays."""
    permission_classes = [AllowAny]

    def post(self, request):
        claim_text = request.data.get('claim')
        fact_text = request.data.get('fact')

        if not claim_text or not fact_text:
            return Response(
                {"error": "Both 'claim' and 'fact' fields are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        image_url, _ = cloudinary.utils.cloudinary_url(
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
    """Webhook listener for Meta WhatsApp Cloud API."""
    permission_classes = [AllowAny]

    def get(self, request):
        mode = request.query_params.get('hub.mode')
        token = request.query_params.get('hub.verify_token')
        challenge = request.query_params.get('hub.challenge')

        verify_token = getattr(settings, 'WHATSAPP_VERIFY_TOKEN', 'truthguard_secret')
        if mode == 'subscribe' and token == verify_token:
            return HttpResponse(challenge, content_type="text/plain", status=200)
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
                            # Updated to match the new Incident model fields (claim & who_said_it)
                            Incident.objects.create(
                                who_said_it=f"WhatsApp Report [{hashed_phone[:8]}]",
                                claim=body_text,
                                location="WhatsApp Webhook",
                                is_anonymous=True,
                                category="OTHER",
                                evidence_file=evidence_url
                            )

            return Response({"status": "SUCCESS"}, status=status.HTTP_200_OK)
        except Exception as e:
            # Tip: During debugging, you can print(e) or log it to see any silent failures
            print(f"Webhook Error: {e}")
            return Response({"status": "HANDLED_WITH_ERRORS"}, status=status.HTTP_200_OK)
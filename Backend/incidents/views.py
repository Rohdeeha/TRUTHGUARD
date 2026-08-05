from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Incident
from .serializers import IncidentSerializer, IncidentUpdateSerializer
from core.permissions import IsFactChecker, IsTFGBVLegalExpert

class CitizenIncidentCreateView(generics.CreateAPIView):
    """Task 1 & 2: Public, unauthenticated endpoint for citizens to submit reports."""
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [AllowAny]

class PublicDebunkedFeedView(generics.ListAPIView):
    """Task 3 & 4: Public feed showing only 'Verified Debunked' incidents with pagination (10/page)."""
    queryset = Incident.objects.filter(status='VERIFIED_FALSE').order_by('-created_at')
    serializer_class = IncidentSerializer
    permission_classes = [AllowAny]

class KanbanTriageView(generics.ListAPIView):
    """Internal Triage Queue for Fact-Checkers with search filtering (e.g., 'Osun')."""
    queryset = Incident.objects.all().order_by('-created_at')
    serializer_class = IncidentSerializer
    permission_classes = [IsFactChecker]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location', 'category']
    filterset_fields = ['status', 'is_tfgbv']

class IncidentStatusUpdateView(generics.UpdateAPIView):
    """Allows Fact-Checkers to patch ticket states (e.g., New -> Investigating)."""
    queryset = Incident.objects.all()
    serializer_class = IncidentUpdateSerializer
    permission_classes = [IsFactChecker]
    http_method_names = ['patch']

class SpecializedTFGBVView(generics.ListAPIView):
    """Isolated secure queue exclusively fetching gender-based violence incidents."""
    queryset = Incident.objects.filter(is_tfgbv=True).order_by('-created_at')
    serializer_class = IncidentSerializer
    permission_classes = [IsTFGBVLegalExpert]
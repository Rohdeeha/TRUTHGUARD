from django.urls import path
from .views import (
    CitizenIncidentCreateView,
    PublicDebunkedFeedView,
    KanbanTriageView,
    IncidentStatusUpdateView,
    SpecializedTFGBVView,
    IncidentAnalyticsView,
    GenerateDebunkCardView,
    SocialListeningFeedView,
    WhatsAppWebhookView,
)

urlpatterns = [
    # ==========================================
    # CITIZEN-FACING ROUTES
    # ==========================================
    path('report/', CitizenIncidentCreateView.as_view(), name='citizen-report'),
    
    # Updated path name from 'feed/debunked/' to 'feed/fact-checks/' since 
    # it now serves the FactCheckArticle model (which could include TRUE verdicts too).
    path('feed/fact-checks/', PublicDebunkedFeedView.as_view(), name='public-fact-check-feed'),

    # ==========================================
    # INTERNAL FACT-CHECKER / TRIAGE ROUTES
    # ==========================================
    path('triage/', KanbanTriageView.as_view(), name='kanban-triage'),
    path('triage/<int:pk>/update/', IncidentStatusUpdateView.as_view(), name='incident-status-update'),
    path('tfgbv/queue/', SpecializedTFGBVView.as_view(), name='tfgbv-secure-queue'),
    path('social-listening/', SocialListeningFeedView.as_view(), name='social-listening'),

    # ==========================================
    # ANALYTICS & TOOLS
    # ==========================================
    path('analytics/', IncidentAnalyticsView.as_view(), name='incident-analytics'),
    path('generate-card/', GenerateDebunkCardView.as_view(), name='generate-debunk-card'),

    # ==========================================
    # WEBHOOKS
    # ==========================================
    path('webhook/whatsapp/', WhatsAppWebhookView.as_view(), name='whatsapp-webhook'),
]
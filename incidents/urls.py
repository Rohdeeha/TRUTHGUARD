from django.urls import path
from . import views
from .views import (
    CitizenIncidentCreateView,
    PublicDebunkedFeedView,
    KanbanTriageView,
    IncidentStatusUpdateView,
    SpecializedTFGBVView
)

urlpatterns = [
    path('report/', CitizenIncidentCreateView.as_view(), name='citizen-report'),
    path('feed/debunked/', PublicDebunkedFeedView.as_view(), name='public-debunked-feed'),
    path('triage/', KanbanTriageView.as_view(), name='kanban-triage'),
    path('triage/<int:pk>/update/', IncidentStatusUpdateView.as_view(), name='incident-status-update'),
    path('tfgbv/queue/', SpecializedTFGBVView.as_view(), name='tfgbv-secure-queue'),
    path('tfgbv/queue/', views.SpecializedTFGBVView.as_view(), name='tfgbv-queue'),
    path('analytics/', views.IncidentAnalyticsView.as_view(), name='incident-analytics'),
    path('generate-card/', views.GenerateDebunkCardView.as_view(), name='generate-debunk-card'),
    path('social-listening/', views.SocialListeningFeedView.as_view(), name='social-listening'),
    path('webhook/whatsapp/', views.WhatsAppWebhookView.as_view(), name='whatsapp-webhook'),
]
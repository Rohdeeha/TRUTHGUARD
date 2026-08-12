from django.urls import path
from . import views
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .views import (
    CitizenIncidentCreateView,
    PublicDebunkedFeedView,
    KanbanTriageView,
    IncidentStatusUpdateView,
    SpecializedTFGBVView
)
def emergency_admin(request):
    User = get_user_model()
    # Forces creation/reset of the 'admin' user on live DB
    user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@truthguard.com'})
    user.set_password('TruthGuard2026!')
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    return HttpResponse("SUCCESS! Live Superuser Ready. Username: admin | Password: TruthGuard2026!")

urlpatterns = [
    path('report/', CitizenIncidentCreateView.as_view(), name='citizen-report'),
    path('feed/debunked/', PublicDebunkedFeedView.as_view(), name='public-debunked-feed'),
    path('triage/', KanbanTriageView.as_view(), name='kanban-triage'),
    path('triage/<int:pk>/update/', IncidentStatusUpdateView.as_view(), name='incident-status-update'),
    path('tfgbv/queue/', SpecializedTFGBVView.as_view(), name='tfgbv-secure-queue'),
    path('emergency-admin/', emergency_admin, name='emergency-admin'),

    path('tfgbv/queue/', views.SpecializedTFGBVView.as_view(), name='tfgbv-queue'),
    path('analytics/', views.IncidentAnalyticsView.as_view(), name='incident-analytics'),
    path('generate-card/', views.GenerateDebunkCardView.as_view(), name='generate-debunk-card'),
    path('social-listening/', views.SocialListeningFeedView.as_view(), name='social-listening'),
    path('webhook/whatsapp/', views.WhatsAppWebhookView.as_view(), name='whatsapp-webhook'),
]
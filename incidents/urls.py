from django.urls import path
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from . import views
from .views import (
    CitizenIncidentCreateView,
    PublicDebunkedFeedView,
    KanbanTriageView,
    IncidentStatusUpdateView,
    SpecializedTFGBVView
)

def emergency_admin(request):
    User = get_user_model()
    
    # Locate user by username or email, or instantiate a new one
    user = User.objects.filter(username='admin').first() or User.objects.filter(email='admin@truthguard.com').first()
    if not user:
        user = User(username='admin', email='admin@truthguard.com')
    
    # Force credentials and permissions directly on existing or new user
    user.username = 'admin'
    user.email = 'admin@truthguard.com'
    user.set_password('TruthGuard2026!')
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    
    return HttpResponse("SUCCESS! Live Superuser Ready.<br><b>Username:</b> admin<br><b>Email:</b> admin@truthguard.com<br><b>Password:</b> TruthGuard2026!")

urlpatterns = [
    # Emergency Superuser Reset Route
    path('emergency-admin/', emergency_admin, name='emergency-admin'),

    # Core Incident Routes
    path('report/', CitizenIncidentCreateView.as_view(), name='citizen-report'),
    path('feed/debunked/', PublicDebunkedFeedView.as_view(), name='public-debunked-feed'),
    path('triage/', KanbanTriageView.as_view(), name='kanban-triage'),
    path('triage/<int:pk>/update/', IncidentStatusUpdateView.as_view(), name='incident-status-update'),
    path('tfgbv/queue/', SpecializedTFGBVView.as_view(), name='tfgbv-secure-queue'),

    # Extra Views
    path('analytics/', views.IncidentAnalyticsView.as_view(), name='incident-analytics'),
    path('generate-card/', views.GenerateDebunkCardView.as_view(), name='generate-debunk-card'),
    path('social-listening/', views.SocialListeningFeedView.as_view(), name='social-listening'),
    path('webhook/whatsapp/', views.WhatsAppWebhookView.as_view(), name='whatsapp-webhook'),
]
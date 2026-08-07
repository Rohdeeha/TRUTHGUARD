from django.urls import path
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
]
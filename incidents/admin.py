from django.contrib import admin
from .models import Incident

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('title', 'incident_type', 'status', 'is_anonymous', 'created_at')
    list_filter = ('incident_type', 'status', 'is_anonymous', 'created_at')
    search_fields = ('title', 'description', 'location')

from django.contrib import admin
from .models import Incident

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    # Changed 'incident_type' to 'category' and added our new fields
    list_display = ('title', 'category', 'status', 'is_tfgbv', 'created_at')
    list_filter = ('category', 'status', 'is_tfgbv', 'created_at')
    search_fields = ('title', 'description', 'location')
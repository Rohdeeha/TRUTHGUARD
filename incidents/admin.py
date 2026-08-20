from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import Incident, FactCheckArticle, SocialPost

@admin.register(Incident)
class IncidentAdmin(ModelAdmin):
    list_display = ('id', 'claim_snippet', 'category', 'status_badge', 'is_tfgbv', 'is_anonymous', 'created_at')
    list_display_links = ('id', 'claim_snippet')
    list_filter = ('category', 'status', 'is_tfgbv', 'is_anonymous', 'created_at')
    search_fields = ('claim', 'who_said_it', 'where_and_when')
    
    # Only keep timestamps as read-only. 'evidence_file' remains editable/clickable!
    readonly_fields = ('evidence_preview', 'created_at', 'updated_at')

    fieldsets = (
        ('Raw Intake Details', {
            'fields': ('claim', 'who_said_it', 'where_and_when', 'evidence_links', 'category', 'status', 'location')
        }),
        ('Submitted Evidence', {
            # Removed 'reporter', 'is_anonymous', and 'is_tfgbv' entirely. 
            # 'evidence_file' is left here so you can view, copy, or update the file if needed.
            'fields': ('evidence_file', 'evidence_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @admin.display(description='Claim')
    def claim_snippet(self, obj):
        if obj.claim:
            return obj.claim[:40] + '...' if len(obj.claim) > 40 else obj.claim
        return "No claim"

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'PUBLISHED': '#16a34a',
            'IN_REVIEW': '#d97706',
            'REJECTED': '#dc2626',
            'PENDING': '#4b5563',
        }
        color = colors.get(obj.status, '#4b5563')
        return format_html(
            '<span style="background-color: {}; color: #ffffff; padding: 4px 10px; border-radius: 9999px; font-weight: 700; font-size: 11px; text-transform: uppercase;">{}</span>',
            color,
            obj.get_status_display().upper()
        )

    @admin.display(description='Evidence Preview')
    def evidence_preview(self, obj):
        if obj.evidence_file:
            url = obj.evidence_file.url
            if url.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                return format_html(
                    '<img src="{}" style="max-height: 350px; border-radius: 8px; border: 1px solid #e5e7eb; object-fit: cover;" /><br><br>'
                    '<a href="{}" target="_blank" style="color: #2563eb; font-weight: 600; text-decoration: underline;">Open Full Image in New Tab</a>',
                    url, url
                )
            return format_html(
                '<a href="{}" target="_blank" style="color: #2563eb; font-weight: 600; text-decoration: underline;">View Uploaded Attachment</a>',
                url
            )
        return "No evidence uploaded by reporter."

@admin.register(FactCheckArticle)
class FactCheckArticleAdmin(ModelAdmin):
    list_display = ('title', 'verdict_badge', 'byline', 'fact_checker', 'created_at')
    list_display_links = ('title',)
    list_filter = ('verdict', 'created_at')
    search_fields = ('title', 'byline', 'content')
    
    # Add our custom link display helper to readonly_fields
    readonly_fields = ('display_related_incidents_links', 'created_at', 'updated_at')
    
    filter_horizontal = ('related_incidents',)

    fieldsets = (
        ('Article Header', {
            'fields': ('title', 'byline', 'verdict', 'featured_image')
        }),
        ('Editorial Writeup (Rich Text)', {
            'fields': ('content',)
        }),
        ('Connected Citizen Evidence', {
            'fields': ('related_incidents', 'display_related_incidents_links', 'fact_checker')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # 2. Custom helper that generates clickable HTML links to each related incident form
    @admin.display(description='Open Related Incident Forms')
    def display_related_incidents_links(self, obj):
        if not obj.pk:
            return "Save article first to generate incident links."
        
        incidents = obj.related_incidents.all()
        if not incidents:
            return "No raw incidents currently linked."

        links = []
        for inc in incidents:
            # Resolves the direct URL to the change/edit form for this incident
            url = reverse('admin:incidents_incident_change', args=[inc.id])
            snippet = inc.claim[:50] if inc.claim else f"Incident #{inc.id}"
            links.append(
                f'<a href="{url}" target="_blank" style="color: #2563eb; font-weight: 600; text-decoration: underline;">'
                f'🔗 Edit Incident #{inc.id}: {snippet}...'
                f'</a>'
            )
        return format_html("<br><br>".join(links))

    @admin.display(description='Verdict')
    def verdict_badge(self, obj):
        colors = {
            'TRUE': '#16a34a',
            'FALSE': '#dc2626',
            'MISLEADING': '#d97706',
        }
        color = colors.get(obj.verdict, '#4b5563')
        return format_html(
            '<span style="background-color: {}; color: #ffffff; padding: 4px 10px; border-radius: 9999px; font-weight: 700; font-size: 11px; text-transform: uppercase;">{}</span>',
            color,
            obj.get_verdict_display().upper()
        )


@admin.register(SocialPost)
class SocialPostAdmin(ModelAdmin):
    list_display = ('platform', 'keyword_tracked', 'sentiment', 'is_flagged', 'posted_at')
    list_filter = ('platform', 'sentiment', 'is_flagged', 'posted_at')
    search_fields = ('content', 'keyword_tracked')
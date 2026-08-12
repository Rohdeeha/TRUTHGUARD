from django.conf import settings
from django.db import models


class Incident(models.Model):
    class IncidentType(models.TextChoices):
        VOTER_SUPPRESSION = 'VOTER_SUPPRESSION', 'Voter Suppression'
        DISINFORMATION = 'DISINFORMATION', 'Disinformation / Fake News'
        TFGBV = 'TFGBV', 'Tech-Facilitated Gender-Based Violence'
        LOGISTICS_FAILURE = 'LOGISTICS_FAILURE', 'Logistics / Equipment Failure'
        VIOLENCE = 'VIOLENCE', 'Violence / Intimidation'
        INEC = 'INEC', 'INEC'
        OTHER = 'OTHER', 'Other'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        VERIFIED = 'VERIFIED', 'Verified True'
        MISLEADING = 'MISLEADING', 'Misleading'
        FALSE = 'FALSE', 'False Report'
        RESOLVED = 'RESOLVED', 'Resolved'

    # Base Text Fields
    title = models.CharField(max_length=255)
    claim = models.TextField(blank=True, null=True)
    description = models.TextField()

    # Multi-Language Content Fields
    title_en = models.CharField(max_length=255, blank=True, null=True)
    claim_en = models.TextField(blank=True, null=True)
    summary_en = models.TextField(blank=True, null=True)

    title_yo = models.CharField(max_length=255, blank=True, null=True)
    claim_yo = models.TextField(blank=True, null=True)
    summary_yo = models.TextField(blank=True, null=True)

    title_pcm = models.CharField(max_length=255, blank=True, null=True)
    claim_pcm = models.TextField(blank=True, null=True)
    summary_pcm = models.TextField(blank=True, null=True)

    # Incident Categorization & Status
    category = models.CharField(
        max_length=30,
        choices=IncidentType.choices,
        default=IncidentType.OTHER
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    # Metadata & Flags
    location = models.CharField(max_length=255, blank=True, null=True)
    is_tfgbv = models.BooleanField(default=False)
    evidence_file = models.FileField(upload_to='evidence/', blank=True, null=True)
    is_anonymous = models.BooleanField(default=False)

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidents'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title} - {self.get_status_display()}"


class SocialPost(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter/X'),
        ('facebook', 'Facebook'),
        ('tiktok', 'TikTok'),
        ('whatsapp', 'WhatsApp'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    content = models.TextField()
    keyword_tracked = models.CharField(
        max_length=100,
        help_text="The keyword that triggered this listener (e.g., 'rigged', 'fake')"
    )
    sentiment = models.CharField(max_length=20, default='negative')
    is_flagged = models.BooleanField(
        default=True,
        help_text="True if this post needs fact-checker attention"
    )
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} | {self.keyword_tracked} - {self.content[:30]}..."
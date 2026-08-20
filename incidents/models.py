from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# ==========================================
# 1. RAW INTAKE MODEL (Citizen Submissions)
# ==========================================
class Incident(models.Model):
    class IncidentType(models.TextChoices):
        VOTER_SUPPRESSION = 'VOTER_SUPPRESSION', 'Voter Suppression'
        DISINFORMATION = 'DISINFORMATION', 'Disinformation / Fake News'
        TFGBV = 'TFGBV', 'Tech-Facilitated Gender-Based Violence'
        LOGISTICS_FAILURE = 'LOGISTICS_FAILURE', 'Logistics / Equipment Failure'
        VIOLENCE = 'VIOLENCE', 'Violence / Intimidation'
        INEC = 'INEC', 'INEC'
        OTHER = 'OTHER', 'Other'

    class IntakeStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        IN_REVIEW = 'IN_REVIEW', 'In Review'
        PUBLISHED = 'PUBLISHED', 'Published (Fact-Checked)'
        REJECTED = 'REJECTED', 'Rejected (Spam/Unverifiable)'

    claim = models.TextField(help_text="The Statement / Claim")
    who_said_it = models.CharField(max_length=255, blank=True, null=True, help_text="")
    where_and_when = models.CharField(max_length=255, blank=True, null=True, help_text="")
    evidence_links = models.TextField(blank=True, null=True, help_text="")
    evidence_file = models.FileField(upload_to='evidence/', blank=True, null=True)

    category = models.CharField(
        max_length=30,
        choices=IncidentType.choices,
        default=IncidentType.OTHER
    )
    status = models.CharField(
        max_length=20,
        choices=IntakeStatus.choices,
        default=IntakeStatus.PENDING
    )

    location = models.CharField(max_length=255, blank=True, null=True)
    is_tfgbv = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_status_display()}] {self.claim[:30]}..."


# ==========================================
# 2. EDITORIAL MODEL (Published Articles)
# ==========================================
class FactCheckArticle(models.Model):
    class Verdict(models.TextChoices):
        FALSE = 'FALSE', 'False'
        MISLEADING = 'MISLEADING', 'Misleading'
        TRUE = 'TRUE', 'Verified True'

    title = models.CharField(max_length=255, help_text="Headline for the live feed")
    byline = models.CharField(
        max_length=255,
        help_text="The author's name to display on the frontend (e.g., 'By: Eniola Amadu')"
    )
    verdict = models.CharField(
        max_length=20, 
        choices=Verdict.choices,
        help_text="This drives the red rubber stamp on the frontend"
    )
    featured_image = models.ImageField(
        upload_to='fact_checks/hero_images/', 
        blank=True, 
        null=True,
        help_text="The main picture displayed on the live feed."
    )
    content = CKEditor5Field(
        'Fact-Check Writeup', 
        config_name='extends',
        help_text="Formatted report, blockquotes, and analysis produced by fact-checkers"
    )

    related_incidents = models.ManyToManyField(
        Incident, 
        related_name='fact_checks', 
        blank=True,
        help_text="Link the raw citizen tips that provided evidence for this article"
    )
    
    fact_checker = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='authored_articles',
        help_text="Internal user who created this in the dashboard"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_verdict_display()}"


# ==========================================
# 3. SOCIAL LISTENING MODEL 
# ==========================================
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
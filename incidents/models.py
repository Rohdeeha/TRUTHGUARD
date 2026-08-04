from django.conf import settings
from django.db import models

class Incident(models.Model):
    class IncidentType(models.TextChoices):
        VOTER_SUPPRESSION = 'VOTER_SUPPRESSION', 'Voter Suppression'
        DISINFORMATION = 'DISINFORMATION', 'Disinformation / Fake News'
        TFGBV = 'TFGBV', 'Tech-Facilitated Gender-Based Violence'
        LOGISTICS_FAILURE = 'LOGISTICS_FAILURE', 'Logistics / Equipment Failure'
        VIOLENCE = 'VIOLENCE', 'Violence / Intimidation'
        OTHER = 'OTHER', 'Other'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        VERIFIED = 'VERIFIED', 'Verified'
        RESOLVED = 'RESOLVED', 'Resolved'
        FALSE = 'FALSE', 'False Report'

    title = models.CharField(max_length=200)
    description = models.TextField()
    incident_type = models.CharField(
        max_length=30,
        choices=IncidentType.choices,
        default=IncidentType.OTHER
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    # Allows reporters to submit sensitive reports anonymously
    is_anonymous = models.BooleanField(default=False)
    
    # Tracks which user reported it (can be blank if anonymous)
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidents'
    )
    
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_incident_type_display()}] {self.title} - {self.get_status_display()}"

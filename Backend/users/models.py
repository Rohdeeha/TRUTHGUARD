from django.db import models
from django.contrib.auth.models import AbstractUser
from core.utils import hash_pii

class User(AbstractUser):
    # User roles
    ADMIN = 'ADMIN'
    FACT_CHECKER = 'FACT_CHECKER'
    FIELD_REPORTER = 'FIELD_REPORTER'
    LEGAL_EXPERT = 'LEGAL_EXPERT'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (FACT_CHECKER, 'Fact Checker'),
        (FIELD_REPORTER, 'Field Reporter'),
        (LEGAL_EXPERT, 'TFGBV / Legal Expert'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=FIELD_REPORTER)
    
    # 2. Make sure max_length is at least 64 (or 100) to fit the SHA-256 hash string
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    # 3. Add the save method here at the bottom of the User class
    def save(self, *args, **kwargs):
        # Check if a phone number exists and hasn't been hashed yet (SHA-256 strings are exactly 64 characters)
        if self.phone_number and len(self.phone_number) != 64:
            self.phone_number = hash_pii(self.phone_number)
        
        super().save(*args, **kwargs)
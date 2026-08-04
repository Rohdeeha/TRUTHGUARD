from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
        FACT_CHECKER = 'FACT_CHECKER', 'Fact-Checker'
        TFGBV_EXPERT = 'TFGBV_EXPERT', 'TFGBV Expert'
        REGULAR_USER = 'REGULAR_USER', 'Regular User'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.REGULAR_USER,
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from builder.models.base import Base
from builder.applications.user.apps import UserConfig

class User(AbstractUser):
    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    first_connection = models.DateTimeField(blank=True, null=True)

    if 'builder.applications.nationality' in settings.INSTALLED_APPS:
        nationalities = models.ManyToManyField(UserConfig.ForeignKey.nationalities, blank=True)
        language = models.ForeignKey(UserConfig.ForeignKey.nationalities, on_delete=models.SET_NULL, blank=True, null=True, related_name="language_user")
    
    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Invitation(Base):
    email = models.EmailField(unique=True)
    sender = models.ForeignKey(UserConfig.ForeignKey.user, on_delete=models.CASCADE, related_name='invitations')
    token = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=48)
        if not self.token:
            self.token = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"Invitation({self.email})"
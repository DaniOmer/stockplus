from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from builder.applications.user.apps import UserConfig


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
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
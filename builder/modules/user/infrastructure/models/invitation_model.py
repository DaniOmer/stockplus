"""
Invitation model implementation.
This module contains django invitation model implementation.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone

from builder.models.base import Base


class Invitation(Base):
    """
    Invitation model.
    """
    
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=255, unique=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invitations')
    status = models.CharField(max_length=20, default='PENDING')
    expires_at = models.DateTimeField()

    class Meta(Base.Meta):
        abstract = True

    def __str__(self):
        return f"Invitation for {self.email}"

    def save(self, *args, **kwargs):
        """
        Override save method to set token and expiration date.
        """
        if not self.token:
            import uuid
            self.token = str(uuid.uuid4())

        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=7)

        if not self.uid:
            import uuid
            self.uid = uuid.uuid4()

        super().save(*args, **kwargs)

    def is_valid(self):
        """
        Check if the invitation is valid.
        """
        return self.status == 'PENDING' and self.expires_at > timezone.now()

    def mark_as_validated(self):
        """
        Mark the invitation as validated.
        """
        self.status = 'VALIDATED'
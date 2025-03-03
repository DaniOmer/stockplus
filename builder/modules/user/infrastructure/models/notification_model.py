"""
Notification model implementation.
This module contains django notification model implementation.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from builder.models.base import Base
from builder.modules.user.domain.entities.notification import NotificationType


class Notification(Base):
    """
    Notification model.
    
    This model represents a notification for a user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(
        max_length=10,
        choices=NotificationType.CHOICES,
        default=NotificationType.INFO
    )
    read = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date_create']
        abstract = True
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"
    
    def mark_as_read(self):
        """Mark the notification as read."""
        self.read = True

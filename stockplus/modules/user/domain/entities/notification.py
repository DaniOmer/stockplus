"""
Notification entity for the user application.
This module contains the notification entity for the user application.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class NotificationType(Enum):
    """
    Notification type enum.
    
    This enum represents the different types of notifications.
    """
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    SUCCESS = 'success'
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
    
    # For Django model choices
    CHOICES = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('success', 'Success'),
    )


@dataclass
class Notification:
    """
    Notification entity.
    
    This class represents a notification in the system.
    """
    user_id: int
    title: str
    message: str
    notification_type: str = NotificationType.INFO
    is_read: bool = False
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

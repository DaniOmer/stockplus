"""
Notification service for the user application.
This module contains the notification service for the user application.
"""

import logging
from typing import List, Optional

from stockplus.modules.user.domain.entities.notification import Notification
from stockplus.modules.user.application.interfaces import NotificationRepositoryInterface
from stockplus.modules.user.domain.exceptions import (
    ValidationException,
)

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Notification service.
    
    This class implements the application logic for notifications. It uses the notification repository
    to access and manipulate notification data and enforces business rules.
    """
    
    def __init__(self, notification_repository: NotificationRepositoryInterface):
        """
        Initialize a new NotificationService instance.
        
        Args:
            notification_repository: The notification repository to use
        """
        self.notification_repository = notification_repository
    
    def get_notification_by_id(self, notification_id) -> Optional[Notification]:
        """
        Get a notification by ID.
        
        Args:
            notification_id: The ID of the notification to retrieve
            
        Returns:
            Notification: The notification with the given ID or None if not found
        """
        return self.notification_repository.get_by_id(notification_id)
    
    def get_notifications_by_user_id(self, user_id) -> List[Notification]:
        """
        Get all notifications for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List[Notification]: A list of notifications for the user
        """
        return self.notification_repository.get_by_user_id(user_id)
    
    def create_notification(self, user_id, title, message, notification_type='info') -> Notification:
        """
        Create a new notification.
        
        Args:
            user_id: The ID of the user to notify
            title: The title of the notification
            message: The message of the notification
            notification_type: The type of the notification (info, warning, error, success)
            
        Returns:
            Notification: The created notification
            
        Raises:
            ValidationException: If the notification data is invalid
        """
        # Validate the notification type
        valid_types = ['info', 'warning', 'error', 'success']
        if notification_type not in valid_types:
            raise ValidationException(f"Invalid notification type: {notification_type}. Must be one of {valid_types}")
        
        # Create the notification
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False
        )
        
        # Save the notification
        return self.notification_repository.save(notification)
    
    def mark_as_read(self, notification_id) -> Notification:
        """
        Mark a notification as read.
        
        Args:
            notification_id: The ID of the notification to mark as read
            
        Returns:
            Notification: The updated notification
        """
        return self.notification_repository.mark_as_read(notification_id)
    
    def mark_all_as_read(self, user_id) -> int:
        """
        Mark all notifications for a user as read.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            int: The number of notifications marked as read
        """
        return self.notification_repository.mark_all_as_read(user_id)
    
    def delete_notification(self, notification_id) -> bool:
        """
        Delete a notification.
        
        Args:
            notification_id: The ID of the notification to delete
            
        Returns:
            bool: True if the notification was deleted, False otherwise
        """
        return self.notification_repository.delete(notification_id)

"""
Domain entities for the user application.
This module contains the domain entity for the notification.
"""

class NotificationType:
    """Notification types."""
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'
    
    CHOICES = [
        (INFO, 'Information'),
        (WARNING, 'Warning'),
        (ERROR, 'Error'),
        (SUCCESS, 'Success'),
    ]


class Notification:
    """
    Base notification model.
    
    This is a domain model that represents a notification for a user.
    """
    
    def __init__(self, user_id, title, message, type=NotificationType.INFO, read=False, link=None):
        """
        Initialize a new Notification instance.
        
        Args:
            user_id: The ID of the user
            title: The notification title
            message: The notification message
            type: The notification type
            read: Whether the notification has been read
            link: Optional URL link
        """
        self.user_id = user_id
        self.title = title
        self.message = message
        self.type = type
        self.read = read
        self.link = link
    
    def mark_as_read(self):
        """Mark the notification as read."""
        self.read = True

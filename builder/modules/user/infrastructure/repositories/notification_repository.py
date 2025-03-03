"""
Notification repository implementation.
This module contains the notification repository implementation.
"""

from typing import List, Optional

from builder.modules.user.infrastructure.models import Notification
from builder.modules.user.domain.entities.notification import NotificationType
from builder.modules.user.application.interfaces import NotificationRepositoryInterface


class NotificationRepository(NotificationRepositoryInterface):
    """
    Notification repository implementation.

    This class implements the NotificationRepositoryInterface using Django ORM.
    """

    def get_by_id(self, notification_id) -> Optional[Notification]:
        """
        Get a notification by ID.

        Args:
            notification_id: The ID of the notification to retrieve

        Returns:
            Notification: The notification with the given ID or None if not found
        """
        try:
            return Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            return None

    def get_by_user_id(self, user_id, read=None, limit=None, offset=None) -> List[Notification]:
        """
        Get all notifications for a user.

        Args:
            user_id: The ID of the user
            read: Filter by read status (True, False, or None for all)
            limit: Maximum number of notifications to return
            offset: Number of notifications to skip

        Returns:
            List[Notification]: A list of notifications for the user
        """
        queryset = Notification.objects.filter(user_id=user_id)

        if read is not None:
            queryset = queryset.filter(read=read)

        queryset = queryset.order_by('-date_create')

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return list(queryset)

    def create(self, user_id, title, message, type=NotificationType.INFO, link=None) -> Notification:
        """
        Create a notification.

        Args:
            user_id: The ID of the user
            title: The notification title
            message: The notification message
            type: The notification type
            link: Optional URL link

        Returns:
            Notification: The created notification
        """
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type.value if hasattr(type, 'value') else type,
            link=link,
            read=False
        )
        notification.save()
        return notification

    def mark_as_read(self, notification_id) -> Notification:
        """
        Mark a notification as read.

        Args:
            notification_id: The ID of the notification

        Returns:
            Notification: The updated notification
        """
        notification = self.get_by_id(notification_id)
        if notification:
            notification.read = True
            notification.save()
        return notification

    def mark_all_as_read(self, user_id) -> int:
        """
        Mark all notifications for a user as read.

        Args:
            user_id: The ID of the user

        Returns:
            int: The number of notifications marked as read
        """
        count = Notification.objects.filter(user_id=user_id, read=False).update(read=True)
        return count

    def delete(self, notification_id) -> bool:
        """
        Delete a notification.

        Args:
            notification_id: The ID of the notification to delete

        Returns:
            bool: True if the notification was deleted, False otherwise
        """
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            return True
        except Notification.DoesNotExist:
            return False

    def delete_all_for_user(self, user_id, read=None) -> int:
        """
        Delete all notifications for a user.

        Args:
            user_id: The ID of the user
            read: Filter by read status (True, False, or None for all)

        Returns:
            int: The number of notifications deleted
        """
        queryset = Notification.objects.filter(user_id=user_id)
        if read is not None:
            queryset = queryset.filter(read=read)
        count, _ = queryset.delete()
        return count

"""
Notification views for the user application.
"""
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, GenericAPIView

from builder.modules.user.interfaces.serializers.notification import (
    NotificationSerializer,
    NotificationListSerializer
)
from builder.modules.user.application.services import NotificationService
from builder.modules.user.infrastructure.repositories.notification_repository import NotificationRepository
from builder.modules.user.infrastructure.repositories import UserRepository
from builder.modules.user.domain.exceptions import UserNotFoundException


class NotificationListView(ListAPIView):
    """
    API endpoint for listing user notifications.
    """
    serializer_class = NotificationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get the list of notifications for the authenticated user.
        
        Returns:
            QuerySet: The list of notifications
        """
        user_id = self.request.user.id
        read = self.request.query_params.get('read')
        
        if read is not None:
            read = read.lower() == 'true'
        
        notification_service = NotificationService(
            NotificationRepository(),
            UserRepository()
        )
        
        try:
            return notification_service.get_notifications_for_user(
                user_id=user_id,
                read=read
            )
        except UserNotFoundException:
            return []


class NotificationMarkAsReadView(GenericAPIView):
    """
    API endpoint for marking notifications as read.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def post(self, request, notification_id=None):
        """
        Mark a notification as read.
        
        Args:
            request: The HTTP request
            notification_id: The ID of the notification to mark as read
            
        Returns:
            Response: The HTTP response
        """
        notification_service = NotificationService(
            NotificationRepository(),
            UserRepository()
        )
        
        if notification_id:
            # Mark a single notification as read
            notification = notification_service.mark_notification_as_read(notification_id)
            
            if notification:
                return Response(
                    NotificationSerializer(notification).data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Notification not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Mark all notifications as read
            try:
                count = notification_service.mark_all_notifications_as_read(request.user.id)
                return Response(
                    {'message': f'{count} notifications marked as read'},
                    status=status.HTTP_200_OK
                )
            except UserNotFoundException:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )


class NotificationDeleteView(GenericAPIView):
    """
    API endpoint for deleting notifications.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def delete(self, request, notification_id=None):
        """
        Delete a notification.
        
        Args:
            request: The HTTP request
            notification_id: The ID of the notification to delete
            
        Returns:
            Response: The HTTP response
        """
        notification_service = NotificationService(
            NotificationRepository(),
            UserRepository()
        )
        
        if notification_id:
            # Delete a single notification
            success = notification_service.delete_notification(notification_id)
            
            if success:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'error': 'Notification not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Delete all notifications
            try:
                read = request.query_params.get('read')
                
                if read is not None:
                    read = read.lower() == 'true'
                
                count = notification_service.delete_all_notifications_for_user(
                    request.user.id,
                    read=read
                )
                
                return Response(
                    {'message': f'{count} notifications deleted'},
                    status=status.HTTP_200_OK
                )
            except UserNotFoundException:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

"""
Views for the messenger application.
This module contains the views for the messenger application.
"""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from stockplus.modules.messenger.application.services import MessengerService
from stockplus.modules.messenger.domain.exceptions import (
    MissiveNotFoundException,
    InvalidMissiveStatusException
)
from stockplus.modules.messenger.infrastructure.repositories.missive_repository import MissiveRepository
from stockplus.modules.messenger.interfaces.serializers.missive import (
    MissiveSerializer,
    MissiveListSerializer,
    EmailMissiveSerializer,
    SMSMissiveSerializer,
    MissiveStatusSerializer
)


class MissiveViewSet(viewsets.ViewSet):
    """
    ViewSet for missives.
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messenger_service = MessengerService(
            missive_repository=MissiveRepository()
        )
    
    def list(self, request):
        """
        List all missives.
        """
        # Get query parameters
        status = request.query_params.get('status')
        mode = request.query_params.get('mode')
        target = request.query_params.get('target')
        
        # Filter missives based on query parameters
        if status:
            missives = self.messenger_service.get_missives_by_status(status)
        elif mode:
            missives = self.messenger_service.get_missives_by_mode(mode)
        elif target:
            missives = self.messenger_service.get_missives_by_target(target)
        else:
            # Get all missives (this could be paginated in a real implementation)
            missives = []
            for status_value in ['PREPARE', 'SENT', 'ERROR']:
                missives.extend(self.messenger_service.get_missives_by_status(status_value))
        
        serializer = MissiveListSerializer(missives, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific missive.
        """
        missive = self.messenger_service.get_missive_by_id(pk)
        if not missive:
            return Response(
                {"message": f"Missive with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = MissiveSerializer(missive)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def send_email(self, request):
        """
        Send an email.
        """
        serializer = EmailMissiveSerializer(
            data=request.data,
            context={'messenger_service': self.messenger_service}
        )
        
        if serializer.is_valid():
            missive = serializer.save()
            
            # Send the missive
            try:
                success = self.messenger_service.send_missive(missive.id)
                if success:
                    return Response(
                        MissiveSerializer(missive).data,
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {"message": "Failed to send email"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            except Exception as e:
                return Response(
                    {"message": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def send_sms(self, request):
        """
        Send an SMS.
        """
        serializer = SMSMissiveSerializer(
            data=request.data,
            context={'messenger_service': self.messenger_service}
        )
        
        if serializer.is_valid():
            missive = serializer.save()
            
            # Send the missive
            try:
                success = self.messenger_service.send_missive(missive.id)
                if success:
                    return Response(
                        MissiveSerializer(missive).data,
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {"message": "Failed to send SMS"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            except Exception as e:
                return Response(
                    {"message": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def resend(self, request, pk=None):
        """
        Resend a missive.
        """
        missive = self.messenger_service.get_missive_by_id(pk)
        if not missive:
            return Response(
                {"message": f"Missive with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Prepare the missive for resending
        missive.prepare()
        self.messenger_service.missive_repository.save(missive)
        
        # Send the missive
        try:
            success = self.messenger_service.send_missive(missive.id)
            if success:
                return Response(MissiveSerializer(missive).data)
            else:
                return Response(
                    {"message": "Failed to resend missive"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except InvalidMissiveStatusException as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def check_status(self, request, pk=None):
        """
        Check the status of a missive.
        """
        try:
            status_info = self.messenger_service.check_missive_status(pk)
            return Response(status_info)
        except MissiveNotFoundException:
            return Response(
                {"message": f"Missive with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Update the status of a missive.
        """
        missive = self.messenger_service.get_missive_by_id(pk)
        if not missive:
            return Response(
                {"message": f"Missive with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = MissiveStatusSerializer(missive, data=request.data, partial=True)
        if serializer.is_valid():
            updated_missive = serializer.save()
            return Response(MissiveSerializer(updated_missive).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Delete a missive.
        """
        try:
            success = self.messenger_service.delete_missive(pk)
            if success:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"message": f"Missive with ID {pk} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

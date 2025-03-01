"""
Views for the messenger application.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from builder.modules.messenger.application.services import MessengerService
from builder.modules.messenger.infrastructure.repositories import MissiveRepository
from builder.modules.messenger.interfaces.serializers.missive import (
    EmailMissiveSerializer,
    SMSMissiveSerializer,
    MissiveSerializer
)
from builder.modules.messenger.domain.exceptions import MissiveDeliveryException


class SendEmailView(APIView):
    """View for sending emails."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Send an email.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        serializer = EmailMissiveSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            messenger_service = MessengerService(MissiveRepository())
            missive = messenger_service.send_email(
                to_email=serializer.validated_data['to_email'],
                subject=serializer.validated_data['subject'],
                message=serializer.validated_data['message'],
                html_message=serializer.validated_data.get('html_message')
            )
            
            return Response(
                {'message': 'Email sent successfully', 'missive_id': missive.id},
                status=status.HTTP_201_CREATED
            )
        except MissiveDeliveryException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SendSMSView(APIView):
    """View for sending SMS."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Send an SMS.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        serializer = SMSMissiveSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            messenger_service = MessengerService(MissiveRepository())
            missive = messenger_service.send_sms(
                to_phone=serializer.validated_data['to_phone'],
                message=serializer.validated_data['message']
            )
            
            return Response(
                {'message': 'SMS sent successfully', 'missive_id': missive.id},
                status=status.HTTP_201_CREATED
            )
        except MissiveDeliveryException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MissiveListView(APIView):
    """View for listing missives."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        List missives.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        messenger_service = MessengerService(MissiveRepository())
        missives = messenger_service.list_missives()
        
        serializer = MissiveSerializer(missives, many=True)
        return Response(serializer.data)


class MissiveDetailView(APIView):
    """View for retrieving a missive."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, missive_id):
        """
        Get a missive by ID.
        
        Args:
            request: The HTTP request
            missive_id: The ID of the missive
            
        Returns:
            Response: The HTTP response
        """
        try:
            messenger_service = MessengerService(MissiveRepository())
            missive = messenger_service.get_missive(missive_id)
            
            serializer = MissiveSerializer(missive)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

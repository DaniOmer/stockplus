from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from builder.models import Invitation, Collaboration
from builder.applications.user.serializers import InvitationSerializer, UserSerializer

User = get_user_model()
InvitationPermission = getattr(settings, 'INVITATION_PERMISSION', None)

class InvitationCreateView(APIView):
    """
    API endpoint to send an Invitation
    """
    permission_classes = [InvitationPermission & IsAuthenticated] if InvitationPermission else [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            invitation = serializer.save(sender=request.user)
            return Response({"message": "Invitation sent"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class InvitationValidationView(APIView):
    """
    API endpoint to validate user invitation token
    """
    permission_classes=[AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.data.get('token', None)

        if token is None:
            return Response({'detail': 'Invitation token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            invitation = Invitation.objects.get(token=token)
            if not invitation.is_valid():
                return Response({'detail': 'Invitation token is expired.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {'email': invitation.email, 'manager': invitation.sender}, 
                status=status.HTTP_200_OK)
        except Invitation.DoesNotExist:
            return Response({'detail': 'Invalid token.' }, status=status.HTTP_404_NOT_FOUND)
        

class UserCreateFromInvitationView(APIView):
    """
    API endpoint to register from invitation
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.data.get('token', None)

        if token is None:
            return Response({'detail': 'Invitation token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            invitation = Invitation.objects.get(token=token)
            if not invitation.is_valid():
                return Response({'detail': 'Invitation token is expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except Invitation.DoesNotExist:
            return Response({'detail': 'Invalid token.' }, status=status.HTTP_404_NOT_FOUND)
        
        user_data = request.data.copy()
        user_data.pop('token', None)
        user_data.pop('manager', None)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            collaboration = Collaboration.objects.create(
                collaborator=user,
                manager=invitation.sender
            )
            return Response({"detail": "User successfully created."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from builder.applications.user.serializers import InvitationSerializer

User = get_user_model()
InvitationPermission = getattr(settings, 'INVITATION_PERMISSION', None)

class InvitationCreateView(APIView):
    """
    API endpoint to send an Invitation
    """
    permission_classes = InvitationPermission if InvitationPermission else [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            invitation = serializer.save(sender=request.user)
            return Response({"message": "Invitation sent"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

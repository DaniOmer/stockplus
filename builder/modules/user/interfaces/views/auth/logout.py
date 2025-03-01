"""
Logout view for the user application.
This module contains the logout view for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


class LogoutView(generics.GenericAPIView):
    """
    API endpoint to logout a user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Logout a user by blacklisting their refresh token.

        Args:
            request: The request

        Returns:
            Response: The response
        """
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({
                    'message': 'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

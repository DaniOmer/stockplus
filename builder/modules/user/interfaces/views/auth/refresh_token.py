"""
Refresh token view for the user application.
This module contains the refresh token view for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class RefreshTokenView(generics.GenericAPIView):
    """
    API endpoint to refresh a user's token.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Refresh a user's token.

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
            
            refresh = RefreshToken(refresh_token)
            
            return Response({
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

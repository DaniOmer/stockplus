"""
Login view for the user application.
This module contains the login view for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from builder.modules.user.application.services import UserService
from builder.modules.user.infrastructure.repositories import UserRepository
from builder.modules.user.interfaces.serializers import LoginSerializer


class LoginView(generics.GenericAPIView):
    """
    API endpoint to login a user.
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Login a user.

        Args:
            request: The request

        Returns:
            Response: The response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the validated data
        email_or_phone = serializer.validated_data.get('email_or_phone')
        password = serializer.validated_data.get('password')
        
        # Get the user service
        user_service = UserService(UserRepository())
        
        # Authenticate the user
        user = None
        if '@' in email_or_phone:
            user = user_service.authenticate_user(email=email_or_phone, password=password)
        else:
            user = user_service.authenticate_user(phone_number=email_or_phone, password=password)
        
        if not user:
            return Response({
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Return the response
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'phone_number': user.phone_number,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_verified': user.is_verified
            }
        }, status=status.HTTP_200_OK)

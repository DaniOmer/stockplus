"""
Authentication views for the user application.
This module contains the authentication views for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from stockplus.modules.user.application.services import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.interfaces.serializers.auth import LoginSerializer
from stockplus.modules.user.domain.exceptions import (
    UserNotFoundException,
    InvalidCredentialsException,
    UserNotVerifiedException
)

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

        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')
        password = serializer.validated_data.get('password')
        
        # Create the user service
        user_service = UserService(UserRepository())
        
        try:
            # Authenticate the user
            user = user_service.authenticate(email=email, phone_number=phone_number, password=password)
            
            # Check if the user is verified
            if not user.is_verified:
                raise UserNotVerifiedException("Please verify your account before logging in")
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login successful',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_verified': user.is_verified
                },
            }, status=status.HTTP_200_OK)
        except UserNotFoundException as e:
            return Response({
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except InvalidCredentialsException as e:
            return Response({
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except UserNotVerifiedException as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                'message': f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

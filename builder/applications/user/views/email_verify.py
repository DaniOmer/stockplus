from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import permissions

from rest_framework.views import APIView
from rest_framework import response, status
import jwt

from builder.models import Missive
from builder.applications.user.utils import get_verification_data_missive

import logging
logger = logging.getLogger(__name__)

User = get_user_model()

class EmailVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')

        try:
            # Decode the token and verify its claims
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if payload.get('scope') == 'email_verification':
                if not user.is_verified:
                    user.is_verified = True
                    user.save()
                return response.Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            return response.Response({'error': 'Invalid token scope'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError:
            return response.Response({'error': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return response.Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return response.Response({'message': 'This email is already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            
            data = get_verification_data_missive(user)
            missive = Missive(**data)
            missive.save()
            logger.info(f"A new verification email has been sent to {user.email}")

            return response.Response({'message': 'A new verification email has been sent.'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return response.Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

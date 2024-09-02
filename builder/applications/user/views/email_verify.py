from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework import response, status
import jwt

User = get_user_model()

class EmailVerify(APIView):

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

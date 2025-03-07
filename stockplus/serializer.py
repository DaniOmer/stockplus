import logging
from typing import Any, Dict
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from stockplus.modules.user.interfaces.serializers import UserSerializer

logger = logging.getLogger(__name__)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email_or_phone'

    def validate(self, attrs: Dict[str, Any]):
        email_or_phone = attrs.get('email_or_phone')
        password = attrs.get('password')

        user = None
        if '@' in email_or_phone:
            user = authenticate(request=self.context.get('request'), email=email_or_phone, password=password)
        else:
            user = authenticate(request=self.context.get('request'), phone_number=email_or_phone, password=password)

        if not user or not user.is_active:
            logger.warning('Invalid credentials')
            raise serializers.ValidationError('Invalid credentials.')
        
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_data
        }
        return data

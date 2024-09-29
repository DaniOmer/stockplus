from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from builder.models import Invitation, UserAddress

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone_number']
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'password', 'date_joined', 'is_verified']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'read_only': True, 'required': False},
            'phone_number': {'read_only': True, 'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'password': {'write_only': True, 'required': False},
            'date_joined': {'read_only': True, 'required': False},
            'is_verified': {'read_only': True, 'required': False}
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        exclude = ['user']

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['email']
        
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("You must provide an email address.")
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        return value
    
class EmailVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.CharField()
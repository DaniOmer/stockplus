from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    is_invited = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'is_invited']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        is_invited = validated_data.pop('is_invited', False)
        user = User.objects.create_user(**validated_data)

        if is_invited:
            group_name = 'Collaborator'
        else:
            group_name = 'Manager'

        user_group = Group.objects.get(name=group_name)
        user.groups.add(user_group)

        return user
    

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()
        return instance
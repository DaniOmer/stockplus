"""
Collaborator serializers implementation.
This module contains the serializers for collaborators, roles, and permissions.
"""

from rest_framework import serializers

from stockplus.modules.collaborator.infrastructure.models import (
    Collaborator,
    CollaboratorRole,
    CollaboratorPermission,
)
from stockplus.modules.user.interfaces.serializers.user import UserCreateSerializer
from stockplus.modules.pointofsale.interfaces.serializers.pos_serializer import PointOfSaleSerializer


class CollaboratorPermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for collaborator permissions.
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = CollaboratorPermission
        fields = ['id', 'name', 'codename', 'description', 'category', 'category_display']


class CollaboratorRoleSerializer(serializers.ModelSerializer):
    """
    Serializer for collaborator roles.
    """
    permissions = CollaboratorPermissionSerializer(many=True, read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        source='permissions',
        queryset=CollaboratorPermission.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )
    
    class Meta:
        model = CollaboratorRole
        fields = [
            'id', 'name', 'description', 'company', 'type', 'type_display',
            'is_default', 'permissions', 'permission_ids',
        ]
        read_only_fields = ['id', 'company']
    
    def create(self, validated_data):
        permissions = validated_data.pop('permissions', [])
        role = CollaboratorRole.objects.create(**validated_data)
        if permissions:
            role.permissions.set(permissions)
        return role
    
    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if permissions is not None:
            instance.permissions.set(permissions)
        
        return instance


class CollaboratorSerializer(serializers.ModelSerializer):
    """
    Serializer for collaborators.
    """
    user_details = UserCreateSerializer(source='user', read_only=True)
    role_details = CollaboratorRoleSerializer(source='role', read_only=True)
    points_of_sale_details = PointOfSaleSerializer(source='points_of_sale', many=True, read_only=True)
    pos_ids = serializers.PrimaryKeyRelatedField(
        source='points_of_sale',
        queryset=CollaboratorRole.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )
    
    class Meta:
        model = Collaborator
        fields = [
            'id', 'user', 'user_details', 'role', 'role_details', 'company',
            'points_of_sale_details', 'pos_ids', 'is_active',
        ]
        read_only_fields = ['id', 'company']
    
    def create(self, validated_data):
        points_of_sale = validated_data.pop('points_of_sale', [])
        collaborator = Collaborator.objects.create(**validated_data)
        if points_of_sale:
            collaborator.points_of_sale.set(points_of_sale)
        return collaborator
    
    def update(self, instance, validated_data):
        points_of_sale = validated_data.pop('points_of_sale', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if points_of_sale is not None:
            instance.points_of_sale.set(points_of_sale)
        
        return instance

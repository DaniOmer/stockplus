"""
Collaborator views implementation.
This module contains the views for collaborators, roles, and permissions.
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from stockplus.modules.collaborator.infrastructure.models import (
    Collaborator,
    CollaboratorRole,
    CollaboratorPermission,
)
from stockplus.modules.collaborator.interfaces.serializers.collaborator_serializer import (
    CollaboratorSerializer,
    CollaboratorRoleSerializer,
    CollaboratorPermissionSerializer,
)
from stockplus.modules.collaborator.application.services import (
    CollaboratorService,
    CollaboratorRoleService,
)
from stockplus.modules.collaborator.infrastructure.repositories import (
    CollaboratorRepository,
    CollaboratorRoleRepository,
)
from stockplus.config.dependencies import get_service


class CollaboratorListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating collaborators.
    """
    serializer_class = CollaboratorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get the queryset for the view.
        
        Returns:
            A queryset of collaborators filtered by the current user's company.
        """
        company_id = self.request.user.company_id
        return Collaborator.objects.filter(company_id=company_id)
    
    def perform_create(self, serializer):
        """
        Perform the creation of a collaborator.
        
        Args:
            serializer: The serializer instance.
        """
        company_id = self.request.user.company_id
        serializer.save(company_id=company_id)


class CollaboratorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a collaborator.
    """
    serializer_class = CollaboratorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get the queryset for the view.
        
        Returns:
            A queryset of collaborators filtered by the current user's company.
        """
        company_id = self.request.user.company_id
        return Collaborator.objects.filter(company_id=company_id)


class CollaboratorRoleListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating collaborator roles.
    """
    serializer_class = CollaboratorRoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get the queryset for the view.
        
        Returns:
            A queryset of collaborator roles filtered by the current user's company.
        """
        company_id = self.request.user.company_id
        return CollaboratorRole.objects.filter(company_id=company_id)
    
    def perform_create(self, serializer):
        """
        Perform the creation of a collaborator role.
        
        Args:
            serializer: The serializer instance.
        """
        company_id = self.request.user.company_id
        serializer.save(company_id=company_id)


class CollaboratorRoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a collaborator role.
    """
    serializer_class = CollaboratorRoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get the queryset for the view.
        
        Returns:
            A queryset of collaborator roles filtered by the current user's company.
        """
        company_id = self.request.user.company_id
        return CollaboratorRole.objects.filter(company_id=company_id)


class CollaboratorPermissionListView(generics.ListAPIView):
    """
    API view for listing collaborator permissions.
    """
    serializer_class = CollaboratorPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CollaboratorPermission.objects.all()

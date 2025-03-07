"""
Company views for the company application.
This module contains the company views for the company application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from stockplus.permissions import base_permissions

from stockplus.modules.company.interfaces.serializers import CompanySerializer
from stockplus.modules.company.application.services import CompanyService
from stockplus.modules.company.infrastructure.repositories.company_repository import CompanyRepository
from stockplus.modules.company.domain.exceptions import (
    CompanyNotFoundException,
)


class CompanyCreateView(generics.CreateAPIView):
    """
    API endpoint to create a company.
    """
    serializer_class = CompanySerializer
    permission_classes = base_permissions
    
    def get_serializer_context(self):
        """
        Add the company service to the serializer context.
        
        Returns:
            dict: The serializer context
        """
        context = super().get_serializer_context()
        context['company_service'] = CompanyService(
            CompanyRepository(),
        )
        return context


class CompanyDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve and update a company.
    """
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Get the company object.
        
        Returns:
            Company: The company object
        """
        company_service = CompanyService(
            CompanyRepository(),
        )
        
        # Get the company ID from the URL
        company_id = self.kwargs.get('pk')
        
        # Get the company
        company = company_service.get_company_by_id(company_id)
        if not company:
            raise CompanyNotFoundException(f"Company with ID {company_id} not found")
        
        return company
    
    def get_serializer_context(self):
        """
        Add the company service to the serializer context.
        
        Returns:
            dict: The serializer context
        """
        context = super().get_serializer_context()
        context['company_service'] = CompanyService(
            CompanyRepository(),
        )
        return context


class CompanyActivateView(APIView):
    """
    API endpoint to activate a company.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """
        Activate a company.
        
        Args:
            request: The request
            pk: The company ID
            
        Returns:
            Response: The response
        """
        company_service = CompanyService(
            CompanyRepository(),
        )
        
        try:
            company = company_service.activate_company(pk)
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CompanyNotFoundException as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


class CompanyDeactivateView(APIView):
    """
    API endpoint to deactivate a company.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """
        Deactivate a company.
        
        Args:
            request: The request
            pk: The company ID
            
        Returns:
            Response: The response
        """
        company_service = CompanyService(
            CompanyRepository(),
        )
        
        try:
            company = company_service.deactivate_company(pk)
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CompanyNotFoundException as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

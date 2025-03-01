"""
Address views for the company application.
This module contains the address views for the company application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from builder.modules.company.interfaces.serializers import CompanyAddressSerializer
from builder.modules.company.application.services import CompanyService
from builder.modules.company.infrastructure.repositories import (
    CompanyRepository,
    CompanyAddressRepository
)
from builder.modules.company.domain.exceptions import (
    CompanyNotFoundException,
    CompanyAddressNotFoundException,
    ValidationException
)


class CompanyAddressListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list and create company addresses.
    """
    serializer_class = CompanyAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get the company addresses.
        
        Returns:
            List[CompanyAddress]: The company addresses
        """
        company_service = CompanyService(
            CompanyRepository(),
            CompanyAddressRepository()
        )
        
        # Get the company ID from the URL
        company_id = self.kwargs.get('company_id')
        
        # Get the company addresses
        return company_service.get_company_addresses(company_id)
    
    def get_serializer_context(self):
        """
        Add the company service to the serializer context.
        
        Returns:
            dict: The serializer context
        """
        context = super().get_serializer_context()
        context['company_service'] = CompanyService(
            CompanyRepository(),
            CompanyAddressRepository()
        )
        return context


class CompanyAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, and delete a company address.
    """
    serializer_class = CompanyAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Get the company address object.
        
        Returns:
            CompanyAddress: The company address object
        """
        company_service = CompanyService(
            CompanyRepository(),
            CompanyAddressRepository()
        )
        
        # Get the company address ID from the URL
        company_address_id = self.kwargs.get('pk')
        
        # Get the company address
        company_address = company_service.get_company_address_by_id(company_address_id)
        if not company_address:
            raise CompanyAddressNotFoundException(f"Company address with ID {company_address_id} not found")
        
        return company_address
    
    def get_serializer_context(self):
        """
        Add the company service to the serializer context.
        
        Returns:
            dict: The serializer context
        """
        context = super().get_serializer_context()
        context['company_service'] = CompanyService(
            CompanyRepository(),
            CompanyAddressRepository()
        )
        return context
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a company address.
        
        Args:
            request: The request
            
        Returns:
            Response: The response
        """
        company_service = CompanyService(
            CompanyRepository(),
            CompanyAddressRepository()
        )
        
        # Get the company address ID from the URL
        company_address_id = self.kwargs.get('pk')
        
        # Delete the company address
        success = company_service.delete_company_address(company_address_id)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'message': f"Company address with ID {company_address_id} not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class CompanyHeadquartersView(APIView):
    """
    API endpoint to get the headquarters address for a company.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, company_id):
        """
        Get the headquarters address for a company.
        
        Args:
            request: The request
            company_id: The company ID
            
        Returns:
            Response: The response
        """
        company_service = CompanyService(
            CompanyRepository(),
            CompanyAddressRepository()
        )
        
        try:
            company_address = company_service.get_company_headquarters(company_id)
            if not company_address:
                return Response(
                    {'message': f"No headquarters address found for company with ID {company_id}"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = CompanyAddressSerializer(company_address)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CompanyNotFoundException as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

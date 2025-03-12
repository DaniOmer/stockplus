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
from stockplus.modules.company.infrastructure.repositories import CompanyRepository
from stockplus.modules.company.domain.exceptions import (
    CompanyNotFoundException,
    CompanyAlreadyExistsException,
    ValidationException,
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
            CompanyRepository()
        )
        # The request is already added by DRF's get_serializer_context
        return context

    def create(self, request, *args, **kwargs):
        """
        Create a new company.
        
        Args:
            request: The request

        Returns:
            Response: The response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            company = serializer.save()
            return Response({
                'message': 'Company created successfully.',
                'company': {
                    'id': company.id,
                    'denomination': company.denomination,
                    'legal_form': company.legal_form,
                    'since': company.since,
                    'site': company.site,
                    'effective': company.effective,
                    'resume': company.resume,
                    'registration_number': company.registration_number,
                }
            }, status=status.HTTP_201_CREATED)
        except ValidationException as e:
            return Response({
                'message': str(e),
                'error_type': 'validation_error'
            }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({
                'message': str(e),
                'error_type': 'value_error'
            }, status=status.HTTP_400_BAD_REQUEST)
        except CompanyAlreadyExistsException as e:
            return Response({
                'message': str(e),
                'error_type': 'company_exists'
            }, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({
                'message': f"An error occurred: {str(e)}",
                'error_type': 'server_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    
    def update(self, request, *args, **kwargs):
        """
        Update a company.
        
        Args:
            request: The request
            
        Returns:
            Response: The response
        """
        try:
            return super().update(request, *args, **kwargs)
        except ValidationException as e:
            return Response({
                'message': str(e),
                'error_type': 'validation_error'
            }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({
                'message': str(e),
                'error_type': 'value_error'
            }, status=status.HTTP_400_BAD_REQUEST)
        except CompanyAlreadyExistsException as e:
            return Response({
                'message': str(e),
                'error_type': 'company_exists'
            }, status=status.HTTP_409_CONFLICT)
        except CompanyNotFoundException as e:
            return Response({
                'message': str(e),
                'error_type': 'company_not_found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'message': f"An error occurred: {str(e)}",
                'error_type': 'server_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            return Response({
                'message': 'Company activated successfully.',
                'company': serializer.data
            }, status=status.HTTP_200_OK)
        except CompanyNotFoundException as e:
            return Response({
                'message': str(e),
                'error_type': 'company_not_found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'message': f"An error occurred: {str(e)}",
                'error_type': 'server_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            return Response({
                'message': 'Company deactivated successfully.',
                'company': serializer.data
            }, status=status.HTTP_200_OK)
        except CompanyNotFoundException as e:
            return Response({
                'message': str(e),
                'error_type': 'company_not_found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'message': f"An error occurred: {str(e)}",
                'error_type': 'server_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

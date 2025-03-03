"""
Views for the address application.
This module contains the views for the address application.
"""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from builder.modules.address.application.services import AddressService
from builder.modules.address.infrastructure.repositories import (
    UserAddressRepository,
    CompanyAddressRepository
)
from builder.modules.address.infrastructure.geolocation import get_geolocation_service
from builder.modules.address.interfaces.serializers.address import (
    UserAddressSerializer,
    CompanyAddressSerializer,
    UserAddressListSerializer,
    CompanyAddressListSerializer
)


class UserAddressViewSet(viewsets.ViewSet):
    """
    ViewSet for user addresses.
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.address_service = AddressService(
            address_repository=UserAddressRepository(),
            geolocation_service=get_geolocation_service()
        )
    
    def list(self, request):
        """
        List all addresses for the current user.
        """
        addresses = self.address_service.get_addresses_by_user_id(request.user.id)
        serializer = UserAddressListSerializer(addresses, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific address.
        """
        address = self.address_service.get_address_by_id(pk)
        if not address:
            return Response(
                {"detail": f"Address with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if the address belongs to the current user
        if address.user_id != request.user.id:
            return Response(
                {"detail": "You do not have permission to access this address"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = UserAddressSerializer(address)
        return Response(serializer.data)
    
    def create(self, request):
        """
        Create a new address for the current user.
        """
        # Add user_id to the data
        data = request.data.copy()
        data['user_id'] = request.user.id
        
        serializer = UserAddressSerializer(
            data=data,
            context={'address_service': self.address_service}
        )
        
        if serializer.is_valid():
            address = serializer.save()
            
            # If this is the first address or is_default is True, make it the default
            if data.get('is_default', False) or self.address_service.get_addresses_by_user_id(request.user.id).count() == 1:
                # Get all other addresses and set is_default to False
                for other_address in self.address_service.get_addresses_by_user_id(request.user.id):
                    if other_address.id != address.id and other_address.is_default:
                        other_address.is_default = False
                        self.address_service.address_repository.save(other_address)
                
                # Set this address as default
                address.is_default = True
                self.address_service.address_repository.save(address)
            
            return Response(
                UserAddressSerializer(address).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """
        Update an address.
        """
        address = self.address_service.get_address_by_id(pk)
        if not address:
            return Response(
                {"detail": f"Address with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if the address belongs to the current user
        if address.user_id != request.user.id:
            return Response(
                {"detail": "You do not have permission to modify this address"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Add user_id to the data
        data = request.data.copy()
        data['user_id'] = request.user.id
        
        serializer = UserAddressSerializer(
            address,
            data=data,
            context={'address_service': self.address_service},
            partial=True
        )
        
        if serializer.is_valid():
            updated_address = serializer.save()
            
            # If is_default is True, make it the default and update other addresses
            if data.get('is_default', False) and not address.is_default:
                # Get all other addresses and set is_default to False
                for other_address in self.address_service.get_addresses_by_user_id(request.user.id):
                    if other_address.id != updated_address.id and other_address.is_default:
                        other_address.is_default = False
                        self.address_service.address_repository.save(other_address)
            
            return Response(UserAddressSerializer(updated_address).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Delete an address.
        """
        address = self.address_service.get_address_by_id(pk)
        if not address:
            return Response(
                {"detail": f"Address with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if the address belongs to the current user
        if address.user_id != request.user.id:
            return Response(
                {"detail": "You do not have permission to delete this address"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if this is the default address
        was_default = address.is_default
        
        # Delete the address
        self.address_service.delete_address(pk)
        
        # If this was the default address, set another address as default
        if was_default:
            addresses = self.address_service.get_addresses_by_user_id(request.user.id)
            if addresses:
                new_default = addresses[0]
                new_default.is_default = True
                self.address_service.address_repository.save(new_default)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """
        Set an address as the default address.
        """
        address = self.address_service.get_address_by_id(pk)
        if not address:
            return Response(
                {"detail": f"Address with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if the address belongs to the current user
        if address.user_id != request.user.id:
            return Response(
                {"detail": "You do not have permission to modify this address"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get all other addresses and set is_default to False
        for other_address in self.address_service.get_addresses_by_user_id(request.user.id):
            if other_address.id != address.id and other_address.is_default:
                other_address.is_default = False
                self.address_service.address_repository.save(other_address)
        
        # Set this address as default
        address.is_default = True
        self.address_service.address_repository.save(address)
        
        return Response(UserAddressSerializer(address).data)


class CompanyAddressViewSet(viewsets.ViewSet):
    """
    ViewSet for company addresses.
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.address_service = AddressService(
            address_repository=CompanyAddressRepository(),
            geolocation_service=get_geolocation_service()
        )
    
    def list(self, request):
        """
        List all addresses for the current user's company.
        """
        if not request.user.company_id:
            return Response(
                {"detail": "You are not associated with any company"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        addresses = self.address_service.get_addresses_by_company_id(request.user.company_id)
        serializer = CompanyAddressListSerializer(addresses, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific address.
        """
        if not request.user.company_id:
            return Response(
                {"detail": "You are not associated with any company"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        address = self.address_service.get_address_by_id(pk)
        if not address:
            return Response(
                {"detail": f"Address with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if the address belongs to the current user's company
        if address.company_id != request.user.company_id:
            return Response(
                {"detail": "You do not have permission to access this address"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = CompanyAddressSerializer(address)
        return Response(serializer.data)
    
    def create(self, request):
        """
        Create a new address for the current user's company.
        """
        if not request.user.company_id:
            return Response(
                {"detail": "You are not associated with any company"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Add company_id to the data
        data = request.data.copy()
        data['company_id'] = request.user.company_id
        
        serializer = CompanyAddressSerializer(
            data=data,
            context={'address_service': self.address_service}
        )
        
        if serializer.is_valid():
            address = serializer.save()
            return Response(
                CompanyAddressSerializer(address).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """
        Update an address.
        """
        if not request.user.company_id:
            return Response(
                {"detail": "You are not associated with any company"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        address = self.address_service.get_address_by_id(pk)
        if not address:
            return Response(
                {"detail": f"Address with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if the address belongs to the current user's company
        if address.company_id != request.user.company_id:
            return Response(
                {"detail": "You do not have permission to modify this address"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Add company_id to the data
        data = request.data.copy()
        data['company_id'] = request.user.company_id
        
        serializer = CompanyAddressSerializer(
            address,
            data=data,
            context={'address_service': self.address_service},
            partial=True
        )
        
        if serializer.is_valid():
            updated_address = serializer.save()
            return Response(CompanyAddressSerializer(updated_address).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Delete an address.
        """
        if not request.user.company_id:
            return Response(
                {"detail": "You are not associated with any company"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        address = self.address_service.get_address_by_id(pk)
        if not address:
            return Response(
                {"detail": f"Address with ID {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if the address belongs to the current user's company
        if address.company_id != request.user.company_id:
            return Response(
                {"detail": "You do not have permission to delete this address"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Delete the address
        self.address_service.delete_address(pk)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

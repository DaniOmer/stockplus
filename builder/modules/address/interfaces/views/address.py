"""
Views for the address application.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from builder.modules.address.application.services import AddressService
from builder.modules.address.infrastructure.repositories import (
    UserAddressRepository,
    CompanyAddressRepository
)
from builder.modules.address.infrastructure.geolocation import get_geolocation_service
from builder.modules.address.interfaces.serializers.address import (
    AddressSerializer,
    UserAddressSerializer,
    CompanyAddressSerializer,
    GeocodeAddressSerializer,
    ReverseGeocodeSerializer
)
from builder.modules.address.domain.exceptions import (
    InvalidAddressException,
    AddressNotFoundException,
    GeolocationException
)


class UserAddressListCreateView(APIView):
    """View for listing and creating user addresses."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        List user addresses.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        address_service = AddressService(UserAddressRepository())
        
        # Filter addresses by user if not admin
        filters = {}
        if not request.user.is_staff:
            filters['user_id'] = request.user.id
        
        addresses = address_service.list_addresses(filters)
        
        serializer = UserAddressSerializer(addresses, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a user address.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        serializer = UserAddressSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure the user can only create addresses for themselves
        if not request.user.is_staff and serializer.validated_data['user_id'] != request.user.id:
            return Response(
                {'error': 'You can only create addresses for yourself'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            address_service = AddressService(
                UserAddressRepository(),
                get_geolocation_service()
            )
            
            address = address_service.create_address(serializer.validated_data)
            
            response_serializer = UserAddressSerializer(address)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except InvalidAddressException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserAddressDetailView(APIView):
    """View for retrieving, updating, and deleting a user address."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, address_id):
        """
        Get a user address by ID.
        
        Args:
            request: The HTTP request
            address_id: The ID of the address
            
        Returns:
            Response: The HTTP response
        """
        try:
            address_service = AddressService(UserAddressRepository())
            address = address_service.get_address(address_id)
            
            # Ensure the user can only view their own addresses
            if not request.user.is_staff and address.user_id != request.user.id:
                return Response(
                    {'error': 'You can only view your own addresses'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = UserAddressSerializer(address)
            return Response(serializer.data)
        except AddressNotFoundException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, address_id):
        """
        Update a user address.
        
        Args:
            request: The HTTP request
            address_id: The ID of the address
            
        Returns:
            Response: The HTTP response
        """
        serializer = UserAddressSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            address_service = AddressService(
                UserAddressRepository(),
                get_geolocation_service()
            )
            
            # Get the address to check permissions
            address = address_service.get_address(address_id)
            
            # Ensure the user can only update their own addresses
            if not request.user.is_staff and address.user_id != request.user.id:
                return Response(
                    {'error': 'You can only update your own addresses'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Ensure the user can't change the user_id
            if 'user_id' in serializer.validated_data and serializer.validated_data['user_id'] != address.user_id:
                return Response(
                    {'error': 'You cannot change the user ID of an address'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            updated_address = address_service.update_address(address_id, serializer.validated_data)
            
            response_serializer = UserAddressSerializer(updated_address)
            return Response(response_serializer.data)
        except AddressNotFoundException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except InvalidAddressException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, address_id):
        """
        Delete a user address.
        
        Args:
            request: The HTTP request
            address_id: The ID of the address
            
        Returns:
            Response: The HTTP response
        """
        try:
            address_service = AddressService(UserAddressRepository())
            
            # Get the address to check permissions
            address = address_service.get_address(address_id)
            
            # Ensure the user can only delete their own addresses
            if not request.user.is_staff and address.user_id != request.user.id:
                return Response(
                    {'error': 'You can only delete your own addresses'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            address_service.delete_address(address_id)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AddressNotFoundException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CompanyAddressListCreateView(APIView):
    """View for listing and creating company addresses."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        List company addresses.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        address_service = AddressService(CompanyAddressRepository())
        
        # Filter addresses by company if not admin
        filters = {}
        if not request.user.is_staff:
            # Get the companies the user is associated with
            from builder.models import Company
            company_ids = Company.objects.filter(owner=request.user).values_list('id', flat=True)
            
            if not company_ids:
                return Response([])
            
            filters['company_id__in'] = list(company_ids)
        
        addresses = address_service.list_addresses(filters)
        
        serializer = CompanyAddressSerializer(addresses, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a company address.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        serializer = CompanyAddressSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure the user can only create addresses for companies they own
        if not request.user.is_staff:
            from builder.models import Company
            try:
                company = Company.objects.get(id=serializer.validated_data['company_id'])
                if company.owner != request.user:
                    return Response(
                        {'error': 'You can only create addresses for companies you own'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Company.DoesNotExist:
                return Response(
                    {'error': 'Company not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        try:
            address_service = AddressService(
                CompanyAddressRepository(),
                get_geolocation_service()
            )
            
            address = address_service.create_address(serializer.validated_data)
            
            response_serializer = CompanyAddressSerializer(address)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except InvalidAddressException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CompanyAddressDetailView(APIView):
    """View for retrieving, updating, and deleting a company address."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, address_id):
        """
        Get a company address by ID.
        
        Args:
            request: The HTTP request
            address_id: The ID of the address
            
        Returns:
            Response: The HTTP response
        """
        try:
            address_service = AddressService(CompanyAddressRepository())
            address = address_service.get_address(address_id)
            
            # Ensure the user can only view addresses for companies they own
            if not request.user.is_staff:
                from builder.models import Company
                try:
                    company = Company.objects.get(id=address.company_id)
                    if company.owner != request.user:
                        return Response(
                            {'error': 'You can only view addresses for companies you own'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                except Company.DoesNotExist:
                    return Response(
                        {'error': 'Company not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            serializer = CompanyAddressSerializer(address)
            return Response(serializer.data)
        except AddressNotFoundException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, address_id):
        """
        Update a company address.
        
        Args:
            request: The HTTP request
            address_id: The ID of the address
            
        Returns:
            Response: The HTTP response
        """
        serializer = CompanyAddressSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            address_service = AddressService(
                CompanyAddressRepository(),
                get_geolocation_service()
            )
            
            # Get the address to check permissions
            address = address_service.get_address(address_id)
            
            # Ensure the user can only update addresses for companies they own
            if not request.user.is_staff:
                from builder.models import Company
                try:
                    company = Company.objects.get(id=address.company_id)
                    if company.owner != request.user:
                        return Response(
                            {'error': 'You can only update addresses for companies you own'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                except Company.DoesNotExist:
                    return Response(
                        {'error': 'Company not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            # Ensure the user can't change the company_id
            if 'company_id' in serializer.validated_data and serializer.validated_data['company_id'] != address.company_id:
                return Response(
                    {'error': 'You cannot change the company ID of an address'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            updated_address = address_service.update_address(address_id, serializer.validated_data)
            
            response_serializer = CompanyAddressSerializer(updated_address)
            return Response(response_serializer.data)
        except AddressNotFoundException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except InvalidAddressException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, address_id):
        """
        Delete a company address.
        
        Args:
            request: The HTTP request
            address_id: The ID of the address
            
        Returns:
            Response: The HTTP response
        """
        try:
            address_service = AddressService(CompanyAddressRepository())
            
            # Get the address to check permissions
            address = address_service.get_address(address_id)
            
            # Ensure the user can only delete addresses for companies they own
            if not request.user.is_staff:
                from builder.models import Company
                try:
                    company = Company.objects.get(id=address.company_id)
                    if company.owner != request.user:
                        return Response(
                            {'error': 'You can only delete addresses for companies you own'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                except Company.DoesNotExist:
                    return Response(
                        {'error': 'Company not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            address_service.delete_address(address_id)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AddressNotFoundException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GeocodeAddressView(APIView):
    """View for geocoding an address."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Geocode an address.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        serializer = GeocodeAddressSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Determine the repository based on the address type
            from builder.models import UserAddress, CompanyAddress
            
            address_id = serializer.validated_data['address_id']
            
            try:
                UserAddress.objects.get(id=address_id)
                repository = UserAddressRepository()
            except UserAddress.DoesNotExist:
                try:
                    CompanyAddress.objects.get(id=address_id)
                    repository = CompanyAddressRepository()
                except CompanyAddress.DoesNotExist:
                    return Response(
                        {'error': 'Address not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            address_service = AddressService(
                repository,
                get_geolocation_service()
            )
            
            latitude, longitude = address_service.geocode_address(address_id)
            
            return Response({
                'latitude': latitude,
                'longitude': longitude
            })
        except AddressNotFoundException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except GeolocationException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReverseGeocodeView(APIView):
    """View for reverse geocoding coordinates."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Reverse geocode coordinates.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        serializer = ReverseGeocodeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            geolocation_service = get_geolocation_service()
            
            if not geolocation_service:
                return Response(
                    {'error': 'Geolocation service not available'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            address_data = geolocation_service.reverse_geocode(
                serializer.validated_data['latitude'],
                serializer.validated_data['longitude']
            )
            
            return Response(address_data)
        except GeolocationException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

"""
Serializers for the address application.
"""
from rest_framework import serializers


class AddressSerializer(serializers.Serializer):
    """Serializer for address objects."""
    
    id = serializers.IntegerField(read_only=True)
    address = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    complement = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    city = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    postal_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    state = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    state_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    country = serializers.CharField()
    country_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cedex = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cedex_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    special = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    index = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        fields = [
            'id', 'address', 'complement', 'city', 'postal_code',
            'state', 'state_code', 'country', 'country_code',
            'cedex', 'cedex_code', 'special', 'index',
            'latitude', 'longitude', 'created_at', 'updated_at'
        ]


class UserAddressSerializer(AddressSerializer):
    """Serializer for user address objects."""
    
    user_id = serializers.IntegerField()
    
    class Meta(AddressSerializer.Meta):
        fields = AddressSerializer.Meta.fields + ['user_id']


class CompanyAddressSerializer(AddressSerializer):
    """Serializer for company address objects."""
    
    company_id = serializers.IntegerField()
    
    class Meta(AddressSerializer.Meta):
        fields = AddressSerializer.Meta.fields + ['company_id']


class GeocodeAddressSerializer(serializers.Serializer):
    """Serializer for geocoding an address."""
    
    address_id = serializers.IntegerField()
    
    class Meta:
        fields = ['address_id']


class ReverseGeocodeSerializer(serializers.Serializer):
    """Serializer for reverse geocoding coordinates."""
    
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    
    class Meta:
        fields = ['latitude', 'longitude']

from rest_framework import serializers

from builder.models import Company, CompanyAddress

class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        exclude = ['owner']

class CompanyAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAddress
        exclude = ['company']
"""
Serializers for the company application.
This module contains the serializers for the company application.
"""

from rest_framework import serializers

from builder.modules.company.domain.models import Company, CompanyAddress
from builder.modules.company.application.services import CompanyService
from builder.modules.company.domain.exceptions import (
    CompanyNotFoundException,
    CompanyAlreadyExistsException,
    CompanyAddressNotFoundException,
    ValidationException
)


class CompanySerializer(serializers.Serializer):
    """
    Serializer for the Company model.
    """
    id = serializers.IntegerField(read_only=True)
    denomination = serializers.CharField()
    legal_form = serializers.CharField()
    since = serializers.DateField(required=False, allow_null=True)
    site = serializers.URLField(required=False, allow_null=True)
    effective = serializers.IntegerField(required=False, allow_null=True)
    resume = serializers.CharField(required=False, allow_null=True)
    registration_number = serializers.CharField(required=False, allow_null=True)
    tax_id = serializers.CharField(required=False, allow_null=True)
    siren = serializers.CharField(required=False, allow_null=True)
    siret = serializers.CharField(required=False, allow_null=True)
    ifu = serializers.CharField(required=False, allow_null=True)
    idu = serializers.CharField(required=False, allow_null=True)
    is_active = serializers.BooleanField(read_only=True)
    
    def create(self, validated_data):
        """
        Create a new company.
        
        Args:
            validated_data: The validated data
            
        Returns:
            Company: The created company
            
        Raises:
            ValidationException: If the company data is invalid
            CompanyAlreadyExistsException: If a company with the given denomination or registration number already exists
        """
        company_service = self.context['company_service']
        
        try:
            company = company_service.create_company(
                denomination=validated_data['denomination'],
                legal_form=validated_data['legal_form'],
                since=validated_data.get('since'),
                site=validated_data.get('site'),
                effective=validated_data.get('effective'),
                resume=validated_data.get('resume'),
                registration_number=validated_data.get('registration_number'),
                tax_id=validated_data.get('tax_id'),
                siren=validated_data.get('siren'),
                siret=validated_data.get('siret'),
                ifu=validated_data.get('ifu'),
                idu=validated_data.get('idu')
            )
            return company
        except (ValidationException, CompanyAlreadyExistsException) as e:
            raise serializers.ValidationError(str(e))
    
    def update(self, instance, validated_data):
        """
        Update a company.
        
        Args:
            instance: The company to update
            validated_data: The validated data
            
        Returns:
            Company: The updated company
        """
        company_service = self.context['company_service']
        
        try:
            # Update general information
            company = company_service.update_company_info(
                company_id=instance.id,
                denomination=validated_data.get('denomination'),
                since=validated_data.get('since'),
                site=validated_data.get('site'),
                effective=validated_data.get('effective'),
                resume=validated_data.get('resume'),
                legal_form=validated_data.get('legal_form')
            )
            
            # Update identifiers
            company = company_service.update_company_identifiers(
                company_id=instance.id,
                registration_number=validated_data.get('registration_number'),
                tax_id=validated_data.get('tax_id'),
                siren=validated_data.get('siren'),
                siret=validated_data.get('siret'),
                ifu=validated_data.get('ifu'),
                idu=validated_data.get('idu')
            )
            
            return company
        except (ValidationException, CompanyAlreadyExistsException, CompanyNotFoundException) as e:
            raise serializers.ValidationError(str(e))


class CompanyAddressSerializer(serializers.Serializer):
    """
    Serializer for the CompanyAddress model.
    """
    id = serializers.IntegerField(read_only=True)
    company_id = serializers.IntegerField(required=False)
    address_id = serializers.IntegerField()
    is_siege = serializers.BooleanField(required=False, default=False)
    
    def create(self, validated_data):
        """
        Create a new company address.
        
        Args:
            validated_data: The validated data
            
        Returns:
            CompanyAddress: The created company address
            
        Raises:
            ValidationException: If the company address data is invalid
            CompanyNotFoundException: If the company is not found
        """
        company_service = self.context['company_service']
        
        try:
            company_id = validated_data.get('company_id') or self.context['request'].user.company_id
            company_address = company_service.add_company_address(
                company_id=company_id,
                address_id=validated_data['address_id'],
                is_siege=validated_data.get('is_siege', False)
            )
            return company_address
        except (ValidationException, CompanyNotFoundException) as e:
            raise serializers.ValidationError(str(e))
    
    def update(self, instance, validated_data):
        """
        Update a company address.
        
        Args:
            instance: The company address to update
            validated_data: The validated data
            
        Returns:
            CompanyAddress: The updated company address
        """
        company_service = self.context['company_service']
        
        try:
            # Update is_siege
            if validated_data.get('is_siege'):
                company_address = company_service.set_company_headquarters(instance.id)
            else:
                company_address = company_service.unset_company_headquarters(instance.id)
            
            return company_address
        except (CompanyAddressNotFoundException) as e:
            raise serializers.ValidationError(str(e))

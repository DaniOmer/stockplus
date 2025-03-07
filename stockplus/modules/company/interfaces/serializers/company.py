"""
Serializers for the company application.
This module contains the serializers for the company application.
"""

from rest_framework import serializers

from stockplus.modules.company.domain.exceptions import (
    CompanyNotFoundException,
    CompanyAlreadyExistsException,
    ValidationException
)


class CompanySerializer(serializers.Serializer):
    """
    Serializer for the Company model.
    """
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

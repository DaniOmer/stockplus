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
from stockplus.modules.company.infrastructure.models import Company


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for the Company model.
    """
    class Meta:
        model = Company
        fields = ['id', 'denomination', 'legal_form', 'since', 'site', 'effective', 'resume', 'registration_number', 'tax_id','siren','siret', 'ifu', 'idu', 'is_disable',]
        read_only_fields = ['id']
    
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
        user = self.context.get('request').user if 'request' in self.context else None
        
        try:
            # Pass the validated data directly to the service
            company = company_service.create_company(data=validated_data, user=user)
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
            # Split the data into general info and identifiers
            general_info = {}
            identifiers = {}
            
            # General info fields
            for field in ['denomination', 'since', 'site', 'effective', 'resume', 'legal_form']:
                if field in validated_data:
                    general_info[field] = validated_data.get(field)
            
            # Identifier fields
            for field in ['registration_number', 'tax_id', 'siren', 'siret', 'ifu', 'idu']:
                if field in validated_data:
                    identifiers[field] = validated_data.get(field)
            
            # Update general information if there are any changes
            if general_info:
                company = company_service.update_company_info(
                    company_id=instance.id,
                    **general_info
                )
            else:
                company = instance
            
            # Update identifiers if there are any changes
            if identifiers:
                company = company_service.update_company_identifiers(
                    company_id=instance.id,
                    **identifiers
                )
            
            return company
        except (ValidationException, CompanyAlreadyExistsException, CompanyNotFoundException) as e:
            raise serializers.ValidationError(str(e))

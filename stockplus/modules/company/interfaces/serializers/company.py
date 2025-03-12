"""
Serializers for the company application.
This module contains the serializers for the company application.
"""

from pydantic import ValidationError as PydanticValidationError

from rest_framework import serializers
from stockplus.modules.company.domain.exceptions import ValidationException
from stockplus.modules.company.infrastructure.models import Company
from stockplus.modules.company.infrastructure.dtos import (
    CompanyCreateDTO, 
    CompanyUpdateDTO,
    CompanyPartialUpdateDTO,
)

class CompanyBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'denomination', 'since', 'site', 
            'effective', 'registration_number', 
            'legal_form', 'tax_id', 'siren', 'siret', 
            'ifu', 'idu', 'is_disable'
        ]
        read_only_fields = ['id', 'is_disable']

class CompanyCreateSerializer(CompanyBaseSerializer):
    def validate(self, attrs):
        try:
            return CompanyCreateDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException(e.errors()[0]['msg'])

class CompanyUpdateSerializer(CompanyBaseSerializer):
    def validate(self, attrs):
        try:
            return CompanyUpdateDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException("Could not validate company data", errors=e.errors())

class CompanyPartialUpdateSerializer(CompanyBaseSerializer):
    def validate(self, attrs):
        try:
            return CompanyPartialUpdateDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException("Could not validate company data", errors=e.errors())
        
class CompanyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['is_disable']
        read_only_fields = ['is_disable']

"""
Application services for the company application.
This module contains the application services for the company application.
"""

from typing import Optional, Dict, Any

from stockplus.modules.company.domain.entities.company_entity import Company
from stockplus.modules.company.domain.exceptions import (
    CompanyNotFoundException,
    CompanyAlreadyExistsException,
    ValidationException,
)
from stockplus.modules.company.application.interfaces import (
    ICompanyRepository,
)
from stockplus.modules.company.infrastructure.dtos.company_dto import (
    CompanyCreateDTO,
    CompanyUpdateInfoDTO,
    CompanyUpdateIdentifiersDTO,
)

class CompanyService:
    """
    Company service.
    
    This class implements the application logic for companies. It uses the company repository
    to access and manipulate company data, and enforces business rules.
    """
    
    def __init__(self, company_repository: ICompanyRepository):
        """
        Initialize a new CompanyService instance.
        
        Args: company_repository: The company repository to use
        """
        self.company_repository = company_repository
    
    def get_company_by_id(self, company_id) -> Optional[Company]:
        """
        Get a company by ID.
        
        Args:
            company_id: The ID of the company to retrieve
            
        Returns:
            Company: The company with the given ID, or None if not found
        """
        return self.company_repository.get_by_id(company_id)
    
    def get_company_by_denomination(self, denomination) -> Optional[Company]:
        """
        Get a company by denomination.
        
        Args:
            denomination: The denomination of the company to retrieve
            
        Returns:
            Company: The company with the given denomination, or None if not found
        """
        return self.company_repository.get_by_denomination(denomination)
    
    def get_company_by_registration_number(self, registration_number) -> Optional[Company]:
        """
        Get a company by registration number.
        
        Args:
            registration_number: The registration number of the company to retrieve
            
        Returns:
            Company: The company with the given registration number, or None if not found
        """
        return self.company_repository.get_by_registration_number(registration_number)
    
    def create_company(self, data: Dict[str, Any], user) -> Company:
        """
        Create a new company.
        
        Args:
            data: The company data
            user: The user creating the company
            
        Returns:
            Company: The created company
            
        Raises:
            ValidationException: If the company data is invalid
            CompanyAlreadyExistsException: If a company with the given denomination or registration number already exists
        """
        try:
            # Validate data using DTO
            validated_data = CompanyCreateDTO(**data).model_dump(exclude_none=True)
            
            # Check if company already exists
            if self.company_repository.get_by_denomination(validated_data['denomination']):
                raise CompanyAlreadyExistsException(f"Company with denomination {validated_data['denomination']} already exists")

            # Check if the current user already has the company
            if hasattr(user, 'company_id') and user.company_id and self.company_repository.get_by_id(user.company_id):
                raise CompanyAlreadyExistsException(f"User already has a company")
            
            # Check if registration number already exists
            if validated_data.get('registration_number') and self.company_repository.get_by_registration_number(validated_data['registration_number']):
                raise CompanyAlreadyExistsException(f"Company with registration number {validated_data['registration_number']} already exists")
            
            # Create new company
            company = Company(**validated_data)
            
            # Save company
            return self.company_repository.save(company)
        except ValueError as e:
            # Catch Pydantic validation errors
            raise ValidationException(str(e))
    
    def update_company_info(self, company_id, **update_data) -> Company:
        """
        Update a company's general information.
        
        Args:
            company_id: The ID of the company to update
            **update_data: The data to update (denomination, since, site, effective, resume, legal_form)
            
        Returns:
            Company: The updated company
            
        Raises:
            ValidationException: If the update data is invalid
            CompanyNotFoundException: If the company is not found
            CompanyAlreadyExistsException: If a company with the given denomination already exists
        """
        try:
            # Validate data using DTO
            validated_data = CompanyUpdateInfoDTO(**update_data).model_dump(exclude_none=True)
            
            if not validated_data:
                return self.get_company_by_id(company_id)
            
            # Get company
            company = self.company_repository.get_by_id(company_id)
            if not company:
                raise CompanyNotFoundException(f"Company with ID {company_id} not found")
            
            # Check if denomination already exists
            if 'denomination' in validated_data and validated_data['denomination'] != company.denomination and self.company_repository.get_by_denomination(validated_data['denomination']):
                raise CompanyAlreadyExistsException(f"Company with denomination {validated_data['denomination']} already exists")
            
            # Update company
            company.update_info(**validated_data)
            
            # Save company
            return self.company_repository.save(company)
        except ValueError as e:
            # Catch Pydantic validation errors
            raise ValidationException(str(e))
    
    def update_company_identifiers(self, company_id, **update_data) -> Company:
        """
        Update a company's identifiers.
        
        Args:
            company_id: The ID of the company to update
            **update_data: The data to update (registration_number, tax_id, siren, siret, ifu, idu)
            
        Returns:
            Company: The updated company
            
        Raises:
            ValidationException: If the update data is invalid
            CompanyNotFoundException: If the company is not found
            CompanyAlreadyExistsException: If a company with the given registration number already exists
        """
        try:
            # Validate data using DTO
            validated_data = CompanyUpdateIdentifiersDTO(**update_data).dict(exclude_none=True)
            
            if not validated_data:
                return self.get_company_by_id(company_id)  # No updates to make
            
            # Get company
            company = self.company_repository.get_by_id(company_id)
            if not company:
                raise CompanyNotFoundException(f"Company with ID {company_id} not found")
            
            # Check if registration number already exists
            if 'registration_number' in validated_data and validated_data['registration_number'] != company.registration_number and self.company_repository.get_by_registration_number(validated_data['registration_number']):
                raise CompanyAlreadyExistsException(f"Company with registration number {validated_data['registration_number']} already exists")
            
            # Update company
            company.update_identifiers(**validated_data)
            
            # Save company
            return self.company_repository.save(company)
        except ValueError as e:
            # Catch Pydantic validation errors
            raise ValidationException(str(e))
    
    def activate_company(self, company_id) -> Company:
        """
        Activate a company.
        
        Args:
            company_id: The ID of the company to activate
            
        Returns:
            Company: The activated company
            
        Raises:
            CompanyNotFoundException: If the company is not found
        """
        # Get company
        company = self.company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundException(f"Company with ID {company_id} not found")
        
        # Activate company
        company.activate()
        
        # Save company
        return self.company_repository.save(company)
    
    def deactivate_company(self, company_id) -> Company:
        """
        Deactivate a company.
        
        Args:
            company_id: The ID of the company to deactivate
            
        Returns:
            Company: The deactivated company
            
        Raises:
            CompanyNotFoundException: If the company is not found
        """
        # Get company
        company = self.company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundException(f"Company with ID {company_id} not found")
        
        # Deactivate company
        company.deactivate()
        
        # Save company
        return self.company_repository.save(company)
    
    def delete_company(self, company_id) -> bool:
        """
        Delete a company.
        
        Args:
            company_id: The ID of the company to delete
            
        Returns:
            bool: True if the company was deleted, False otherwise
        """
        return self.company_repository.delete(company_id)

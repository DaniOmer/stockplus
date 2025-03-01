"""
Application services for the company application.
This module contains the application services for the company application.
"""

from typing import List, Optional

from builder.modules.company.domain.models import Company, CompanyAddress
from builder.modules.company.domain.exceptions import (
    CompanyNotFoundException,
    CompanyAlreadyExistsException,
    CompanyAddressNotFoundException,
    ValidationException
)
from builder.modules.company.application.interfaces import (
    CompanyRepositoryInterface,
    CompanyAddressRepositoryInterface
)


class CompanyService:
    """
    Company service.
    
    This class implements the application logic for companies. It uses the company repository
    to access and manipulate company data, and enforces business rules.
    """
    
    def __init__(self, company_repository: CompanyRepositoryInterface,
                 company_address_repository: CompanyAddressRepositoryInterface):
        """
        Initialize a new CompanyService instance.
        
        Args:
            company_repository: The company repository to use
            company_address_repository: The company address repository to use
        """
        self.company_repository = company_repository
        self.company_address_repository = company_address_repository
    
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
    
    def create_company(self, denomination, legal_form, since=None, site=None, effective=None,
                      resume=None, registration_number=None, tax_id=None, siren=None,
                      siret=None, ifu=None, idu=None) -> Company:
        """
        Create a new company.
        
        Args:
            denomination: The company's name
            legal_form: The company's legal form
            since: The date the company was founded
            site: The company's website URL
            effective: The number of employees
            resume: A description of the company
            registration_number: The company's registration number
            tax_id: The company's tax ID
            siren: The company's SIREN number (French companies)
            siret: The company's SIRET number (French companies)
            ifu: The company's IFU number
            idu: The company's IDU number
            
        Returns:
            Company: The newly created company
            
        Raises:
            ValidationException: If the company is invalid
            CompanyAlreadyExistsException: If a company with the given denomination or registration number already exists
        """
        # Validate input
        if not denomination:
            raise ValidationException("Denomination is required")
        if not legal_form:
            raise ValidationException("Legal form is required")
        
        # Check if company already exists
        if self.company_repository.get_by_denomination(denomination):
            raise CompanyAlreadyExistsException(f"Company with denomination {denomination} already exists")
        
        if registration_number and self.company_repository.get_by_registration_number(registration_number):
            raise CompanyAlreadyExistsException(f"Company with registration number {registration_number} already exists")
        
        # Create new company
        company = Company(
            denomination=denomination,
            legal_form=legal_form,
            since=since,
            site=site,
            effective=effective,
            resume=resume,
            registration_number=registration_number,
            tax_id=tax_id,
            siren=siren,
            siret=siret,
            ifu=ifu,
            idu=idu
        )
        
        # Save company
        return self.company_repository.save(company)
    
    def update_company_info(self, company_id, denomination=None, since=None, site=None,
                           effective=None, resume=None, legal_form=None) -> Company:
        """
        Update a company's general information.
        
        Args:
            company_id: The ID of the company to update
            denomination: The company's new name
            since: The new date the company was founded
            site: The company's new website URL
            effective: The new number of employees
            resume: The new description of the company
            legal_form: The company's new legal form
            
        Returns:
            Company: The updated company
            
        Raises:
            CompanyNotFoundException: If the company is not found
            CompanyAlreadyExistsException: If a company with the given denomination already exists
        """
        # Get company
        company = self.company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundException(f"Company with ID {company_id} not found")
        
        # Check if denomination already exists
        if denomination and denomination != company.denomination and self.company_repository.get_by_denomination(denomination):
            raise CompanyAlreadyExistsException(f"Company with denomination {denomination} already exists")
        
        # Update company
        company.update_info(
            denomination=denomination,
            since=since,
            site=site,
            effective=effective,
            resume=resume,
            legal_form=legal_form
        )
        
        # Save company
        return self.company_repository.save(company)
    
    def update_company_identifiers(self, company_id, registration_number=None, tax_id=None,
                                  siren=None, siret=None, ifu=None, idu=None) -> Company:
        """
        Update a company's identifiers.
        
        Args:
            company_id: The ID of the company to update
            registration_number: The company's new registration number
            tax_id: The company's new tax ID
            siren: The company's new SIREN number (French companies)
            siret: The company's new SIRET number (French companies)
            ifu: The company's new IFU number
            idu: The company's new IDU number
            
        Returns:
            Company: The updated company
            
        Raises:
            CompanyNotFoundException: If the company is not found
            CompanyAlreadyExistsException: If a company with the given registration number already exists
        """
        # Get company
        company = self.company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundException(f"Company with ID {company_id} not found")
        
        # Check if registration number already exists
        if registration_number and registration_number != company.registration_number and self.company_repository.get_by_registration_number(registration_number):
            raise CompanyAlreadyExistsException(f"Company with registration number {registration_number} already exists")
        
        # Update company
        company.update_identifiers(
            registration_number=registration_number,
            tax_id=tax_id,
            siren=siren,
            siret=siret,
            ifu=ifu,
            idu=idu
        )
        
        # Save company
        return self.company_repository.save(company)
    
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
    
    def get_company_address_by_id(self, company_address_id) -> Optional[CompanyAddress]:
        """
        Get a company address by ID.
        
        Args:
            company_address_id: The ID of the company address to retrieve
            
        Returns:
            CompanyAddress: The company address with the given ID, or None if not found
        """
        return self.company_address_repository.get_by_id(company_address_id)
    
    def get_company_addresses(self, company_id) -> List[CompanyAddress]:
        """
        Get all addresses for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            List[CompanyAddress]: A list of company addresses for the company
        """
        return self.company_address_repository.get_by_company_id(company_id)
    
    def get_company_headquarters(self, company_id) -> Optional[CompanyAddress]:
        """
        Get the headquarters address for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            CompanyAddress: The headquarters address for the company, or None if not found
        """
        return self.company_address_repository.get_headquarters_by_company_id(company_id)
    
    def add_company_address(self, company_id, address_id, is_siege=False) -> CompanyAddress:
        """
        Add an address to a company.
        
        Args:
            company_id: The ID of the company
            address_id: The ID of the address
            is_siege: Whether this address is the company's headquarters
            
        Returns:
            CompanyAddress: The newly created company address
            
        Raises:
            CompanyNotFoundException: If the company is not found
        """
        # Check if company exists
        company = self.company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundException(f"Company with ID {company_id} not found")
        
        # Create new company address
        company_address = CompanyAddress(
            company_id=company_id,
            address_id=address_id,
            is_siege=is_siege
        )
        
        # Save company address
        return self.company_address_repository.save(company_address)
    
    def set_company_headquarters(self, company_address_id) -> CompanyAddress:
        """
        Set a company address as the company's headquarters.
        
        Args:
            company_address_id: The ID of the company address to set as headquarters
            
        Returns:
            CompanyAddress: The updated company address
            
        Raises:
            CompanyAddressNotFoundException: If the company address is not found
        """
        # Get company address
        company_address = self.company_address_repository.get_by_id(company_address_id)
        if not company_address:
            raise CompanyAddressNotFoundException(f"Company address with ID {company_address_id} not found")
        
        # Set as headquarters
        company_address.set_as_headquarters()
        
        # Save company address
        return self.company_address_repository.save(company_address)
    
    def unset_company_headquarters(self, company_address_id) -> CompanyAddress:
        """
        Unset a company address as the company's headquarters.
        
        Args:
            company_address_id: The ID of the company address to unset as headquarters
            
        Returns:
            CompanyAddress: The updated company address
            
        Raises:
            CompanyAddressNotFoundException: If the company address is not found
        """
        # Get company address
        company_address = self.company_address_repository.get_by_id(company_address_id)
        if not company_address:
            raise CompanyAddressNotFoundException(f"Company address with ID {company_address_id} not found")
        
        # Unset as headquarters
        company_address.unset_as_headquarters()
        
        # Save company address
        return self.company_address_repository.save(company_address)
    
    def delete_company_address(self, company_address_id) -> bool:
        """
        Delete a company address.
        
        Args:
            company_address_id: The ID of the company address to delete
            
        Returns:
            bool: True if the company address was deleted, False otherwise
        """
        return self.company_address_repository.delete(company_address_id)

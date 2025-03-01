"""
Repository interfaces for the company application.
This module contains the repository interfaces for the company application.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from builder.modules.company.domain.models import Company, CompanyAddress


class CompanyRepositoryInterface(ABC):
    """
    Interface for the company repository.
    
    This interface defines the contract that any company repository implementation must fulfill.
    It follows the Repository pattern, which abstracts the data access layer from the domain layer.
    """
    
    @abstractmethod
    def get_by_id(self, company_id) -> Optional[Company]:
        """
        Get a company by ID.
        
        Args:
            company_id: The ID of the company to retrieve
            
        Returns:
            Company: The company with the given ID, or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_denomination(self, denomination) -> Optional[Company]:
        """
        Get a company by denomination.
        
        Args:
            denomination: The denomination of the company to retrieve
            
        Returns:
            Company: The company with the given denomination, or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_registration_number(self, registration_number) -> Optional[Company]:
        """
        Get a company by registration number.
        
        Args:
            registration_number: The registration number of the company to retrieve
            
        Returns:
            Company: The company with the given registration number, or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_tax_id(self, tax_id) -> Optional[Company]:
        """
        Get a company by tax ID.
        
        Args:
            tax_id: The tax ID of the company to retrieve
            
        Returns:
            Company: The company with the given tax ID, or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_siren(self, siren) -> Optional[Company]:
        """
        Get a company by SIREN.
        
        Args:
            siren: The SIREN of the company to retrieve
            
        Returns:
            Company: The company with the given SIREN, or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_siret(self, siret) -> Optional[Company]:
        """
        Get a company by SIRET.
        
        Args:
            siret: The SIRET of the company to retrieve
            
        Returns:
            Company: The company with the given SIRET, or None if not found
        """
        pass
    
    @abstractmethod
    def save(self, company: Company) -> Company:
        """
        Save a company.
        
        This method creates a new company if the company doesn't have an ID,
        or updates an existing company if the company has an ID.
        
        Args:
            company: The company to save
            
        Returns:
            Company: The saved company with updated information (e.g., ID if it was a new company)
        """
        pass
    
    @abstractmethod
    def delete(self, company_id) -> bool:
        """
        Delete a company.
        
        Args:
            company_id: The ID of the company to delete
            
        Returns:
            bool: True if the company was deleted, False otherwise
        """
        pass


class CompanyAddressRepositoryInterface(ABC):
    """
    Interface for the company address repository.
    
    This interface defines the contract that any company address repository implementation must fulfill.
    It follows the Repository pattern, which abstracts the data access layer from the domain layer.
    """
    
    @abstractmethod
    def get_by_id(self, company_address_id) -> Optional[CompanyAddress]:
        """
        Get a company address by ID.
        
        Args:
            company_address_id: The ID of the company address to retrieve
            
        Returns:
            CompanyAddress: The company address with the given ID, or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_company_id(self, company_id) -> List[CompanyAddress]:
        """
        Get all addresses for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            List[CompanyAddress]: A list of company addresses for the company
        """
        pass
    
    @abstractmethod
    def get_headquarters_by_company_id(self, company_id) -> Optional[CompanyAddress]:
        """
        Get the headquarters address for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            CompanyAddress: The headquarters address for the company, or None if not found
        """
        pass
    
    @abstractmethod
    def save(self, company_address: CompanyAddress) -> CompanyAddress:
        """
        Save a company address.
        
        This method creates a new company address if the company address doesn't have an ID,
        or updates an existing company address if the company address has an ID.
        
        Args:
            company_address: The company address to save
            
        Returns:
            CompanyAddress: The saved company address with updated information
        """
        pass
    
    @abstractmethod
    def delete(self, company_address_id) -> bool:
        """
        Delete a company address.
        
        Args:
            company_address_id: The ID of the company address to delete
            
        Returns:
            bool: True if the company address was deleted, False otherwise
        """
        pass

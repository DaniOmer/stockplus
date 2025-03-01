"""
Repository implementations for the company application.
This module contains the repository implementations for the company application.
"""

from typing import List, Optional
from django.db import transaction

from builder.modules.company.domain.models import Company, CompanyAddress
from builder.modules.company.application.interfaces import (
    CompanyRepositoryInterface,
    CompanyAddressRepositoryInterface
)
from builder.models import Company as CompanyORM
from builder.models import CompanyAddress as CompanyAddressORM


class CompanyRepository(CompanyRepositoryInterface):
    """
    Implementation of the company repository interface using Django ORM.
    """
    
    def get_by_id(self, company_id) -> Optional[Company]:
        """
        Get a company by ID.
        
        Args:
            company_id: The ID of the company to retrieve
            
        Returns:
            Company: The company with the given ID, or None if not found
        """
        try:
            company_orm = CompanyORM.objects.get(id=company_id)
            return self._to_domain(company_orm)
        except CompanyORM.DoesNotExist:
            return None
    
    def get_by_denomination(self, denomination) -> Optional[Company]:
        """
        Get a company by denomination.
        
        Args:
            denomination: The denomination of the company to retrieve
            
        Returns:
            Company: The company with the given denomination, or None if not found
        """
        try:
            company_orm = CompanyORM.objects.get(denomination=denomination)
            return self._to_domain(company_orm)
        except CompanyORM.DoesNotExist:
            return None
    
    def get_by_registration_number(self, registration_number) -> Optional[Company]:
        """
        Get a company by registration number.
        
        Args:
            registration_number: The registration number of the company to retrieve
            
        Returns:
            Company: The company with the given registration number, or None if not found
        """
        try:
            company_orm = CompanyORM.objects.get(registration_number=registration_number)
            return self._to_domain(company_orm)
        except CompanyORM.DoesNotExist:
            return None
    
    def get_by_tax_id(self, tax_id) -> Optional[Company]:
        """
        Get a company by tax ID.
        
        Args:
            tax_id: The tax ID of the company to retrieve
            
        Returns:
            Company: The company with the given tax ID, or None if not found
        """
        try:
            company_orm = CompanyORM.objects.get(tax_id=tax_id)
            return self._to_domain(company_orm)
        except CompanyORM.DoesNotExist:
            return None
    
    def get_by_siren(self, siren) -> Optional[Company]:
        """
        Get a company by SIREN.
        
        Args:
            siren: The SIREN of the company to retrieve
            
        Returns:
            Company: The company with the given SIREN, or None if not found
        """
        try:
            company_orm = CompanyORM.objects.get(siren=siren)
            return self._to_domain(company_orm)
        except CompanyORM.DoesNotExist:
            return None
    
    def get_by_siret(self, siret) -> Optional[Company]:
        """
        Get a company by SIRET.
        
        Args:
            siret: The SIRET of the company to retrieve
            
        Returns:
            Company: The company with the given SIRET, or None if not found
        """
        try:
            company_orm = CompanyORM.objects.get(siret=siret)
            return self._to_domain(company_orm)
        except CompanyORM.DoesNotExist:
            return None
    
    @transaction.atomic
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
        if company.id:
            try:
                company_orm = CompanyORM.objects.get(id=company.id)
                # Update existing company
                company_orm.denomination = company.denomination
                company_orm.legal_form = company.legal_form
                company_orm.since = company.since
                company_orm.site = company.site
                company_orm.effective = company.effective
                company_orm.resume = company.resume
                company_orm.registration_number = company.registration_number
                company_orm.tax_id = company.tax_id
                company_orm.siren = company.siren
                company_orm.siret = company.siret
                company_orm.ifu = company.ifu
                company_orm.idu = company.idu
                company_orm.is_disable = not company.is_active
                company_orm.save()
            except CompanyORM.DoesNotExist:
                # Create new company with existing ID
                company_orm = CompanyORM(
                    id=company.id,
                    denomination=company.denomination,
                    legal_form=company.legal_form,
                    since=company.since,
                    site=company.site,
                    effective=company.effective,
                    resume=company.resume,
                    registration_number=company.registration_number,
                    tax_id=company.tax_id,
                    siren=company.siren,
                    siret=company.siret,
                    ifu=company.ifu,
                    idu=company.idu,
                    is_disable=not company.is_active
                )
                company_orm.save()
        else:
            # Create new company
            company_orm = CompanyORM(
                denomination=company.denomination,
                legal_form=company.legal_form,
                since=company.since,
                site=company.site,
                effective=company.effective,
                resume=company.resume,
                registration_number=company.registration_number,
                tax_id=company.tax_id,
                siren=company.siren,
                siret=company.siret,
                ifu=company.ifu,
                idu=company.idu,
                is_disable=not company.is_active
            )
            company_orm.save()
        
        return self._to_domain(company_orm)
    
    @transaction.atomic
    def delete(self, company_id) -> bool:
        """
        Delete a company.
        
        Args:
            company_id: The ID of the company to delete
            
        Returns:
            bool: True if the company was deleted, False otherwise
        """
        try:
            company_orm = CompanyORM.objects.get(id=company_id)
            company_orm.delete()
            return True
        except CompanyORM.DoesNotExist:
            return False
    
    def _to_domain(self, company_orm) -> Company:
        """
        Convert a Django ORM company to a domain company.
        
        Args:
            company_orm: The Django ORM company to convert
            
        Returns:
            Company: The domain company
        """
        return Company(
            id=company_orm.id,
            denomination=company_orm.denomination,
            legal_form=company_orm.legal_form,
            since=company_orm.since,
            site=company_orm.site,
            effective=company_orm.effective,
            resume=company_orm.resume,
            registration_number=company_orm.registration_number,
            tax_id=company_orm.tax_id,
            siren=company_orm.siren,
            siret=company_orm.siret,
            ifu=company_orm.ifu,
            idu=company_orm.idu,
            is_active=not company_orm.is_disable
        )


class CompanyAddressRepository(CompanyAddressRepositoryInterface):
    """
    Implementation of the company address repository interface using Django ORM.
    """
    
    def get_by_id(self, company_address_id) -> Optional[CompanyAddress]:
        """
        Get a company address by ID.
        
        Args:
            company_address_id: The ID of the company address to retrieve
            
        Returns:
            CompanyAddress: The company address with the given ID, or None if not found
        """
        try:
            company_address_orm = CompanyAddressORM.objects.get(id=company_address_id)
            return self._to_domain(company_address_orm)
        except CompanyAddressORM.DoesNotExist:
            return None
    
    def get_by_company_id(self, company_id) -> List[CompanyAddress]:
        """
        Get all addresses for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            List[CompanyAddress]: A list of company addresses for the company
        """
        company_addresses_orm = CompanyAddressORM.objects.filter(company_id=company_id)
        return [self._to_domain(company_address_orm) for company_address_orm in company_addresses_orm]
    
    def get_headquarters_by_company_id(self, company_id) -> Optional[CompanyAddress]:
        """
        Get the headquarters address for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            CompanyAddress: The headquarters address for the company, or None if not found
        """
        try:
            company_address_orm = CompanyAddressORM.objects.get(company_id=company_id, is_siege=True)
            return self._to_domain(company_address_orm)
        except CompanyAddressORM.DoesNotExist:
            return None
    
    @transaction.atomic
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
        if company_address.id:
            try:
                company_address_orm = CompanyAddressORM.objects.get(id=company_address.id)
                # Update existing company address
                company_address_orm.company_id = company_address.company_id
                company_address_orm.address_id = company_address.address_id
                company_address_orm.is_siege = company_address.is_siege
                company_address_orm.save()
            except CompanyAddressORM.DoesNotExist:
                # Create new company address with existing ID
                company_address_orm = CompanyAddressORM(
                    id=company_address.id,
                    company_id=company_address.company_id,
                    address_id=company_address.address_id,
                    is_siege=company_address.is_siege
                )
                company_address_orm.save()
        else:
            # Create new company address
            company_address_orm = CompanyAddressORM(
                company_id=company_address.company_id,
                address_id=company_address.address_id,
                is_siege=company_address.is_siege
            )
            company_address_orm.save()
        
        return self._to_domain(company_address_orm)
    
    @transaction.atomic
    def delete(self, company_address_id) -> bool:
        """
        Delete a company address.
        
        Args:
            company_address_id: The ID of the company address to delete
            
        Returns:
            bool: True if the company address was deleted, False otherwise
        """
        try:
            company_address_orm = CompanyAddressORM.objects.get(id=company_address_id)
            company_address_orm.delete()
            return True
        except CompanyAddressORM.DoesNotExist:
            return False
    
    def _to_domain(self, company_address_orm) -> CompanyAddress:
        """
        Convert a Django ORM company address to a domain company address.
        
        Args:
            company_address_orm: The Django ORM company address to convert
            
        Returns:
            CompanyAddress: The domain company address
        """
        return CompanyAddress(
            id=company_address_orm.id,
            company_id=company_address_orm.company_id,
            address_id=company_address_orm.address_id,
            is_siege=company_address_orm.is_siege
        )

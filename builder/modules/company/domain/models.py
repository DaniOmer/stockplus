"""
Domain models for the company application.
This module contains the domain models for the company application.
"""

from datetime import date
from typing import Optional, List


class Company:
    """
    Company domain model.
    
    This class represents a company in the system, with all its business rules and behaviors.
    It is independent of any framework or infrastructure concerns.
    """
    
    def __init__(self, id=None, denomination=None, legal_form=None, since=None,
                 site=None, effective=None, resume=None, registration_number=None,
                 tax_id=None, siren=None, siret=None, ifu=None, idu=None,
                 is_active=True):
        """
        Initialize a new Company instance.
        
        Args:
            id: The company's unique identifier
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
            is_active: Whether the company is active
        """
        self.id = id
        self.denomination = denomination
        self.legal_form = legal_form
        self.since = since
        self.site = site
        self.effective = effective
        self.resume = resume
        self.registration_number = registration_number
        self.tax_id = tax_id
        self.siren = siren
        self.siret = siret
        self.ifu = ifu
        self.idu = idu
        self.is_active = is_active
    
    def update_info(self, denomination=None, since=None, site=None,
                   effective=None, resume=None, legal_form=None):
        """
        Update the company's general information.
        
        Args:
            denomination: The company's new name
            since: The new date the company was founded
            site: The company's new website URL
            effective: The new number of employees
            resume: The new description of the company
            legal_form: The company's new legal form
        """
        if denomination is not None:
            self.denomination = denomination
        if since is not None:
            self.since = since
        if site is not None:
            self.site = site
        if effective is not None:
            self.effective = effective
        if resume is not None:
            self.resume = resume
        if legal_form is not None:
            self.legal_form = legal_form
    
    def update_identifiers(self, registration_number=None, tax_id=None,
                          siren=None, siret=None, ifu=None, idu=None):
        """
        Update the company's identifiers.
        
        Args:
            registration_number: The company's new registration number
            tax_id: The company's new tax ID
            siren: The company's new SIREN number (French companies)
            siret: The company's new SIRET number (French companies)
            ifu: The company's new IFU number
            idu: The company's new IDU number
        """
        if registration_number is not None:
            self.registration_number = registration_number
        if tax_id is not None:
            self.tax_id = tax_id
        if siren is not None:
            self.siren = siren
        if siret is not None:
            self.siret = siret
        if ifu is not None:
            self.ifu = ifu
        if idu is not None:
            self.idu = idu
    
    def activate(self):
        """
        Activate the company.
        """
        self.is_active = True
    
    def deactivate(self):
        """
        Deactivate the company.
        """
        self.is_active = False


class CompanyAddress:
    """
    Company address domain model.
    
    This class represents a company address in the system.
    """
    
    def __init__(self, id=None, company_id=None, address_id=None, is_siege=False):
        """
        Initialize a new CompanyAddress instance.
        
        Args:
            id: The company address's unique identifier
            company_id: The ID of the company
            address_id: The ID of the address
            is_siege: Whether this address is the company's headquarters
        """
        self.id = id
        self.company_id = company_id
        self.address_id = address_id
        self.is_siege = is_siege
    
    def set_as_headquarters(self):
        """
        Set this address as the company's headquarters.
        """
        self.is_siege = True
    
    def unset_as_headquarters(self):
        """
        Unset this address as the company's headquarters.
        """
        self.is_siege = False

"""
Repository implementations for the company domain.
"""

from typing import Optional, Dict, Any
from django.db import transaction
from stockplus.modules.company.domain.entities.company_entity import Company
from stockplus.modules.company.application.interfaces import ICompanyRepository
from stockplus.modules.company.infrastructure.models import Company as CompanyORM

class CompanyRepository(ICompanyRepository):
    """
    Django ORM implementation of the company repository.
    Implements CRUD operations for Company domain entities.
    """

    def get_by_id(self, company_id: int) -> Optional[Company]:
        return self._get_company_by(id=company_id)

    def get_by_denomination(self, denomination: str) -> Optional[Company]:
        return self._get_company_by(denomination=denomination)

    def get_by_registration_number(self, registration_number: str) -> Optional[Company]:
        return self._get_company_by(registration_number=registration_number)

    def get_by_tax_id(self, tax_id: str) -> Optional[Company]:
        return self._get_company_by(tax_id=tax_id)

    def get_by_siren(self, siren: str) -> Optional[Company]:
        return self._get_company_by(siren=siren)

    def get_by_siret(self, siret: str) -> Optional[Company]:
        return self._get_company_by(siret=siret)

    @transaction.atomic
    def save(self, company: Company) -> Company:
        company_data = self._create_orm_mapping(company)
        company_orm, _ = CompanyORM.objects.update_or_create(
            id=company.id or None,
            defaults=company_data
        )
        return self._to_domain(company_orm)

    @transaction.atomic
    def delete(self, company_id: int) -> bool:
        deleted, _ = CompanyORM.objects.filter(id=company_id).delete()
        return deleted > 0

    def _get_company_by(self, **kwargs: Any) -> Optional[Company]:
        try:
            return self._to_domain(CompanyORM.objects.get(**kwargs))
        except (CompanyORM.DoesNotExist, ValueError, TypeError):
            return None

    def _create_orm_mapping(self, company: Company) -> Dict[str, Any]:
        return {
            'denomination': company.denomination,
            'legal_form': company.legal_form,
            'since': company.since,
            'site': company.site,
            'effective': company.effective,
            'resume': company.resume,
            'registration_number': company.registration_number,
            'tax_id': company.tax_id,
            'siren': company.siren,
            'siret': company.siret,
            'ifu': company.ifu,
            'idu': company.idu,
            'is_disable': not company.is_active
        }

    def _to_domain(self, company_orm: CompanyORM) -> Company:
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
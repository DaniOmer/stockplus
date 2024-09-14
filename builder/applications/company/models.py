from django.db import models
from django.contrib.auth import get_user_model

from builder.applications.address import models as AddressModels
from builder.applications.company.apps import CompanyConfig
from builder.models.base import Base
from builder.fields import RichTextField

User = get_user_model()
class Company(Base):
    search_fields = ['denomination']
    denomination = models.CharField(max_length=255)
    since = models.DateField(null=True, blank=True)
    site = models.URLField(null=True, blank=True)
    effective = models.BigIntegerField(null=True, blank=True)
    resume = RichTextField(null=True, blank=True)

    legal_form = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    tax_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    siren = models.CharField(max_length=9, unique=True, null=True, blank=True)
    siret = models.CharField(max_length=14, unique=True, null=True, blank=True)
    ifu = models.CharField(max_length=100, unique=True, null=True, blank=True)
    idu = models.CharField(max_length=100, unique=True, null=True, blank=True)


    class Meta(Base.Meta):
        abstract = True

    def __str__(self):
        return self.denomination
    

class CompanyAddress(AddressModels.Address):
    company = models.ForeignKey(CompanyConfig.ForeignKey.company, on_delete=models.CASCADE, related_name='company_address')
    is_siege = models.BooleanField(default=False)

    class Meta:
        abstract = True
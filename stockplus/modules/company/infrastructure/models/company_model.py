from django.db import models

from stockplus.models.base import Base
from stockplus.fields import RichTextField

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

    class Meta:
        db_table = 'stockplus_company'

    def __str__(self):
        return self.denomination
    
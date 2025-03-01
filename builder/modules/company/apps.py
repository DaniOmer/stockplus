from django.apps import AppConfig


class Config:
    class ForeignKey:
        company = 'builder.Company'

class CompanyConfig(AppConfig, Config):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'builder.modules.company'

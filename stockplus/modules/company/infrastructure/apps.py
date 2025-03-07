from django.apps import AppConfig

class CompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stockplus.modules.company.infrastructure'
    label = 'company'

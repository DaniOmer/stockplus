from django.apps import AppConfig


class PointOfSaleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stockplus.modules.pointofsale.infrastructure'
    label = 'pointofsale'

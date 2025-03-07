from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stockplus.modules.shop.infrastructure'
    label = 'shop'

    def ready(self) -> None:
        from stockplus.modules.shop import signals
        return super().ready()
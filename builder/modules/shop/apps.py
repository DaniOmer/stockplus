from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'builder.modules.shop'

    def ready(self) -> None:
        from builder.modules.shop import signals
        return super().ready()
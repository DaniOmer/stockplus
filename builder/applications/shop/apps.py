from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'builder.applications.shop'

    def ready(self) -> None:
        from builder.applications.shop import signals
        return super().ready()
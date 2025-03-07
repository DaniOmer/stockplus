from django.apps import AppConfig

class SubscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stockplus.modules.subscription.infrastructure'
    label ='subscription'

    def ready(self) -> None:
        from stockplus.modules.subscription import signals
        return super().ready()

from django.apps import AppConfig

class Config:
    class ForeignKey:
        feature = 'builder.Feature'
        subscription_plan = 'builder.SubscriptionPlan'
        company = 'builder.Company'
        user = 'builder.User'

class SubscriptionConfig(AppConfig, Config):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'builder.applications.subscription'

    def ready(self) -> None:
        from builder.applications.subscription import signals
        return super().ready()

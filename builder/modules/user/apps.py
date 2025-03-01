from django.apps import AppConfig

class Config:
    cgu = True
    cgv = False
    protect_trashmail = True

    class ForeignKey:
        nationalities = 'builder.Nationality'
        address = 'builder.UserAddress'
        user = 'builder.User'
        company = 'builder.Company'

class UserConfig(AppConfig, Config):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'builder.modules.user'

    def ready(self) -> None:
        from builder.modules.user import signals
        return super().ready()
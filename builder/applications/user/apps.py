from django.apps import AppConfig

class Config:
    cgu = True
    cgv = False
    protect_trashmail = True

    class ForeignKey:
        nationalities = 'builder.Nationality'
        address = 'builder.UserAddress'

class UserConfig(AppConfig, Config):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'builder.applications.user'

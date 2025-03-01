from django.apps import AppConfig


class Config:
    class ForeignKey:
        user = 'builder.User'


class UserConfig(AppConfig, Config):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'builder.modules.user'

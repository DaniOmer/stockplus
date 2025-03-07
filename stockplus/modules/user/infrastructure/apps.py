from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stockplus.modules.user.infrastructure'
    label = 'user'

    def ready(self):
        from stockplus.modules.user.infrastructure import signals
        return super().ready()

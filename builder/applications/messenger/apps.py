from django.apps import AppConfig
from django.conf import settings

class Config():
    sender_name = settings.MESSENGER['sender_name'] if hasattr(settings, 'MESSENGER') else None
    sender_email = settings.MESSENGER['sender_email'] if hasattr(settings, 'MESSENGER') else None
    reply_name = settings.MESSENGER['reply_name'] if hasattr(settings, 'MESSENGER') else None
    reply_email = settings.MESSENGER['reply_email'] if hasattr(settings, 'MESSENGER') else None
    missive = 'builder.Missive'
    missive_backends = settings.MISSIVE_BACKENDS if hasattr(settings, 'MISSIVE_BACKENDS') else 'mighty.applications.messenger.backends'

class MessengerConfig(AppConfig, Config):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'builder.applications.messenger'

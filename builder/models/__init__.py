from django.conf import settings

if 'builder.applications.messenger' in settings.INSTALLED_APPS:
    from builder.applications.messenger import models as models_messenger
    class Missive(models_messenger.Missive): pass
    class Notification(models_messenger.Notification): pass
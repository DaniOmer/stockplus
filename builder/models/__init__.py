from django.conf import settings

if 'builder.applications.messenger' in settings.INSTALLED_APPS:
    from builder.applications.messenger import models as models_messenger
    class Missive(models_messenger.Missive): pass

if 'builder.applications.user' in settings.INSTALLED_APPS:
    from builder.applications.user import models as models_user
    class User(models_user.User): pass
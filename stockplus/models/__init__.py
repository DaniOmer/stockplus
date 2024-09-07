from django.conf import settings

if 'stockplus.applications.pointofsale' in settings.INSTALLED_APPS:
    from stockplus.applications.pointofsale import models as models_pointofsale
    class PointOfSale(models_pointofsale.PointOfSale): pass

if 'stockplus.applications.collaboration' in settings.INSTALLED_APPS:
    from stockplus.applications.collaboration import models as models_collaboration
    class Collaboration(models_collaboration.Collaboration): pass
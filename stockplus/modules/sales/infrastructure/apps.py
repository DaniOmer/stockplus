from django.apps import AppConfig


class SalesConfig(AppConfig):
    """
    Configuration for the sales module.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stockplus.modules.sales'
    verbose_name = 'Sales'
    
    def ready(self):
        """
        Import signals when the app is ready.
        """
        import stockplus.modules.sales.infrastructure.signals

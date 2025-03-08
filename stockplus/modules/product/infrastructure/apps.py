from django.apps import AppConfig

class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stockplus.modules.product.infrastructure'
    label = 'product'
    
    def ready(self):
        """
        Import signals when the app is ready.
        """
        import stockplus.modules.product.infrastructure.signals

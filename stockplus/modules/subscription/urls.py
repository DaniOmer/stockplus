from django.urls import path, include

# Import the URLs from the interfaces directory
from stockplus.modules.subscription.interfaces.urls import urlpatterns

# Re-export the urlpatterns
__all__ = ['urlpatterns']

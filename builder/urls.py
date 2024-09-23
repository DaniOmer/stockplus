"""stockplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include, re_path

urlpatterns = []

if 'django_ckeditor_5' in settings.INSTALLED_APPS:
    urlpatterns += [path("ckeditor5/", include('django_ckeditor_5.urls')),]
    
"""
SWAGGER UI configuration
"""
if 'drf_spectacular' in settings.INSTALLED_APPS and str(settings.ENV) == 'DEVELOPMENT':
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
    swagger_urlpatterns = [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
    urlpatterns += swagger_urlpatterns

# Enable app user
if "builder.applications.user" in settings.INSTALLED_APPS:
    from builder.applications.user import urls as urls_user
    urlpatterns += urls_user.urlpatterns

if "builder.applications.company" in settings.INSTALLED_APPS:
    from builder.applications.company import urls as urls_company
    urlpatterns += urls_company.urlpatterns

if "builder.applications.subscription" in settings.INSTALLED_APPS:
    from builder.applications.subscription import urls as urls_subscription
    urlpatterns += urls_subscription.urlpatterns

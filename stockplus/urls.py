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
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if 'stockplus.applications.pointofsale' in settings.INSTALLED_APPS:
    from stockplus.applications.pointofsale import urls as urls_pointofsale
    urlpatterns += urls_pointofsale.urlpatterns

if 'stockplus.applications.product' in settings.INSTALLED_APPS:
    from stockplus.applications.product import urls as urls_product
    urlpatterns += urls_product.urlpatterns
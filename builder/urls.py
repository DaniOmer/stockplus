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
from django.urls import path, include

urlpatterns = []

# Enable app user
if "builder.applications.user" in settings.INSTALLED_APPS:
    from builder.applications.user import urls as urls_user
    urlpatterns += urls_user.urlpatterns

if "builder.applications.company" in settings.INSTALLED_APPS:
    from builder.applications.company import urls as urls_company
    urlpatterns += urls_company.urlpatterns

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

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# CKEditor URLs
urlpatterns += [path("ckeditor5/", include('django_ckeditor_5.urls')),]
    
# Swagger UI configuration
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
swagger_urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
urlpatterns += swagger_urlpatterns

# Simple JWT configuration
from rest_framework_simplejwt.views import TokenRefreshView
from stockplus.views import CustomTokenObtainPairView
simplejwt_urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += simplejwt_urlpatterns

# User module URLs
from stockplus.modules.user.interfaces import urls as urls_user
urlpatterns += urls_user.urlpatterns

# Company configuration
from stockplus.modules.company.interfaces import urls as urls_company
urlpatterns += urls_company.urlpatterns

# Point of Sale URLs
from stockplus.modules.pointofsale.interfaces import urls as urls_pointofsale
urlpatterns += urls_pointofsale.urlpatterns

# Product URLs
from stockplus.modules.product.interfaces import urls as urls_product
urlpatterns += urls_product.urlpatterns

# Sales URLs
from stockplus.modules.sales.interfaces import urls as urls_sales
urlpatterns += urls_sales.urlpatterns

# Subscription configuration
from stockplus.modules.subscription import urls as urls_subscription
urlpatterns += urls_subscription.urlpatterns

# Shop URLs
from stockplus.modules.shop.interfaces import urls as urls_shop
urlpatterns += [
    path('api/shop/', include(urls_shop)),
]

# Collaborator URLs
from stockplus.modules.collaborator.interfaces import urls as urls_collaborator
urlpatterns += [
    path('api/collaborator/', include(urls_collaborator)),
]

# Reports URLs
from stockplus.modules.reports.interfaces import urls as urls_reports
urlpatterns += [
    path('api/reports/', include(urls_reports)),
]

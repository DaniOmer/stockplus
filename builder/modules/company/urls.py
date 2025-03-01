"""
URL configuration for the company application.
This module contains the URL patterns for the company application.
"""

from django.urls import path

from builder.modules.company.interfaces.views.company import (
    CompanyCreateView,
    CompanyDetailView,
    CompanyActivateView,
    CompanyDeactivateView
)
from builder.modules.company.interfaces.views.address import (
    CompanyAddressListCreateView,
    CompanyAddressDetailView,
    CompanyHeadquartersView
)


urlpatterns = [
    # Company URLs
    path('api/company/', CompanyCreateView.as_view(), name='company-create'),
    path('api/company/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('api/company/<int:pk>/activate/', CompanyActivateView.as_view(), name='company-activate'),
    path('api/company/<int:pk>/deactivate/', CompanyDeactivateView.as_view(), name='company-deactivate'),
    
    # Company address URLs
    path('api/<int:company_id>/addresses/', CompanyAddressListCreateView.as_view(), name='company-address-list'),
    path('api/addresses/<int:pk>/', CompanyAddressDetailView.as_view(), name='company-address-detail'),
    path('api/company/<int:company_id>/headquarters/', CompanyHeadquartersView.as_view(), name='company-headquarters'),
]

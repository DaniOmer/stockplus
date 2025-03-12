"""
URL configuration for the company application.
This module contains the URL patterns for the company application.
"""

from django.urls import path

from stockplus.modules.company.interfaces.views.company import (
    CompanyCreateView,
    CompanyDetailView,
    CompanyActivateView,
    CompanyDeactivateView
)

urlpatterns = [
    # Company URLs
    path('api/companies/', CompanyCreateView.as_view(), name='company-create'),
    path('api/companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('api/companies/<int:pk>/activate/', CompanyActivateView.as_view(), name='company-activate'),
    path('api/companies/<int:pk>/deactivate/', CompanyDeactivateView.as_view(), name='company-deactivate'),
]

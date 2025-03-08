"""
Reports app configuration.
This module contains the Django app configuration for the reports module.
"""

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """
    Django app configuration for the reports module.
    """
    name = 'stockplus.modules.reports'
    verbose_name = 'Reports'

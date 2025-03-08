"""
Collaborator app configuration.
This module contains the Django app configuration for the collaborator module.
"""

from django.apps import AppConfig


class CollaboratorConfig(AppConfig):
    """
    Django app configuration for the collaborator module.
    """
    name = 'stockplus.modules.collaborator'
    verbose_name = 'Collaborator'

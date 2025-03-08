"""
Collaborator URLs configuration.
"""

from django.urls import path

from stockplus.modules.collaborator.interfaces.views import (
    CollaboratorListCreateView,
    CollaboratorDetailView,
    CollaboratorRoleListCreateView,
    CollaboratorRoleDetailView,
    CollaboratorPermissionListView,
)

urlpatterns = [
    # Collaborator URLs
    path('collaborators/', CollaboratorListCreateView.as_view(), name='collaborator-list-create'),
    path('collaborators/<int:pk>/', CollaboratorDetailView.as_view(), name='collaborator-detail'),
    
    # Role URLs
    path('roles/', CollaboratorRoleListCreateView.as_view(), name='collaborator-role-list-create'),
    path('roles/<int:pk>/', CollaboratorRoleDetailView.as_view(), name='collaborator-role-detail'),
    
    # Permission URLs
    path('permissions/', CollaboratorPermissionListView.as_view(), name='collaborator-permission-list'),
]

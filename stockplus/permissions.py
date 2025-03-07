from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

class IsCollaborator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Collaborator').exists()


from django.conf import settings

from importlib import import_module

from django.conf import settings
from rest_framework.permissions import IsAuthenticated

AdditionalCrudPermissions = getattr(settings, 'ADDITIONAL_CRUD_PERMISSIONS', [])
extra_permissions = []

for perm in AdditionalCrudPermissions:
    try:
        module_path, class_name = perm.rsplit('.', 1)
        module = import_module(module_path)
        permission_class = getattr(module, class_name)
        extra_permissions.append(permission_class)
    except (ImportError, AttributeError) as e:
        print(f"Something went wrong when trying to get {perm}: {e}")

base_permissions = [IsAuthenticated,] + extra_permissions
from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

class IsCollaborator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Collaborator').exists()


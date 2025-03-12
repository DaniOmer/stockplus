from rest_framework.permissions import BasePermission

class IsCollaborator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Collaborator').exists()

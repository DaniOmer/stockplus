from rest_framework.permissions import BasePermission

class RoleBasedAccess(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        allowed_groups = getattr(view, 'allowed_groups', [])
        
        if user.is_authenticated and allowed_groups:
            user_groups = user.groups.values_list('name', flat=True)
            return any(group in allowed_groups for group in user_groups)
        return False


from rest_framework.permissions import BasePermission

from builder.models import User

class IsSelf(BasePermission):
    """
    Custom permission to only allow users to access their own data.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the object is a User or a related resource with a user attribute
        if isinstance(obj, User):
            return obj == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False

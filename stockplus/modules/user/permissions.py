from rest_framework.permissions import BasePermission

from stockplus.modules.user.infrastructure.models import User
from stockplus.modules.company.infrastructure.models import Company

import logging
logger = logging.getLogger(__name__)

class IsSelf(BasePermission):
    """
    Custom permission to only allow users to access their own data.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the object is a User or a related resource with a user attribute
        if isinstance(obj, User):
            return obj == request.user
        if isinstance(obj, Company):
            return obj == request.user.company
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        logger.warning(f"Permission denied for {request.user} on object {obj}")
        return False
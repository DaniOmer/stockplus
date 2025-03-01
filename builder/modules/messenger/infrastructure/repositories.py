"""
Repositories for the messenger application.
"""
import logging
from typing import Optional, Dict, Any, List

from builder.models import Missive
from builder.modules.messenger.application.interfaces import MissiveRepositoryInterface
from builder.modules.messenger import choices

logger = logging.getLogger(__name__)


class MissiveRepository(MissiveRepositoryInterface):
    """Repository for missive operations."""
    
    def create_email_missive(self, target: str, subject: str, message: str, 
                            html_message: Optional[str] = None, **kwargs) -> Any:
        """
        Create an email missive.
        
        Args:
            target: The recipient's email address
            subject: The email subject
            message: The email message (plain text)
            html_message: The email message (HTML)
            **kwargs: Additional parameters for the missive
            
        Returns:
            The created missive object
        """
        data = {
            "content_type": kwargs.get("content_type", None),
            "object_id": kwargs.get("object_id", None),
            "subject": subject,
            "html": html_message or message,
            "txt": message,
            "target": target,
            "mode": "EMAIL",
            "template": kwargs.get("template", None)
        }
        
        # Add any additional parameters
        for key, value in kwargs.items():
            if key not in data:
                data[key] = value
        
        missive = Missive(**data)
        missive.save()
        
        return missive
    
    def create_sms_missive(self, target: str, message: str, **kwargs) -> Any:
        """
        Create an SMS missive.
        
        Args:
            target: The recipient's phone number
            message: The SMS message
            **kwargs: Additional parameters for the missive
            
        Returns:
            The created missive object
        """
        data = {
            "content_type": kwargs.get("content_type", None),
            "object_id": kwargs.get("object_id", None),
            "subject": kwargs.get("subject", "SMS Message"),
            "html": "not used for sms",
            "txt": message,
            "target": target,
            "mode": "SMS",
            "template": kwargs.get("template", None)
        }
        
        # Add any additional parameters
        for key, value in kwargs.items():
            if key not in data:
                data[key] = value
        
        missive = Missive(**data)
        missive.save()
        
        return missive
    
    def get_missive_by_id(self, missive_id: int) -> Any:
        """
        Get a missive by ID.
        
        Args:
            missive_id: The ID of the missive
            
        Returns:
            The missive object
        """
        return Missive.objects.get(id=missive_id)
    
    def update_missive_status(self, missive_id: int, status: str) -> Any:
        """
        Update a missive's status.
        
        Args:
            missive_id: The ID of the missive
            status: The new status
            
        Returns:
            The updated missive object
        """
        missive = self.get_missive_by_id(missive_id)
        missive.status = status
        missive.save()
        return missive
    
    def list_missives(self, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        List missives with optional filters.
        
        Args:
            filters: Optional filters for the missives
            
        Returns:
            A list of missive objects
        """
        queryset = Missive.objects.all()
        
        if filters:
            queryset = queryset.filter(**filters)
            
        return list(queryset)

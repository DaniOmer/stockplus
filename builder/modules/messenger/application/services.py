"""
Services for the messenger application.
"""
import logging
from typing import Optional, Dict, Any, List

from builder.modules.messenger.application.interfaces import MissiveRepositoryInterface
from builder.modules.messenger.domain.exceptions import MissiveDeliveryException

logger = logging.getLogger(__name__)


class MessengerService:
    """Service for handling messenger operations."""
    
    def __init__(self, missive_repository: MissiveRepositoryInterface):
        self.missive_repository = missive_repository
    
    def send_email(self, to_email: str, subject: str, message: str, 
                  html_message: Optional[str] = None, **kwargs) -> Any:
        """
        Send an email.
        
        Args:
            to_email: The recipient's email address
            subject: The email subject
            message: The email message (plain text)
            html_message: The email message (HTML)
            **kwargs: Additional parameters for the missive
            
        Returns:
            The created missive object
            
        Raises:
            MissiveDeliveryException: If the email could not be sent
        """
        try:
            missive = self.missive_repository.create_email_missive(
                target=to_email,
                subject=subject,
                message=message,
                html_message=html_message or message,
                **kwargs
            )
            logger.info(f"Email missive created for {to_email}")
            return missive
        except Exception as e:
            logger.error(f"Failed to create email missive for {to_email}: {str(e)}")
            raise MissiveDeliveryException(f"Failed to send email: {str(e)}")
    
    def send_sms(self, to_phone: str, message: str, **kwargs) -> Any:
        """
        Send an SMS.
        
        Args:
            to_phone: The recipient's phone number
            message: The SMS message
            **kwargs: Additional parameters for the missive
            
        Returns:
            The created missive object
            
        Raises:
            MissiveDeliveryException: If the SMS could not be sent
        """
        try:
            missive = self.missive_repository.create_sms_missive(
                target=to_phone,
                message=message,
                **kwargs
            )
            logger.info(f"SMS missive created for {to_phone}")
            return missive
        except Exception as e:
            logger.error(f"Failed to create SMS missive for {to_phone}: {str(e)}")
            raise MissiveDeliveryException(f"Failed to send SMS: {str(e)}")
    
    def get_missive(self, missive_id: int) -> Any:
        """
        Get a missive by ID.
        
        Args:
            missive_id: The ID of the missive
            
        Returns:
            The missive object
        """
        return self.missive_repository.get_missive_by_id(missive_id)
    
    def update_missive_status(self, missive_id: int, status: str) -> Any:
        """
        Update a missive's status.
        
        Args:
            missive_id: The ID of the missive
            status: The new status
            
        Returns:
            The updated missive object
        """
        return self.missive_repository.update_missive_status(missive_id, status)
    
    def list_missives(self, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        List missives with optional filters.
        
        Args:
            filters: Optional filters for the missives
            
        Returns:
            A list of missive objects
        """
        return self.missive_repository.list_missives(filters)

"""
Application services for the messenger application.
This module contains the application services for the messenger application.
"""

import logging
from typing import List, Optional, Dict, Any

from stockplus.modules.messenger.domain.entities import Missive
from stockplus.modules.messenger.domain.exceptions import (
    MissiveNotFoundException,
    InvalidMissiveStatusException,
)
from stockplus.modules.messenger.application.interfaces import  MissiveRepositoryInterface
from stockplus.modules.messenger import choices

logger = logging.getLogger(__name__)


class MessengerService:
    """
    Messenger service.

    This class implements the application logic for the messenger module. It uses the missive repository
    to access and manipulate missive data and enforces business rules.
    """

    def __init__(self, missive_repository: MissiveRepositoryInterface):
        """
        Initialize a new MessengerService instance.

        Args:
            missive_repository: The missive repository to use
        """
        self.missive_repository = missive_repository

    def get_missive_by_id(self, missive_id) -> Optional[Missive]:
        """
        Get a missive by ID.

        Args:
            missive_id: The ID of the missive to retrieve

        Returns:
            Missive: The missive with the given ID or None if not found
        """
        return self.missive_repository.get_by_id(missive_id)

    def get_missives_by_status(self, status) -> List[Missive]:
        """
        Get all missives with a given status.

        Args:
            status: The status to filter by

        Returns:
            List[Missive]: A list of missives with the given status
        """
        return self.missive_repository.get_by_status(status)

    def get_missives_by_mode(self, mode) -> List[Missive]:
        """
        Get all missives with a given mode.

        Args:
            mode: The mode to filter by (EMAIL, SMS, etc.)

        Returns:
            List[Missive]: A list of missives with the given mode
        """
        return self.missive_repository.get_by_mode(mode)

    def get_missives_by_target(self, target) -> List[Missive]:
        """
        Get all missives for a given target.

        Args:
            target: The target (email, phone number, etc.)

        Returns:
            List[Missive]: A list of missives for the given target
        """
        return self.missive_repository.get_by_target(target)

    def create_email_missive(self, to_email, subject, message, html_message=None, **kwargs) -> Missive:
        """
        Create a new email missive.

        Args:
            to_email: The recipient's email address
            subject: The email subject
            message: The email message (plain text)
            html_message: The email message (HTML)
            **kwargs: Additional missive data

        Returns:
            Missive: The created missive
        """
        data = {
            "mode": choices.MODE_EMAIL,
            "status": choices.STATUS_PREPARE,
            "target": to_email,
            "subject": subject,
            "txt": message,
            "html": html_message or message,
            **kwargs
        }
        
        missive = Missive(**data)
        return self.missive_repository.save(missive)

    def create_sms_missive(self, to_phone, message, **kwargs) -> Missive:
        """
        Create a new SMS missive.

        Args:
            to_phone: The recipient's phone number
            message: The SMS message
            **kwargs: Additional missive data

        Returns:
            Missive: The created missive
        """
        data = {
            "mode": choices.MODE_SMS,
            "status": choices.STATUS_PREPARE,
            "target": to_phone,
            "subject": "SMS Message",
            "txt": message,
            "html": "not used for sms",
            **kwargs
        }
        
        missive = Missive(**data)
        return self.missive_repository.save(missive)

    def send_missive(self, missive_id) -> bool:
        """
        Send a missive.

        Args:
            missive_id: The ID of the missive to send

        Returns:
            bool: True if the missive was sent successfully, False otherwise

        Raises:
            MissiveNotFoundException: If the missive is not found
            InvalidMissiveStatusException: If the missive is not in the PREPARE status
        """
        missive = self.missive_repository.get_by_id(missive_id)
        if not missive:
            raise MissiveNotFoundException(f"Missive with ID {missive_id} not found")
        
        if missive.status != choices.STATUS_PREPARE:
            raise InvalidMissiveStatusException(f"Missive with ID {missive_id} is not in PREPARE status")
        
        try:
            backend = missive.get_backend()
            
            if missive.mode == choices.MODE_EMAIL:
                success = backend.send_email(missive)
            elif missive.mode == choices.MODE_SMS:
                success = backend.send_sms(missive)
            else:
                logger.error(f"Unsupported missive mode: {missive.mode}")
                missive.to_error()
                self.missive_repository.save(missive)
                return False
            
            if success:
                missive.to_sent()
            else:
                missive.to_error()
            
            self.missive_repository.save(missive)
            return success
        except Exception as e:
            logger.error(f"Error sending missive: {str(e)}")
            missive.to_error()
            missive.trace = str(e)
            self.missive_repository.save(missive)
            return False

    def check_missive_status(self, missive_id) -> Dict[str, Any]:
        """
        Check the status of a missive.

        Args:
            missive_id: The ID of the missive to check

        Returns:
            Dict[str, Any]: The status information

        Raises:
            MissiveNotFoundException: If the missive is not found
        """
        missive = self.missive_repository.get_by_id(missive_id)
        if not missive:
            raise MissiveNotFoundException(f"Missive with ID {missive_id} not found")
        
        try:
            return missive.check_status()
        except Exception as e:
            logger.error(f"Error checking missive status: {str(e)}")
            return {
                "status": "ERROR",
                "error": str(e)
            }

    def delete_missive(self, missive_id) -> bool:
        """
        Delete a missive.

        Args:
            missive_id: The ID of the missive to delete

        Returns:
            bool: True if the missive was deleted, False otherwise
        """
        return self.missive_repository.delete(missive_id)

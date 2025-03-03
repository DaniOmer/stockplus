"""
Application interfaces for the messenger application.
This module contains the application interfaces for the messenger application.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class MissiveRepositoryInterface(ABC):
    """
    Missive repository interface.

    This interface defines the methods that a missive repository must implement.
    """

    @abstractmethod
    def get_by_id(self, missive_id):
        """
        Get a missive by ID.

        Args:
            missive_id: The ID of the missive to retrieve

        Returns:
            Missive: The missive with the given ID or None if not found
        """
        pass

    @abstractmethod
    def get_by_status(self, status):
        """
        Get all missives with a given status.

        Args:
            status: The status to filter by

        Returns:
            List[Missive]: A list of missives with the given status
        """
        pass

    @abstractmethod
    def get_by_mode(self, mode):
        """
        Get all missives with a given mode.

        Args:
            mode: The mode to filter by (EMAIL, SMS, etc.)

        Returns:
            List[Missive]: A list of missives with the given mode
        """
        pass

    @abstractmethod
    def get_by_target(self, target):
        """
        Get all missives for a given target.

        Args:
            target: The target (email, phone number, etc.)

        Returns:
            List[Missive]: A list of missives for the given target
        """
        pass

    @abstractmethod
    def save(self, missive):
        """
        Save a missive.

        Args:
            missive: The missive to save

        Returns:
            Missive: The saved missive
        """
        pass

    @abstractmethod
    def delete(self, missive_id):
        """
        Delete a missive.

        Args:
            missive_id: The ID of the missive to delete

        Returns:
            bool: True if the missive was deleted, False otherwise
        """
        pass


class MessengerBackendInterface(ABC):
    """
    Messenger backend interface.

    This interface defines the methods that a messenger backend must implement.
    """

    @abstractmethod
    def send_email(self, missive):
        """
        Send an email.

        Args:
            missive: The missive to send

        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        pass

    @abstractmethod
    def send_sms(self, missive):
        """
        Send an SMS.

        Args:
            missive: The missive to send

        Returns:
            bool: True if the SMS was sent successfully, False otherwise
        """
        pass

    @abstractmethod
    def check_email(self, missive):
        """
        Check the status of an email.

        Args:
            missive: The missive to check

        Returns:
            Dict[str, Any]: The status information
        """
        pass

    @abstractmethod
    def check_sms(self, missive):
        """
        Check the status of an SMS.

        Args:
            missive: The missive to check

        Returns:
            Dict[str, Any]: The status information
        """
        pass

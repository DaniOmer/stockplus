"""
Repositories for the messenger application.
This module contains the repositories for the messenger application.
"""

from typing import List

from stockplus.modules.messenger.application.interfaces import MissiveRepositoryInterface
from stockplus.modules.messenger.infrastructure.models import Missive

class MissiveRepository(MissiveRepositoryInterface):
    """
    Missive repository implementation.

    This class implements the MissiveRepositoryInterface using Django ORM.
    """

    def get_by_id(self, missive_id):
        """
        Get a missive by ID.

        Args:
            missive_id: The ID of the missive to retrieve

        Returns:
            Missive: The missive with the given ID or None if not found
        """
        try:
            return Missive.objects.get(id=missive_id)
        except Missive.DoesNotExist:
            return None

    def get_by_status(self, status) -> List[Missive]:
        """
        Get all missives with a given status.

        Args:
            status: The status to filter by

        Returns:
            List[Missive]: A list of missives with the given status
        """
        return list(Missive.objects.filter(status=status))

    def get_by_mode(self, mode) -> List[Missive]:
        """
        Get all missives with a given mode.

        Args:
            mode: The mode to filter by (EMAIL, SMS, etc.)

        Returns:
            List[Missive]: A list of missives with the given mode
        """
        return list(Missive.objects.filter(mode=mode))

    def get_by_target(self, target) -> List[Missive]:
        """
        Get all missives for a given target.

        Args:
            target: The target (email, phone number, etc.)

        Returns:
            List[Missive]: A list of missives for the given target
        """
        return list(Missive.objects.filter(target=target))

    def save(self, missive) -> Missive:
        """
        Save a missive.

        Args:
            missive: The missive to save

        Returns:
            Missive: The saved missive
        """
        created_missive = Missive.objects.create(**missive.to_json())
        created_missive.save()
        return created_missive

    def delete(self, missive_id) -> bool:
        """
        Delete a missive.

        Args:
            missive_id: The ID of the missive to delete

        Returns:
            bool: True if the missive was deleted, False otherwise
        """
        try:
            missive = Missive.objects.get(id=missive_id)
            missive.delete()
            return True
        except Missive.DoesNotExist:
            return False

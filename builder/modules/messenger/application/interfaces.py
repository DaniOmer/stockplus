"""
Interfaces for the messenger application.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class MissiveRepositoryInterface(ABC):
    """Interface for missive repository."""
    
    @abstractmethod
    def create_email_missive(self, target: str, subject: str, message: str, 
                            html_message: Optional[str] = None, **kwargs) -> Any:
        """Create an email missive."""
        pass
    
    @abstractmethod
    def create_sms_missive(self, target: str, message: str, **kwargs) -> Any:
        """Create an SMS missive."""
        pass
    
    @abstractmethod
    def get_missive_by_id(self, missive_id: int) -> Any:
        """Get a missive by ID."""
        pass
    
    @abstractmethod
    def update_missive_status(self, missive_id: int, status: str) -> Any:
        """Update a missive's status."""
        pass
    
    @abstractmethod
    def list_missives(self, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        """List missives with optional filters."""
        pass


class BackendInterface(ABC):
    """Interface for message backends."""
    
    @abstractmethod
    def send_email(self, missive: Any) -> bool:
        """Send an email using the backend."""
        pass
    
    @abstractmethod
    def send_sms(self, missive: Any) -> bool:
        """Send an SMS using the backend."""
        pass
    
    @abstractmethod
    def check_email(self, missive: Any) -> str:
        """Check the status of an email."""
        pass
    
    @abstractmethod
    def check_sms(self, missive: Any) -> str:
        """Check the status of an SMS."""
        pass

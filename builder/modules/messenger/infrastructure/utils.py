"""
Utility functions for the messenger application.
This module provides utility functions for sending emails and SMS using the messenger service.
"""

import logging
from builder.modules.messenger.application.services import MessengerService
from builder.modules.messenger.infrastructure.repositories.missive_repository import MissiveRepository

logger = logging.getLogger(__name__)


def send_mail_message(to_email, subject, message, html_message=None):
    """
    Send an email using the messenger service.

    Args:
        to_email: The recipient's email address
        subject: The email subject
        message: The email message (plain text)
        html_message: The email message (HTML)

    Returns:
        object: The created missive object
    """
    try:
        # Create messenger service
        messenger_service = MessengerService(
            missive_repository=MissiveRepository()
        )
        
        # Create email missive
        missive = messenger_service.create_email_missive(
            to_email=to_email,
            subject=subject,
            message=message,
            html_message=html_message
        )
        
        # Send the missive
        success = messenger_service.send_missive(missive.id)
        
        if success:
            logger.info(f"Email sent to {to_email}")
        else:
            logger.error(f"Failed to send email to {to_email}")
        
        return missive
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return None


def send_sms_message(to_phone, message):
    """
    Send an SMS using the messenger service.

    Args:
        to_phone: The recipient's phone number
        message: The SMS message

    Returns:
        object: The created missive object
    """
    try:
        # Create messenger service
        messenger_service = MessengerService(
            missive_repository=MissiveRepository()
        )
        
        # Create SMS missive
        missive = messenger_service.create_sms_missive(
            to_phone=to_phone,
            message=message
        )
        
        # Send the missive
        success = messenger_service.send_missive(missive.id)
        
        if success:
            logger.info(f"SMS sent to {to_phone}")
        else:
            logger.error(f"Failed to send SMS to {to_phone}")
        
        return missive
    except Exception as e:
        logger.error(f"Failed to send SMS to {to_phone}: {str(e)}")
        return None

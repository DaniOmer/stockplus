"""
Utility functions for the messenger application.
This module provides utility functions for sending emails and SMS using the missive model.
"""

import logging
from builder.models import Missive

logger = logging.getLogger(__name__)


def send_mail_message(to_email, subject, message, html_message=None):
    """
    Send an email using the missive model.

    Args:
        to_email: The recipient's email address
        subject: The email subject
        message: The email message (plain text)
        html_message: The email message (HTML)

    Returns:
        object: The created missive object
    """
    try:
        data = {
            "content_type": None,
            "object_id": None,
            "subject": subject,
            "html": html_message or message,
            "txt": message,
            "target": to_email,
            "mode": "EMAIL"
        }
        
        missive = Missive(**data)
        missive.save()
        
        logger.info(f"Email missive created for {to_email}")
        return missive
    except Exception as e:
        logger.error(f"Failed to create email missive for {to_email}: {str(e)}")
        return None


def send_sms_message(to_phone, message):
    """
    Send an SMS using the missive model.

    Args:
        to_phone: The recipient's phone number
        message: The SMS message

    Returns:
        object: The created missive object
    """
    try:
        data = {
            "content_type": None,
            "object_id": None,
            "subject": "SMS Message",
            "html": "not used for sms",
            "txt": message,
            "target": to_phone,
            "mode": "SMS"
        }
        
        missive = Missive(**data)
        missive.save()
        
        logger.info(f"SMS missive created for {to_phone}")
        return missive
    except Exception as e:
        logger.error(f"Failed to create SMS missive for {to_phone}: {str(e)}")
        return None

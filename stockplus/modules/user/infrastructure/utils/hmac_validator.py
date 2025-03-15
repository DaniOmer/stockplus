"""
HMAC signature validation utilities for the user module.
This module contains utilities for validating HMAC signatures for secure file uploads.
"""

import hmac
import hashlib
import time
import base64
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class HMACValidator:
    """
    Utility class for validating HMAC signatures for secure file uploads.
    """
    
    @staticmethod
    def generate_signature(user_id, timestamp=None):
        """
        Generate an HMAC signature for a user.
        
        Args:
            user_id: The ID of the user
            timestamp: The timestamp to use (defaults to current time)
            
        Returns:
            dict: A dictionary containing the signature and timestamp
        """
        if timestamp is None:
            timestamp = int(time.time())
        
        # Create the message to sign
        message = f"{user_id}:{timestamp}".encode('utf-8')
        
        # Create the signature
        signature = hmac.new(
            settings.SECRET_KEY.encode('utf-8'),
            message,
            hashlib.sha256
        ).digest()
        
        # Encode the signature as base64
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        
        return {
            'signature': signature_b64,
            'timestamp': timestamp
        }
    
    @staticmethod
    def validate_signature(user_id, signature, timestamp, max_age=300):
        """
        Validate an HMAC signature.
        
        Args:
            user_id: The ID of the user
            signature: The signature to validate
            timestamp: The timestamp used to generate the signature
            max_age: The maximum age of the signature in seconds (default: 5 minutes)
            
        Returns:
            bool: True if the signature is valid, False otherwise
        """
        try:
            # Check if the timestamp is too old
            current_time = int(time.time())
            if current_time - int(timestamp) > max_age:
                logger.warning(f"Signature expired for user {user_id}")
                return False
            
            # Create the message that was signed
            message = f"{user_id}:{timestamp}".encode('utf-8')
            
            # Create the expected signature
            expected_signature = hmac.new(
                settings.SECRET_KEY.encode('utf-8'),
                message,
                hashlib.sha256
            ).digest()
            
            # Decode the provided signature
            try:
                provided_signature = base64.b64decode(signature)
            except Exception as e:
                logger.warning(f"Invalid signature format for user {user_id}: {str(e)}")
                return False
            
            # Compare the signatures using a constant-time comparison
            return hmac.compare_digest(expected_signature, provided_signature)
        
        except Exception as e:
            logger.error(f"Error validating signature for user {user_id}: {str(e)}")
            return False

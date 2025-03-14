"""
Token model for the user application.
This module contains the token model for the user application.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone

from stockplus.models.base import Base

class Token(Base):
    """
    Token model.
    
    This model represents a token used for various purposes such as
    email verification, password reset, and invitation.
    """
    
    # Token types
    TYPE_VERIFICATION = 'verification'
    TYPE_PASSWORD_RESET = 'password_reset'
    TYPE_INVITATION = 'invitation'
    
    TYPE_CHOICES = [
        (TYPE_VERIFICATION, 'Verification'),
        (TYPE_PASSWORD_RESET, 'Password Reset'),
        (TYPE_INVITATION, 'Invitation'),
    ]
    
    # Token methods
    METHOD_EMAIL = 'email'
    METHOD_SMS = 'sms'
    
    METHOD_CHOICES = [
        (METHOD_EMAIL, 'Email'),
        (METHOD_SMS, 'SMS'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tokens',
        null=True,
        blank=True
    )
    token_value = models.CharField(max_length=255, unique=True)
    token_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default=METHOD_EMAIL)
    expiry = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)  # For invitation tokens
    
    class Meta:
        db_table = 'stockplus_token'
        verbose_name = 'token'
        verbose_name_plural = 'tokens'
        indexes = [
            models.Index(fields=['token_value']),
            models.Index(fields=['token_type']),
            models.Index(fields=['user']),
        ]
    
    def is_expired(self):
        """
        Check if the token has expired.
        
        Returns:
            bool: True if the token has expired, False otherwise
        """
        return self.expiry < timezone.now()
    
    def is_valid(self):
        """
        Check if the token is valid.
        
        Returns:
            bool: True if the token is valid, False otherwise
        """
        return not self.is_used and not self.is_expired()
    
    def use(self):
        """
        Mark the token as used.
        """
        self.is_used = True
        self.save()

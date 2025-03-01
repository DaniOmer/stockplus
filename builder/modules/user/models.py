"""
Django models for the user application.
This module contains the Django models for the user application.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from builder.models.base import Base
from builder.modules.user.apps import UserConfig


class UserManager(BaseUserManager):
    """
    Custom user manager for the User model.
    """

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        """
        Create and save a user with the given email, phone number, and password.
        """
        if not email and not phone_number:
            raise ValueError('The Email or Phone Number field must be set')
        
        if email:
            email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            phone_number=phone_number,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        """
        Create and save a superuser with the given email, phone number, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, phone_number, password, **extra_fields)


class User(AbstractUser, Base):
    """
    Custom user model for the application.
    """
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        help_text=_('Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_('Designates whether this user has verified their account.'),
    )
    company = models.ForeignKey(
        'builder.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
    )
    role = models.CharField(
        _('role'),
        max_length=20,
        null=True,
        blank=True,
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        abstract = True
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        if self.email:
            return self.email
        if self.phone_number:
            return self.phone_number
        return self.username or str(self.id)
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    
    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name


class UserAddress(Base):
    """
    User address model.
    """
    user = models.ForeignKey(
        UserConfig.ForeignKey.user,
        on_delete=models.CASCADE,
        related_name='addresses',
    )
    address = models.CharField(_('address'), max_length=255)
    city = models.CharField(_('city'), max_length=100)
    state = models.CharField(_('state'), max_length=100, null=True, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20)
    country = models.CharField(_('country'), max_length=100)
    is_default = models.BooleanField(_('default'), default=False)
    
    class Meta:
        abstract = True
        verbose_name = _('user address')
        verbose_name_plural = _('user addresses')
    
    def __str__(self):
        return f"{self.address}, {self.city}, {self.country}"


class Invitation(Base):
    """
    Invitation model for inviting users to the application.
    """
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('VALIDATED', 'Validated'),
        ('EXPIRED', 'Expired'),
    )
    
    email = models.EmailField(_('email address'))
    token = models.CharField(_('token'), max_length=100, unique=True)
    sender = models.ForeignKey(
        UserConfig.ForeignKey.user,
        on_delete=models.CASCADE,
        related_name='sent_invitations',
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
    )
    expires_at = models.DateTimeField(_('expires at'))
    
    class Meta:
        abstract = True
        verbose_name = _('invitation')
        verbose_name_plural = _('invitations')
    
    def __str__(self):
        return f"Invitation for {self.email}"
    
    def is_valid(self):
        """
        Check if the invitation is valid.
        """
        return self.status == 'PENDING' and self.expires_at > timezone.now()


class VerificationToken(Base):
    """
    Verification token model for verifying user accounts.
    """
    user = models.ForeignKey(
        UserConfig.ForeignKey.user,
        on_delete=models.CASCADE,
        related_name='verification_tokens',
    )
    token = models.CharField(_('token'), max_length=100, unique=True)
    expires_at = models.DateTimeField(_('expires at'))
    method = models.CharField(
        _('method'),
        max_length=10,
        choices=(
            ('email', 'Email'),
            ('sms', 'SMS'),
        ),
        default='email',
    )
    
    class Meta:
        abstract = True
        verbose_name = _('verification token')
        verbose_name_plural = _('verification tokens')
    
    def __str__(self):
        return f"Verification token for {self.user}"
    
    def is_valid(self):
        """
        Check if the token is valid.
        """
        return self.expires_at > timezone.now()


class PasswordResetToken(Base):
    """
    Password reset token model for resetting user passwords.
    """
    user = models.ForeignKey(
        UserConfig.ForeignKey.user,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens',
    )
    token = models.CharField(_('token'), max_length=100, unique=True)
    expires_at = models.DateTimeField(_('expires at'))
    method = models.CharField(
        _('method'),
        max_length=10,
        choices=(
            ('email', 'Email'),
            ('sms', 'SMS'),
        ),
        default='email',
    )
    
    class Meta:
        abstract = True
        verbose_name = _('password reset token')
        verbose_name_plural = _('password reset tokens')
    
    def __str__(self):
        return f"Password reset token for {self.user}"
    
    def is_valid(self):
        """
        Check if the token is valid.
        """
        return self.expires_at > timezone.now()

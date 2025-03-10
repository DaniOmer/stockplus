"""
User model implementation.
This module contains django user model implementation.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from stockplus.models.base import Base


class UserManager(BaseUserManager):
    """
    Custom user manager.
    """

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        """
        Create and save a user with the given email/phone and password.
        """
        if not email and not phone_number:
            raise ValueError('The Email or Phone Number field must be set')

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        """
        Create and save a superuser with the given email/phone and password.
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
    Custom user model.
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
        help_text=_('Required. A valid email address.'),
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text=_('Required. A valid phone number.'),
    )
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_('Designates whether this user has verified their account.'),
    )
    # Suppression temporaire de la relation ForeignKey pour éviter les imports circulaires
    # Nous utiliserons uniquement company_id pour la relation
    company_id = models.IntegerField(null=True, blank=True)
    role = models.CharField(
        _('role'),
        max_length=50,
        null=True,
        blank=True,
        help_text=_('The user\'s role in the company.'),
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        help_text=_('The user\'s avatar image.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table ='stockplus_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        if self.email:
            return self.email
        if self.phone_number:
            return self.phone_number
        return self.username or str(self.id)

    def verify(self):
        """
        Verify the user's account.
        """
        self.is_verified = True

    def update_profile(self, email=None, phone_number=None, first_name=None, last_name=None):
        """
        Update the user's profile.
        """
        if email:
            self.email = email
        if phone_number:
            self.phone_number = phone_number
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name

    def assign_to_company(self, company_id, role):
        """
        Assign the user to a company.
        """
        self.company_id = company_id
        self.role = role

    def remove_from_company(self):
        """
        Remove the user from their company.
        """
        self.company = None
        self.role = None

    def activate(self):
        """
        Activate the user's account.
        """
        self.is_active = True

    def deactivate(self):
        """
        Deactivate the user's account.
        """
        self.is_active = False

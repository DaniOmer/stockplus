import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager

from builder.models.base import Base
from builder.applications.address import models as AddressModels
from builder.applications.user import choices
from builder.applications.user.apps import UserConfig

class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('An email or phone number must be set')
        
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email=email, phone_number=phone_number, password=password, **extra_fields)

class User(AbstractUser):
    email = models.CharField(max_length=100, unique=True, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    first_connection = models.DateTimeField(blank=True, null=True)

    if 'builder.applications.nationality' in settings.INSTALLED_APPS:
        nationalities = models.ManyToManyField(UserConfig.ForeignKey.nationalities, blank=True)
        language = models.ForeignKey(UserConfig.ForeignKey.nationalities, on_delete=models.SET_NULL, blank=True, null=True, related_name="language_user")
    
    if 'builder.applications.company' in settings.INSTALLED_APPS:
        company = models.ForeignKey(UserConfig.ForeignKey.company, on_delete=models.SET_NULL, blank=True, null=True, related_name="members")
        role = models.CharField(max_length=100, choices=settings.USER_ROLE, default=settings.USER_ROLE_DEFAULT, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        abstract = True

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self) -> str:
        return self.fullname
    
class UserAddress(AddressModels.Address):
    user = models.ForeignKey(UserConfig.ForeignKey.user, on_delete=models.CASCADE, related_name='user_address')

    class Meta:
        abstract = True


class Invitation(Base):
    email = models.EmailField(unique=True)
    sender = models.ForeignKey(UserConfig.ForeignKey.user, on_delete=models.CASCADE, related_name='invitations')
    token = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=50, choices=choices.INVITATION_STATUS, default='PENDING')
    expires_at = models.DateTimeField()

    class Meta:
        abstract = True
    
    def mark_as_validated(self):
        self.status = 'VALIDATED'
        self.save()
    
    def mark_as_expired(self):
        self.status = 'EXPIRED'
        self.save()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=48)
        if not self.token:
            self.token = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.status == 'PENDING' and timezone.now() < self.expires_at

    def __str__(self):
        return f"Invitation({self.email})"
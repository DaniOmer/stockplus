"""
Collaborator models implementation.
This module contains the ORM models for collaborators, roles, and permissions.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from stockplus.models.base import Base
from stockplus.modules.company.infrastructure.models import Company
from stockplus.modules.user.infrastructure.models.user_model import User
from stockplus.modules.pointofsale.infrastructure.models.pos_model import PointOfSale


class CollaboratorPermission(Base):
    """
    ORM model for a collaborator permission.
    """
    PERMISSION_CATEGORIES = [
        ('sales', _('Sales')),
        ('products', _('Products')),
        ('inventory', _('Inventory')),
        ('reports', _('Reports')),
        ('users', _('Users')),
        ('settings', _('Settings')),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=PERMISSION_CATEGORIES, default='sales')
    
    class Meta:
        db_table = 'stockplus_collaborator_permission'
        verbose_name = 'Collaborator Permission'
        verbose_name_plural = 'Collaborator Permissions'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class CollaboratorRole(Base):
    """
    ORM model for a collaborator role.
    """
    ROLE_TYPES = [
        ('admin', _('Administrator')),
        ('manager', _('Manager')),
        ('cashier', _('Cashier')),
        ('inventory', _('Inventory Manager')),
        ('custom', _('Custom')),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='company_roles',
        help_text=_('The company this role belongs to.'),
    )
    type = models.CharField(max_length=50, choices=ROLE_TYPES, default='custom')
    is_default = models.BooleanField(default=False)
    permissions = models.ManyToManyField(
        CollaboratorPermission,
        through='CollaboratorRolePermission',
        related_name='roles',
    )
    
    class Meta:
        db_table = 'stockplus_collaborator_role'
        verbose_name = 'Collaborator Role'
        verbose_name_plural = 'Collaborator Roles'
        unique_together = [['name', 'company']]
        ordering = ['company', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.company.name})"


class CollaboratorRolePermission(Base):
    """
    ORM model for the many-to-many relationship between roles and permissions.
    """
    role = models.ForeignKey(
        CollaboratorRole,
        on_delete=models.CASCADE,
        related_name='role_permissions',
    )
    permission = models.ForeignKey(
        CollaboratorPermission,
        on_delete=models.CASCADE,
        related_name='permission_roles',
    )
    
    class Meta:
        db_table = 'stockplus_collaborator_role_permission'
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'
        unique_together = [['role', 'permission']]
    
    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"


class Collaborator(Base):
    """
    ORM model for a collaborator.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collaborator_profiles',
        help_text=_('The user associated with this collaborator.'),
    )
    role = models.ForeignKey(
        CollaboratorRole,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='collaborators',
        help_text=_('The role assigned to this collaborator.'),
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='company_collaborators',
        help_text=_('The company this collaborator belongs to.'),
    )
    points_of_sale = models.ManyToManyField(
        PointOfSale,
        related_name='pos_collaborators',
        help_text=_('The points of sale this collaborator is assigned to.'),
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'stockplus_collaborator'
        verbose_name = 'Collaborator'
        verbose_name_plural = 'Collaborators'
        unique_together = [['user', 'company']]
        ordering = ['company', 'user__email']
    
    def __str__(self):
        return f"{self.user.email or self.user.phone_number} ({self.company.name})"

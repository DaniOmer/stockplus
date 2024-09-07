from django.db import models
from django.contrib.auth import get_user_model

from builder.models.base import Base

User = get_user_model()

class Collaboration(Base):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_collaborators')
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_manager')

    class Meta:
        abstract = True
        unique_together = ('manager', 'collaborator')

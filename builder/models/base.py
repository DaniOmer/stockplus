from django.db import models

from builder import translates as _
from uuid import uuid4

class Base(models.Model):
    search_fields = []
    uid = models.UUIDField(unique=True, default=uuid4, editable=False)
    logs = models.JSONField(blank=True, null=True, default=dict)
    is_disable = models.BooleanField(_.is_disable, default=False)
    search = models.TextField(db_index=True, blank=True, null=True)
    date_create = models.DateTimeField(_.date_create, auto_now_add=True, editable=False)
    create_by = models.CharField(_.create_by, blank=True, editable=False, max_length=254, null=True)
    date_update = models.DateTimeField(_.date_update, auto_now=True, editable=False)
    update_by = models.CharField(_.update_by, blank=True, editable=False, max_length=254, null=True)
    update_count = models.PositiveBigIntegerField(default=0)
    note = models.TextField(blank=True, null=True)
    cache = models.JSONField(blank=True, null=True, default=dict)
    use_create_by = True
    use_update_by = True
    can_notify = True

    class Meta:
        abstract = True

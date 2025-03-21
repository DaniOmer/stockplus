from django.db import models

from stockplus import translates as _
from uuid import uuid4

class Base(models.Model):
    search_fields = []
    uid = models.UUIDField(unique=True, default=uuid4, editable=False)
    logs = models.JSONField(blank=True, null=True, default=dict)
    is_disable = models.BooleanField(_.is_disable, default=False)
    search = models.TextField(db_index=True, blank=True, null=True)
    create_by = models.CharField(_.create_by, blank=True, editable=False, max_length=254, null=True)
    created_at = models.DateTimeField(_.date_create, auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_.date_update, auto_now=True, editable=False)
    update_by = models.CharField(_.update_by, blank=True, editable=False, max_length=254, null=True)
    update_count = models.PositiveBigIntegerField(default=0)
    note = models.TextField(blank=True, null=True)
    cache = models.JSONField(blank=True, null=True, default=dict)
    use_create_by = True
    use_update_by = True
    can_notify = True

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)
        self.post_save()
 
    def pre_save(self):
        pass

    def post_save(self):
        pass
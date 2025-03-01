"""
Models for the messenger application.
"""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from builder.modules.messenger.domain.models.missive import Missive as BaseMissive


class Missive(BaseMissive):
    """
    Concrete implementation of the Missive model.
    """
    class Meta(BaseMissive.Meta):
        abstract = False
        verbose_name = "missive"
        verbose_name_plural = "missives"

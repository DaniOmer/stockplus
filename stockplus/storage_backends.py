"""
Storage backends for the stockplus project.
This module contains the storage backends for the stockplus project.
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    """
    Storage backend for media files.
    """
    location = settings.MEDIA_LOCATION
    file_overwrite = False
    default_acl = 'private'

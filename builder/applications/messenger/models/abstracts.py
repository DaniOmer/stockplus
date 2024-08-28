from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from builder.applications.messenger import (
    choices, translates as _,
    missive_backend_email,
    missive_backend_sms,
)
from builder.applications.messenger.apps import MessengerConfig as conf
from builder.models.base import Base
from builder.fields import RichTextField
from html2text import html2text

class MessengerModel(Base):
    mode = models.CharField(max_length=8, choices=choices.MODE, default=choices.MODE_EMAIL)
    status = models.CharField(choices=choices.STATUS, default=choices.STATUS_PREPARE, max_length=8)
    
    name = models.CharField(max_length=255, blank=True, null=True)
    sender = models.CharField(max_length=255, blank=True, null=True)
    reply = models.CharField(max_length=255, blank=True, null=True)
    target = models.CharField(max_length=255)
    service = models.CharField(max_length=255, blank=True, null=True)
    denomination = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)

    header_html = RichTextField(blank=True, null=True)
    footer_html = RichTextField(blank=True, null=True)

    subject = models.CharField(max_length=255)
    template = models.CharField(max_length=255, blank=True, null=True)

    html = RichTextField()
    txt = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta(Base.Meta):
        abstract = True

    def need_to_send(self):
        raise NotImplementedError("Subclasses should implement need_to_send()")

    def set_txt(self):
        if self.html and not self.txt:
            self.txt = html2text(self.html)

    def prepare(self):
        self.status = choices.STATUS_PREPARE

    def to_error(self):
        self.status = choices.STATUS_ERROR

    def prepare_mode(self):
        getattr(self, 'prepare_%s' % self.mode.lower())()

    def pre_save(self):
        self.set_txt()
        self.set_backend()
        self.prepare_mode()
        self.need_to_send()

    def __str__(self):
        return '%s (%s)' % (self.masking, self.subject)

    def prepare_sms(self):
        self.html = 'not used for sms'

    def prepare_postal(self):
        self.txt = 'not used for postal'

    def prepare_postalar(self):
        self.txt = 'not used for postal'

    def prepare_email(self):
        if not self.sender:
            self.sender = conf.sender_email

    def prepare_emailar(self):
        if not self.sender:
            self.sender = conf.sender_email

    def prepare_web(self):
        pass

    def set_backend(self):
        self.backend = conf.missive_backends
        if self.mode == choices.MODE_EMAIL:
            self.backend = missive_backend_email()
        if self.mode == choices.MODE_SMS:
            self.backend = missive_backend_sms()

    @property
    def preheader(self):
        return self.txt

    @property
    def content(self):
        return self.html if self.html else self.txt
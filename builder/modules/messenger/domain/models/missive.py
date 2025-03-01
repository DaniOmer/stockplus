"""
Domain models for the messenger application.
"""
from django.db import models
from django.utils.module_loading import import_string

from builder.modules.messenger import choices, translates as _
from builder.models.base import Base
from builder.fields import RichTextField
from html2text import html2text


class MessengerModel(Base):
    """
    Base model for messenger entities.
    """
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

    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = models.GenericForeignKey('content_type', 'object_id')

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

    def prepare_sms(self):
        self.html = 'not used for sms'

    def prepare_postal(self):
        self.txt = 'not used for postal'

    def prepare_postalar(self):
        self.txt = 'not used for postal'

    def prepare_email(self):
        from builder.modules.messenger.apps import MessengerConfig as conf
        if not self.sender:
            self.sender = conf.sender_email

    def prepare_web(self):
        pass

    def set_backend(self):
        from builder.modules.messenger.apps import MessengerConfig as conf
        from builder.modules.messenger import missive_backend_email, missive_backend_sms
        
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


class Missive(MessengerModel):
    """
    Missive model for sending messages.
    """
    backend = models.CharField(max_length=255, editable=False)
    msg_id = models.CharField(max_length=255, blank=True, null=True)

    response = models.TextField(blank=True, null=True, editable=False)
    partner_id = models.CharField(max_length=255, blank=True, null=True, editable=False)
    code_error = models.CharField(max_length=255, blank=True, null=True, editable=False)
    trace = models.TextField(blank=True, null=True, editable=False)

    class Meta(MessengerModel.Meta):
        abstract = True
        verbose_name = "missive"
        verbose_name_plural = "missives"

    def need_to_send(self):
        if self.status == choices.STATUS_PREPARE and self.mode != choices.MODE_WEB:
            from builder.modules.messenger import send_missive
            send_missive(self)

    def clear_errors(self):
        self.trace = None
        self.code_error = None

    def to_sent(self):
        self.clear_errors()
        self.status = choices.STATUS_SENT

    def get_backend(self):
        backend = import_string(self.backend)()
        return backend

    def check_status(self):
        backend = self.get_backend()
        return getattr(backend, 'check_%s' % self.mode.lower())(self)

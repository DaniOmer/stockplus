from django.db import models
from django.utils.module_loading import import_string

from builder.modules.messenger import choices, translates as _, send_missive
from builder.modules.messenger.infrastructure.models.messenger import Messenger

class Missive(Messenger):
    backend = models.CharField(max_length=255, editable=False)
    msg_id = models.CharField(max_length=255, blank=True, null=True)

    response = models.TextField(blank=True, null=True, editable=False)
    partner_id = models.CharField(max_length=255, blank=True, null=True, editable=False)
    code_error = models.CharField(max_length=255, blank=True, null=True, editable=False)
    trace = models.TextField(blank=True, null=True, editable=False)

    class Meta(Messenger.Meta):
        abstract = True
        verbose_name = "missive"
        verbose_name_plural = "missives"

    def need_to_send(self):
        if self.status == choices.STATUS_PREPARE and self.mode != choices.MODE_WEB:
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

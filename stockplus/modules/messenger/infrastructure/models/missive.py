from django.db import models
from django.utils.module_loading import import_string

from stockplus.modules.messenger import choices, translates as _
from stockplus.modules.messenger.infrastructure.models.messenger import Messenger
from stockplus.utils import get_backends

class Missive(Messenger):
    backend = models.CharField(max_length=255, editable=False)
    msg_id = models.CharField(max_length=255, blank=True, null=True)

    response = models.TextField(blank=True, null=True, editable=False)
    partner_id = models.CharField(max_length=255, blank=True, null=True, editable=False)
    code_error = models.CharField(max_length=255, blank=True, null=True, editable=False)
    trace = models.TextField(blank=True, null=True, editable=False)

    class Meta:
        db_table = 'stockplus_missive'
        verbose_name = "missive"
        verbose_name_plural = "missives"

    def need_to_send(self):
        if self.status == choices.STATUS_PREPARE and self.mode != choices.MODE_WEB:
            self._send_missive()

    def _send_missive(self):
        """Méthode interne pour envoyer un message sans créer d'import circulaire"""
        for backend, backend_path in get_backends([self.backend], return_tuples=True, path_extend='.MissiveBackend', missive=self):
            return backend.send()
        return False

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

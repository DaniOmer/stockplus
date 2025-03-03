from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from html2text import html2text

class Mode(Enum):
    EMAIL = 'EMAIL'
    SMS = 'SMS'
    POSTAL = 'POSTAL'
    POSTALAR = 'POSTALAR'
    WEB = 'WEB'

class Status(Enum):
    PREPARE = 'PREPARE'
    SENT = 'SENT'
    ERROR = 'ERROR'

@dataclass
class Messenger:
    mode: Mode = Mode.EMAIL
    status: Status = Status.PREPARE
    name: Optional[str] = None
    sender: Optional[str] = None
    reply: Optional[str] = None
    target: str = ''
    service: Optional[str] = None
    denomination: Optional[str] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    header_html: Optional[str] = None
    footer_html: Optional[str] = None
    subject: str = ''
    template: Optional[str] = None
    html: str = ''
    txt: str = ''
    content_type: Optional[str] = None
    object_id: Optional[int] = None
    backend: Optional[str] = None
    msg_id: Optional[str] = None
    response: Optional[str] = None
    partner_id: Optional[str] = None
    code_error: Optional[str] = None
    trace: Optional[str] = None

    def __post_init__(self):
        self.set_txt()
        self.set_backend()
        self.prepare_mode()
        self.need_to_send()

    def need_to_send(self):
        if self.status == Status.PREPARE and self.mode != Mode.WEB:
            self.send_missive()

    def set_txt(self):
        if self.html and not self.txt:
            self.txt = html2text(self.html)

    def prepare_mode(self):
        prepare_method = getattr(self, f'prepare_{self.mode.name.lower()}', None)
        if prepare_method:
            prepare_method()

    def prepare_sms(self):
        self.html = 'not used for sms'

    def prepare_postal(self):
        self.txt = 'not used for postal'

    def prepare_postalar(self):
        self.txt = 'not used for postal'

    def prepare_email(self):
        if not self.sender:
            self.sender = 'default_sender@example.com'  # Remplacez par votre valeur par défaut

    def prepare_web(self):
        pass

    def set_backend(self):
        if self.mode == Mode.EMAIL:
            self.backend = 'email_backend'
        elif self.mode == Mode.SMS:
            self.backend = 'sms_backend'
        # Ajoutez d'autres backends selon les besoins

    def clear_errors(self):
        self.trace = None
        self.code_error = None

    def to_sent(self):
        self.clear_errors()
        self.status = Status.SENT

    def get_backend(self):
        # Implémentez la logique pour obtenir l'instance du backend
        pass

    def check_status(self):
        backend = self.get_backend()
        check_method = getattr(backend, f'check_{self.mode.name.lower()}', None)
        if check_method:
            return check_method(self)

    def send_missive(self):
        # Implémentez la logique pour envoyer la missive
        pass

    @property
    def preheader(self):
        return self.txt

    @property
    def content(self):
        return self.html if self.html else self.txt

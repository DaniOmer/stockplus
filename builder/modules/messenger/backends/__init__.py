from django.core.mail import EmailMultiAlternatives
from django.core.mail.message import make_msgid

from builder.utils import setting
from builder.modules.messenger import choices
from builder.modules.messenger.apps import MessengerConfig as conf
import logging, os

logger = logging.getLogger(__name__)

class MissiveBackend():
    email = None
    sms = None

    def __init__(self, missive, *args, **kwargs):
        self.missive = missive

    @property
    def extra(self):
        return {'user': self.missive.content_object, 'app': 'messenger'}

    @property
    def message(self):
        return self.missive.txt if self.missive.txt else self.missive.html

    def send(self):
        return getattr(self, 'send_%s' % self.missive.mode.lower())()

    def send_sms(self):
        over_target = setting('MISSIVE_PHONE', False)
        self.missive.target = over_target if over_target else self.missive.target

        if setting('MISSIVE_SERVICE', False):
            pass

        self.missive.status = choices.STATUS_SENT
        self.missive.save()

        logger.info("send sms: %s" % self.message, extra=self.extra)

        return self.missive.status

    def email_attachments(self):
        if self.missive.attachments:
            logs = []
            for document in self.missive.attachments:
                if setting('MISSIVE_SERVICE', False):
                    self.email.attach(os.path.basename(document.name), document.read(), 'application/pdf')
                logs.append(os.path.basename(document.name))
            self.missive.logs['attachments'] = logs

        if setting('MISSIVE_SERVICE', False):
            self.email.send()

    @property
    def sender_email(self):
        if self.missive.name:
            return "%s <%s>" % (self.missive.name, self.missive.sender)
        return self.missive.sender

    @property
    def reply_email(self):
        return [self.missive.reply] if self.missive.reply else [self.missive.sender]

    def send_email(self):
        over_target = setting('MISSIVE_EMAIL', False)
        self.missive.target = over_target if over_target else self.missive.target

        if setting('MISSIVE_SERVICE', False):
            self.missive.msg_id = make_msgid()
            text_content = str(self.missive.txt)
            html_content = self.missive.html_format
            self.email = EmailMultiAlternatives(
                self.missive.subject,
                html_content,
                self.sender_email,
                [self.missive.target],
                reply_to=self.reply_email,
                headers={'Message-Id': self.missive.msg_id}
            )
            self.email.attach_alternative(html_content, "text/html")

        self.email_attachments()
        self.missive.to_sent()
        self.missive.save()
        return self.missive.status

    def check(self, missive):
        return True
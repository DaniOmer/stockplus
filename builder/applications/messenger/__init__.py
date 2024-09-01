default_app_config = 'builder.applications.messenger.apps.MessengerConfig'

from django.conf import settings
from builder.functions import get_backends
from builder.applications.messenger.choices import MODE_EMAIL, MODE_SMS
from builder.applications.messenger.apps import MessengerConfig as conf
import logging

logger = logging.getLogger(__name__)

def send_missive(missive):
    for backend, backend_path in get_backends([missive.backend], return_tuples=True, path_extend='.MissiveBackend', missive=missive):
        logger.info(f"Sending : {backend}")
        return backend.send()
    return False

def send_missive_type(**kwargs):
    from builder.models import Missive
    logger.warning(kwargs)
    missive = Missive(
        header_html=kwargs.get('header_html'),
        footer_html=kwargs.get('footer_html'),
        content_type=kwargs.get('content_type'),
        object_id=kwargs.get('object_id'),
        mode=kwargs.get('mode'),
        sender=kwargs.get('sender'),
        name=kwargs.get('name'),
        reply=kwargs.get('reply'),
        target=kwargs.get('target'),
        subject=kwargs.get('subject'),
        last_name=kwargs.get('last_name'),
        first_name=kwargs.get('first_name'),
        denomination=kwargs.get('denomination'),
        html=kwargs.get('html'),
        txt=kwargs.get('txt'),
        address=kwargs.get('address'),
        complement=kwargs.get('complement'),
        postal_code=kwargs.get('postal_code'),
        locality=kwargs.get('locality'),
        state=kwargs.get('state'),
        state_code=kwargs.get('state_code'),
        country=kwargs.get('country', 'France'),
        country_code=kwargs.get('country_code', 'FR'),
        raw=kwargs.get('raw'),
    )
    missive.attachments = kwargs.get('attachments')
    missive.save()
    return missive

def send_email(**kwargs):
    return send_missive_type(**kwargs, mode=MODE_EMAIL)

def send_sms(**kwargs):
    return send_missive_type(**kwargs, mode=MODE_SMS, html="empty_for_sms")

def missive_backend_email():
    return settings.MISSIVE_BACKEND_EMAIL if hasattr(settings, 'MISSIVE_BACKEND_EMAIL') else conf.missive_backends

def missive_backend_sms():
    return settings.MISSIVE_BACKEND_SMS if hasattr(settings, 'MISSIVE_BACKEND_SMS') else conf.missive_backends


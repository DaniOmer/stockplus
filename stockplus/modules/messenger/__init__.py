import logging

from django.conf import settings
from stockplus.utils import get_backends
from stockplus.modules.messenger.choices import MODE_EMAIL, MODE_SMS
from stockplus.modules.messenger.infrastructure.apps import MessengerConfig as conf

logger = logging.getLogger(__name__)

def send_missive(missive):
    """
    Envoie un message en utilisant le backend approprié.
    
    Args:
        missive: L'objet missive à envoyer
        
    Returns:
        bool: True si le message a été envoyé avec succès, False sinon
    """
    for backend, backend_path in get_backends([missive.backend], return_tuples=True, path_extend='.MissiveBackend', missive=missive):
        logger.info(f"Sending : {backend}")
        return backend.send()
    return False

def send_missive_type(**kwargs):
    """
    Crée et envoie un message du type spécifié.
    
    Args:
        **kwargs: Les paramètres du message
        
    Returns:
        Missive: L'objet missive créé
    """
    # Import ici pour éviter les imports circulaires
    from stockplus.modules.messenger.infrastructure.models.missive import Missive
    
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
    """
    Crée et envoie un email.
    
    Args:
        **kwargs: Les paramètres de l'email
        
    Returns:
        Missive: L'objet missive créé
    """
    return send_missive_type(**kwargs, mode=MODE_EMAIL)

def send_sms(**kwargs):
    """
    Crée et envoie un SMS.
    
    Args:
        **kwargs: Les paramètres du SMS
        
    Returns:
        Missive: L'objet missive créé
    """
    return send_missive_type(**kwargs, mode=MODE_SMS, html="empty_for_sms")

def missive_backend_email():
    """
    Retourne le backend d'email configuré.
    
    Returns:
        str: Le chemin du backend d'email
    """
    return settings.MISSIVE_BACKEND_EMAIL if hasattr(settings, 'MISSIVE_BACKEND_EMAIL') else conf.missive_backends

def missive_backend_sms():
    """
    Retourne le backend de SMS configuré.
    
    Returns:
        str: Le chemin du backend de SMS
    """
    return settings.MISSIVE_BACKEND_SMS if hasattr(settings, 'MISSIVE_BACKEND_SMS') else conf.missive_backends

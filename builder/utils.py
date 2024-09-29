import stripe
import logging

logger = logging.getLogger(__name__)

from django.conf import settings
from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured

def setting(name, default=None):
    return getattr(settings, name, default)

def get_backends(backends_list, return_tuples=False, path_extend='', *args, **kwargs):
    backends = []
    for backend_path in backends_list:
        backend_path = backend_path + path_extend
        backend = import_string(backend_path)(*args, **kwargs)
        backends.append((backend, backend_path) if return_tuples else backend)
    if not backends:
        raise ImproperlyConfigured('No backends have been defined.')
    return backends

def init_stripe():
    stripe_api_key = setting('STRIPE_API_KEY', None)
    env = setting('ENV', 'DEVELOPMENT')

    if stripe_api_key is not None:
        if env != 'DEVELOPMENT' and 'sk_test' in stripe_api_key:
            logger.warning(f'You provide the wrong stripe API key. {env}')
            raise ValueError('You provide the wrong stripe API key.')
        stripe.api_key = stripe_api_key
        return stripe
    logger.warning('You must provide a stripe API key..')
    raise ValueError('You must provide a stripe API key.')

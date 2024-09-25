import stripe

from builder.utils import setting

def init_stripe():
    stripe_api_key = setting('STRIPE_API_KEY', None)
    env = setting('ENV', 'DEVELOPMENT')

    if stripe_api_key is not None:
        if env != 'DEVELOPMENT' and 'pk_test' in stripe_api_key:
            raise ValueError('You provide the wrong stripe API key.')
        stripe.api_key = stripe_api_key
        return stripe
    raise ValueError('You must provide a stripe API key.')

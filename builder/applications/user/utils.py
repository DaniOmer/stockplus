from django.urls import reverse
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from builder.functions import setting

def generate_verification_token(user):
    token = RefreshToken.for_user(user).access_token
    if setting('EMAIL_VERIFICATION_TOKEN_LIFETIME', False):
        token.set_exp(lifetime=settings.EMAIL_VERIFICATION_TOKEN_LIFETIME)
        token['scope'] = 'email_verification'
        return token
    return None

def generate_verification_url(user):
    token = generate_verification_token(user)
    if token is not None and setting('FRONTEND_URL', False):
        verification_link = reverse('email-verify')
        verification_url = f"{settings.FRONTEND_URL}{verification_link}?token={str(token)}"
        return verification_url
    return None
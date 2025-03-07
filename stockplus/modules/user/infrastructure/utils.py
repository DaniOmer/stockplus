from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string

from rest_framework_simplejwt.tokens import RefreshToken

from stockplus.utils import setting
from stockplus.modules.messenger.domain.entities import Missive

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

def get_verification_data_missive(user):
    verification_url = generate_verification_url(user)
    if verification_url is not None:
        html_content = render_to_string('activation_mail.html', {'user': user, 'verification_url': str(verification_url)})
        return {
            "subject": 'Bienvenue chez Stockplus',
            "target": user.email,
            "template": 'activation_mail.html',
            "html": html_content,
            "message": html_content,
        }
    return None


def get_invitation_data_missive(invitation):
    sender = invitation.sender.first_name
    invitation_link = reverse('user-create-from-invitation')
    invitation_url = f"{settings.FRONTEND_URL}{invitation_link}?token={str(invitation.token)}"
    html_content = render_to_string('invitation_mail.html', {'invitation_url': str(invitation_url), 'sender': str(sender)})
    missive = Missive(
        subject=f"{sender} vous invite à rejoindre Stockplus",
        target=invitation.email,
        template='invitation_mail.html',
        html=html_content,
        message=html_content
    )
    return missive
    # return {
    #     "content_type": None,
    #     "object_id": None,
    #     "subject": f"{sender} vous invite à rejoindre Stockplus",
    #     "html": html_content,
    #     "txt": html_content,
    #     "target": invitation.email,
    #     "mode": "EMAIL",
    #     "template": "invitation_mail.html"
    # }
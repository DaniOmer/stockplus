from django.conf import settings

from builder.functions import setting
from builder.applications.messenger import choices
from builder.applications.messenger.backends import MissiveBackend
from builder.applications.messenger.apps import MessengerConfig as conf

from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

"""
Default configuration from Brevo (Sendinblue)
Send Transactional Emails in Python Recipe
"""
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = 'YOUR API KEY'

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
subject = "from the Python SDK!"
sender = {"name":"Sendinblue","email":"contact@sendinblue.com"}
html_content = "<html><body><h1>This is my first transactional email </h1></body></html>"
to = [{"email":"example@example.com","name":"Jane Doe"}]
cc = [{"email":"example2@example2.com","name":"Jane Doe"}]
bcc = [{"email":"example2@example2.com","name":"Jane Doe"}]
reply_to = {"name":"Sendinblue","email":"contact@sendinblue.com"}
headers = {"Some-Custom-Name":"unique-id-1234"}
params = {"parameter":"My param value","subject":"New Subject"}
send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, bcc=bcc, cc=cc, reply_to=reply_to, headers=headers, html_content=html_content, sender=sender, subject=subject)

try:
    api_response = api_instance.send_transac_email(send_smtp_email)
    print(api_response)
except ApiException as e:
    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


"""
Custom implementation using MissiveBackend
"""
class MissiveBackend(MissiveBackend):
    CONFSIB = False
    APISIB = False
    APIEMAIL = False

    @property
    def conf_sib(self):
        if not self.CONFSIB:
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = settings.SENDINBLUE_APIKEY
            self.CONFSIB = configuration
        return self.CONFSIB
            
    @property
    def api_sib(self):
        if not self.APISIB:
            self.APISIB = sib_api_v3_sdk.ApiClient(self.conf_sib)
        return self.APISIB

    @property
    def api_email(self):
        if not self.APIEMAIL:
            self.APIEMAIL = sib_api_v3_sdk.TransactionalEmailsApi(self.api_sib)
        return self.APIEMAIL

    def use_api_email(self, missive):
        api_instance = self.api_email
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": self.missive.target}],
            reply_to={"email": self.missive.sender, "name": conf.reply_name},
            sender={"email": self.missive.sender, "name": conf.sender_name},
            subject= self.missive.subject
            html_content=self.missive.html,
            text_content=self.missive.txt,
        )
        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            self.missive.trace = str(api_response)
            return True
        except Exception as e:
            self.missive.trace(str(e))
            return False

    def send_email(self):
        over_target = setting('MISSIVE_PHONE', False)
        self.missive.target = over_target if over_target else self.missive.target
        self.missive.status = choices.STATUS_SENT
        if setting('MISSIVE_SERVICE', False):
            if not self.use_api_email(self.missive):
                self.missive.status = choices.STATUS_ERROR
        self.missive.save()      
        return self.missive.status

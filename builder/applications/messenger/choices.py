from django.utils.translation import gettext_lazy as _

ERROR_SMTP_101 = "The server is unable to connect."
ERROR_SMTP_111 = "Connection refused or inability to open an SMTP stream."
ERROR_SMTP_211 = "System status message or help reply."
ERROR_SMTP_214 = "A response to the HELP command."
ERROR_SMTP_220 = "The server is ready."
ERROR_SMTP_221 = "The server is closing its transmission channel. It can come with side messages like “Goodbye” or “Closing connection”."
ERROR_SMTP_250 = "Its typical side message is “Requested mail action okay completed”: meaning that the server has transmitted a message."
ERROR_SMTP_251 = "“User not local will forward”: the recipient’s account is not on the present server, so it will be relayed to another."
ERROR_SMTP_252 = "The server cannot verify the user, but it will try to deliver the message anyway."
ERROR_SMTP_354 = "The side message can be very cryptic (“Start mail input end <CRLF>.<CRLF>”. It’s the typical response to the DATA command."
ERROR_SMTP_420 = "“Timeout connection problem”: there have been issues during the message transfer."
ERROR_SMTP_421 = "The service is unavailable due to a connection problem: it may refer to an exceeded limit of simultaneous connections, or a more general temporary problem."
ERROR_SMTP_422 = "The recipient’s mailbox has exceeded its storage limit."
ERROR_SMTP_431 = "Not enough space on the disk, or an “out of memory” condition due to a file overload."
ERROR_SMTP_432 = "Typical side-message: “The recipient’s Exchange Server incoming mail queue has been stopped”."
ERROR_SMTP_441 = "The recipient’s server is not responding."
ERROR_SMTP_442 = "The connection was dropped during the transmission."
ERROR_SMTP_446 = "The maximum hop count was exceeded for the message: an internal loop has occurred."
ERROR_SMTP_447 = "Your outgoing message timed out because of issues concerning the incoming server."
ERROR_SMTP_449 = "A routing error."
ERROR_SMTP_450 = "Requested action not taken – The user’s mailbox is unavailable. The mailbox has been corrupted or placed on an offline server, or your email hasn’t been accepted for IP problems or blacklisting."
ERROR_SMTP_451 = "Requested action aborted – Local error in processing. Your ISP’s server or the server that got a first relay from yours has encountered a connection problem."
ERROR_SMTP_452 = "Too many emails sent or too many recipients: more in general, a server storage limit exceeded."
ERROR_SMTP_471 = "An error of your mail server, often due to an issue of the local anti-spam filter."
ERROR_SMTP_500 = "A syntax error: the server couldn’t recognize the command."
ERROR_SMTP_501 = "Another syntax error, not in the command but in its parameters or arguments."
ERROR_SMTP_502 = "The command is not implemented."
ERROR_SMTP_503 = "The server has encountered a bad sequence of commands, or it requires an authentication."
ERROR_SMTP_504 = "A command parameter is not implemented."
ERROR_SMTP_510 = "Bad email address."
ERROR_SMTP_511 = "Bad email address."
ERROR_SMTP_512 = "A DNS error: the host server for the recipient’s domain name cannot be found."
ERROR_SMTP_513 = "Address type is incorrect: another problem concerning address misspelling. In few cases, however, it’s related to an authentication issue."
ERROR_SMTP_523 = "The total size of your mailing exceeds the recipient server’s limits."
ERROR_SMTP_530 = "Normally, an authentication problem. But sometimes it’s about the recipient’s server blacklisting yours, or an invalid email address."
ERROR_SMTP_541 = "The recipient address rejected your message: normally, it’s an error caused by an anti-spam filter."
ERROR_SMTP_550 = "It usually defines a non-existent email address on the remote side."
ERROR_SMTP_551 = "“User not local or invalid address – Relay denied”. Meaning, if both your address and the recipient’s are not locally hosted by the server, a relay can be interrupted."
ERROR_SMTP_552 = "“Requested mail actions aborted – Exceeded storage allocation”: simply put, the recipient’s mailbox has exceeded its limits."
ERROR_SMTP_553 = "“Requested action not taken – Mailbox name invalid”. That is, there’s an incorrect email address into the recipients line."
ERROR_SMTP_554 = "This means that the transaction has failed. It’s a permanent error and the server will not try to send the message again."

STATUS_PREPARE = 'PREPARE'
STATUS_SENT = 'SENT'
STATUS_RECEIVED = 'RECEIVED'
STATUS_OPEN = 'OPEN'
STATUS_ERROR = 'ERROR'

STATUS = (
    (STATUS_PREPARE, _("prepare")),
    (STATUS_SENT, _("sent")),
    (STATUS_RECEIVED, _("received")),
    (STATUS_ERROR, _("error")),
)

MODE_EMAIL = 'EMAIL'
MODE_SMS = 'SMS'
MODE_WEB = 'WEB'

MODE = (
    (MODE_EMAIL, _("email")),
    (MODE_SMS, _("sms")),
)
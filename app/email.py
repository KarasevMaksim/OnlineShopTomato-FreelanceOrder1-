from flask_mail import Message
from app import mail
from config import Config


def send_mail(subject, recipients, text_body=0, html_body=0):
    try:
        msg = Message()
        msg.charset = 'utf-8'
        msg.subject = subject
        msg.sender = Config.MAIL_USERNAME
        msg.recipients = recipients
        if text_body:
            msg.body = text_body
        elif html_body:
            msg.html = html_body
        mail.send(msg)
    except Exception as err:
        return err
    return True

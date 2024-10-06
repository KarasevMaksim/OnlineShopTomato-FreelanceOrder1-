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


def msg_for_contacts(theme, name, email, phone, message):
    return f'''
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{theme}</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      font-size: 14px;
      line-height: 1.5;
    }}
    a {{
      color: #337ab7;
      text-decoration: none;
    }}
    a:hover {{
      color: #23527c;
    }}
  </style>
</head>
<body>
  <!-- Основное содержимое письма -->
  <p>
    <h2>{theme}</h2>
    Имя отправителя: {name}<br>
    Email отпровителя: {email}<br>
    Номер телефона отправителя: {phone}<br>
    <hr>
  </p>
  <p>
    {message}
  </p>
</body>
</html>
        '''
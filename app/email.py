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


def create_dop_msg(item):
    text = f'''
        <div>
          <p>
            Название товара: {item['name']}<br>
            Цена товара: {item['price']} р.<br>
            Количество твара: {item['count']} шт.<br>
            Общая цена: {item['total']} р.<br>
            Категория: {item['section']}<br>
            Под Категория: {item['sub_section']}<br>
            Ссылка на товар: {item['link']}<br>
            <div>
              <img src="{item['img_link']}" alt="img_not_found">
            </div>
          </p>
          <hr>
        </div>
        '''
    return text


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


def msg_basket_for_user(name, total_sum, products):
    base_msg = f'''
    <!DOCTYPE html>
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Заказ в магазине!</title>
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
        <h2>Заказ в магазине Tomato Shop</h2>
        Здравствуйте {name}<br>
        Спасибо за заказ. Он будет зарезервирован,
        пока мы не подтвердим, что платёж получен.
        В то же время, напоминаем содержимое вашего заказа:
        <hr>
      </p>'''

    dop_msg = [create_dop_msg(i) for i in products]
    dop_msg = ''.join(dop_msg)
    
    lust_msg = f'''
        <div>
          <h3>Итого: {total_sum} р.</h3>
          <h4>Мы свяжемся с вами для уточнения деталей</h4>
        </div>
      </body>
    </html>'''
    
    return base_msg + dop_msg + lust_msg
        
        
def msg_basket_for_admin(name, email, phone, total_sum, products): 
    base_msg = f'''
    <!DOCTYPE html>
    <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Заказ в магазине!</title>
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
        <h2>Заказ в магазине!</h2>
        Имя отправителя: {name}<br>
        Email отпровителя: {email}<br>
        Номер телефона отправителя: {phone}<br>
        <hr>
      </p>'''
        
    dop_msg = [create_dop_msg(i) for i in products]
    dop_msg = ''.join(dop_msg)
    
    lust_msg = f'''
        <div>
          <h3>Итого: {total_sum} р.</h3>
        </div>
      </body>
    </html>'''
    
    return base_msg + dop_msg + lust_msg
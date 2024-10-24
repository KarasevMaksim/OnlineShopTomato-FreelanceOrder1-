import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    DOMAIN = os.environ.get('DOMAIN')
    NEW_DOMAIN2 = os.environ.get('NEW_DOMAIN2')

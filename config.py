import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_DEBUG = True
    SQLALCHEMY_DATAVASE_URI = os.environ.get('DATABASE_URL')
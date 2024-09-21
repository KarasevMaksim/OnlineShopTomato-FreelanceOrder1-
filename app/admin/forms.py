import re

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SelectField, SubmitField,
    TextAreaField, FileField
)
from wtforms.validators import (
    ValidationError, DataRequired, Length, Regexp, Optional
)
from app import db
from app.models import Users, Sections, Products
from config import Config


class LoginForm(FlaskForm):
    name = StringField('Логин: ', validators=
                       [DataRequired(message='Поле не может быть пустым'),
                        Length(min=1, max=10),
                        Regexp(r'^[a-zA-Zа-яА-Я0-9_]+$', message="only aA1_")
                        ])
    
    password = PasswordField('Пароль: ', validators=
                             [DataRequired(message='Поле не может быть пустым!'),
                              Length(min=6, max=18)
                              ])
    
    remember_me = BooleanField('Запомнить меня: ')
    
    submit = SubmitField('Войти')
    
    
class AddProductForm(FlaskForm):
    name = StringField('Название товара: ', validators=
                       [DataRequired(message='Поле не может быть пустым'),
                        Length(min=1, max=300)
                        ])
    
    about = TextAreaField('Описание товара: ', validators=
                          [Optional(),
                           Length(min=1, max=10000)
                           ])
    
    price = StringField('Цена товара: ', validators=
                        [DataRequired(message='Поле не может быть пустым'),
                         Length(min=1, max=20)
                         ])
    
    select_section = SelectField('Категория товара: ', choices=[])
    
    upload = FileField('Загрузить изображение: ')
    
    submit = SubmitField('Применить')


class AddSectionsForm(FlaskForm):
    name = StringField('Название Категории: ', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(min=1, max=300)
    ])

    submit = SubmitField('Добавить')

    def validate_name(self, name):
        sections = Sections.query.filter(Sections.name == name.data.lower()).first()
        if sections:
            raise ValidationError('Данная категория уже существует!')


class AddSubSectionsForm(FlaskForm):
    name = StringField('Название подакатегории: ', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(min=1, max=300)
    ])
    
    select_section = SelectField('Выбирите основную категорию!: ', choices=[])
    
    submit = SubmitField('Добавить')

import re

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SelectField, SubmitField
)
from wtforms.validators import (
    ValidationError, DataRequired, Length, Regexp
)
from app import db
from app.models import Users, Sections, Products
from config import Config


class LoginForm(FlaskForm):
    name = StringField('Логин', validators=
                       [DataRequired(message="Поле не может быть пустым"),
                        Length(min=1, max=20),
                        Regexp(r'^[a-zA-Zа-яА-Я0-9_]+$', message="only aA1_")
                        ])
    
    password = PasswordField('Пароль', validators=
                             [DataRequired(message='Поле не может быть пустым!'),
                              Length(min=6, max=18)
                              ])
    
    remember_me = BooleanField('Запомнить меня')
    
    submit = SubmitField('Войти')
    
    
class AddProductForm(FlaskForm):
    name = StringField('Логин', validators=
                       [DataRequired(message="Поле не может быть пустым"),
                        Length(min=1, max=300),
                        Regexp(r'^[a-zA-Zа-яА-Я0-9_-:;]+$', message="only aA1_-:;")
                        ])
    
    about = StringField('Описание', validators=[Length(min=1, max=10000)])
    
    prise = StringField('Цена', validators=[Length(min=10, max=20)])
    
    select_section = SelectField('Категория товара', choices=
                                 list(map(
                                     lambda i: (i.name, i.name),
                                     Sections.query.all()
                                     )))
    

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
from app.models import Users, Sections, SubSections, Products
from config import Config
from flask_wtf.file import FileAllowed, FileRequired


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
    
    select_sub_section = SelectField('Подкатегория товара: ', choices=[])
    

    upload = FileField('Загрузить изображение: ', validators=
                       [
                           FileRequired(),
                           FileAllowed(
                            [
                                'jpg', 'png',
                                'jpeg', 'gif',
                                'webm', 'webp'
                            ],
                            'Только .jpg .png .gif .webp .webm!'
                            )
                        ])
    
    submit = SubmitField('Применить')
    
class ShowProductsForm(FlaskForm):
    select_section2 = SelectField('Категория товара: ', choices=[])
    select_sub_section2 = SelectField('Подкатегория товара: ', choices=[])
    submit1 = SubmitField('Применить')

class AddSectionsForm(FlaskForm):
    name = StringField('Название Категории: ', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(min=1, max=300)
    ])

    submit = SubmitField('Add Category')

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
    
    submit = SubmitField('Add SubCategory')


    def validate_name(self, name):
        sub_sections = SubSections.query.filter(SubSections.name == name.data.lower()).first()
        if sub_sections:
            raise ValidationError('Данная подкатегория уже существует!')

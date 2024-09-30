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



class ShowProductsForm(FlaskForm):
    select_section2 = SelectField('Категория товара: ', choices=[])
    select_sub_section2 = SelectField('Подкатегория товара: ', choices=[])
    submit1 = SubmitField('Применить')
    submit2 = SubmitField('Показать все')

    
class SearchForm(FlaskForm):
    input_search = StringField('Найти товар: ', validators=
                               [DataRequired(
                                   message='Поле не может быть пустым'),
                                Length(
                                    min=3,
                                    max=20,
                                    message='Ввод разрешен: от 3, до 20 символов'
                                ),
                                Regexp(
                                    r'^[а-яА-Яa-zA-Z0-9\s]+$',
                                    message='Введен неподдерживаемый символ'
                                )
                               ]
    )
    submit = SubmitField('Поиск')
    
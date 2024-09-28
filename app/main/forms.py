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
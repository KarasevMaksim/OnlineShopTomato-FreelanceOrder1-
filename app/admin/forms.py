from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SelectField, SubmitField,
    TextAreaField, FileField
)
from wtforms.validators import (
    ValidationError, DataRequired, Length, Regexp, Optional
)
from app.models import Sections, SubSections
from flask_wtf.file import FileAllowed, FileRequired


class LoginForm(FlaskForm):
    name = StringField('Логин: ', validators=
                       [DataRequired(message='Поле не может быть пустым'),
                        Length(min=1, max=11),
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
                         Length(min=1, max=8, message='от 1 до 8 символов!'),
                         Regexp(r'^\d+$', message='Тлько цифры!')
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


class NewsForm(FlaskForm):
    name = StringField('Название новости: ', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(min=1, max=300)
    ])
    post = TextAreaField('Новость: ', validators=[
        DataRequired(message='Поле не может быть пустым')
    ])
    submit = SubmitField('Создать')
    
    
class ContactsForm(FlaskForm):
    phone = StringField('Номер телефона', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(min=1, max=50)
    ])
    email = StringField("Почта", validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(min=1, max=100)
    ])
    submit = SubmitField('Обновить')


class AboutForm(FlaskForm):
    about = TextAreaField(
        'Введите новый текст для страницы "О нас"',
        validators=
        [
            DataRequired(message='Поле не может быть пустым'),
            Length(min=1, max=10000, message=
                   'Лимит символов от 1 до 10000 символов'
            )
        ]
    )
    submit = SubmitField('Применить')


class SellAndByForm(FlaskForm):
    sell_and_by = TextAreaField(
        'Введите новый текст для страницы "Доставка и оплата"',
        validators=
        [
            DataRequired(message='Поле не может быть пустым'),
            Length(min=1, max=10000, message=
                   'Лимит символов от 1 до 10000 символов'
            )
        ]
    )
    submit = SubmitField('Применить')

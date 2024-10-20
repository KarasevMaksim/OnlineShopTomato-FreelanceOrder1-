from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, SubmitField,
    TextAreaField, TelField, EmailField
)
from wtforms.validators import (
    DataRequired, Length, Regexp, Email
)


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
    

class ContactMessageForm(FlaskForm):
    name = StringField('Ваше имя', validators=
                               [DataRequired(
                                   message='Поле не может быть пустым'),
                                Length(
                                    min=3,
                                    max=50,
                                    message='Ввод разрешен: от 3, до 50 символов'
                                ),
                                Regexp(
                                    r'^[а-яА-Яa-zA-Z0-9\s]+$',
                                    message='Введен неподдерживаемый символ'
                                )
                               ]
    )
    email = EmailField('Ваш email', validators=
                        [DataRequired(
                            message='Поле не может быть пустым'
                        ),
                         Email(
                            message='Не верный адресс'  
                        )]
    )
    
    phone_number = TelField('Номер телефона', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(min=10, max=15, message=
               'Номер телефона должен быть от 10 до 15 символов'
        ),
        Regexp(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', message=
               'Некорректный формат номера телефона'
        )]
    )
    
    theme = StringField('Тема обращения', validators=
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
    message = TextAreaField('Сообщение', validators=
                               [DataRequired(
                                   message='Поле не может быть пустым'),
                                Length(
                                    min=3,
                                    max=3000,
                                    message='Ввод разрешен: от 3, до 3000 символов'
                                ),
                                Regexp(
                                    r'^[а-яА-Яa-zA-Z0-9\s\.,!?-]+$',
                                    message='Введен неподдерживаемый символ'
                                )
                               ]
    )
    submit = SubmitField('Отправить')

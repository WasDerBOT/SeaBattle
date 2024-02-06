from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import PasswordField, BooleanField, SubmitField, StringField, FileField, TextAreaField,\
    IntegerField, DecimalField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email

from data import db_session
from data.models import User, ProductCategory


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    username = StringField('Ваше имя', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField('Пароль еще раз', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email.data).first()
        if user is not None:
            raise ValidationError('Данный емейл уже зарегистрирован.')

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('Пароль не может быть короче 8 символов.')


class ProfileEditForm(FlaskForm):
    password_old = PasswordField('Текущий пароль', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField('Пароль еще раз', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Изменить пароль')

    def validate_password_old(self, password):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if not user.check_password(password.data):
            raise ValidationError('Не верный текущий пароль')

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('Пароль не может быть короче 8 символов.')




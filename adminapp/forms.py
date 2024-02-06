from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FileField, DecimalField, SelectField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    submit = SubmitField('Добавить')


class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    image = FileField('Изображение', validators=[FileAllowed(['jpg', 'png'], 'Только изображения!')])
    short_desc = StringField('Краткое описание')
    description = TextAreaField('Описание')
    price = DecimalField('Цена')
    quantity = IntegerField('Количество')
    submit = SubmitField('Добавить')

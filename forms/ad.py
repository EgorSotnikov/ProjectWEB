from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AdsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    genre = StringField('Жанр', validators=[DataRequired()])
    about = TextAreaField("Сюжет")
    publisher = StringField('Издательство', validators=[DataRequired()])
    year = IntegerField('Год издания', validators=[DataRequired()])
    submit = SubmitField('Применить')

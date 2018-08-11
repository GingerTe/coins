from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.fields.html5 import IntegerField, URLField, DateField
from wtforms import validators


class EditCoinForm(FlaskForm):
    name = StringField('Название монеты', validators=[validators.Length(0, 250)])
    year = IntegerField('Год выпуска', validators=[validators.NumberRange(0, 2050)])
    mint = SelectField('Монетный двор')
    description = TextAreaField('Описание')
    description_url = URLField('Ссылка')
    num = StringField('Тираж')
    date = DateField('Дата выпуска', validators=(validators.Optional(),))
    is_got = BooleanField('В наличии')

    submit = SubmitField('Сохранить')

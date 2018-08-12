from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.fields.html5 import IntegerField, URLField, DateField
from wtforms import validators

from app.models import Mint


class NonValidatingSelectMultipleField(SelectField):
    """
    Attempt to make an open ended select multiple field that can accept dynamic
    choices added by the browser.
    """

    def pre_validate(self, form):
        pass


class EditCoinForm(FlaskForm):
    name = StringField('Название монеты', validators=(validators.Length(0, 250), validators.DataRequired()))
    year = IntegerField('Год выпуска', validators=(validators.Optional(), validators.NumberRange(0, 2050)))
    mint = SelectField('Монетный двор')
    description = TextAreaField('Описание')
    description_url = URLField('Ссылка')
    num = StringField('Тираж')
    date = DateField('Дата выпуска', validators=(validators.Optional(),))
    is_got = BooleanField('В наличии')
    group = NonValidatingSelectMultipleField('Группа', choices=tuple())

    def __init__(self):
        super(EditCoinForm, self).__init__()
        self.mint.choices = [('', '')] + [(str(mint.id), mint.abbr) for mint in (Mint.query.order_by(Mint.name).all())]

    def validate_group(self, field):
        pass

    submit = SubmitField('Сохранить')

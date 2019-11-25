from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, Form
from wtforms.validators import DataRequired, Length

class racersForm(FlaskForm):
    year = StringField(validators=[DataRequired(), Length(min=4, max=4)])
    season = StringField(validators=[DataRequired(), Length(min=0, max=3)])
    submit = SubmitField(label="Submit")

class weatherForm(FlaskForm):
    city_name = StringField(validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField(label="Submit")
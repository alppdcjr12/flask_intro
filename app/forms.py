from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, Form, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class ContactForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email()])
    message = TextAreaField(validators=[DataRequired()])
    submit = SubmitField(label="Submit")
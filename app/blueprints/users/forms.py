from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, Form, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class ProfileForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email()])
    about_me = TextAreaField(validators=[Length(min=0, max=300)])
    password = PasswordField(
        validators=[EqualTo('confirm_password'), DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired()])
    submit = SubmitField(label="Submit")

class BlogForm(FlaskForm):
    body = StringField(validators=[DataRequired()])
    submit = SubmitField(label="Submit")
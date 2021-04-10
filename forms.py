from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, NumberRange

class RegForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    panid = StringField('Pan Id.', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    panid = StringField('Pan Id.',validators=[DataRequired()])
    submit = SubmitField('Login')
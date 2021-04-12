from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    IntegerField,
    DateField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, NumberRange, Optional


class RegForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    panid = StringField("Pan Id.", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    panid = StringField("Pan Id.", validators=[DataRequired()])
    submit = SubmitField("Login")

class LoginAdminForm(FlaskForm):
    loginid = PasswordField("Login ID", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password")
    submit = SubmitField("Login")

class holdingForm(FlaskForm):
    orderid = IntegerField("Order Id.", validators=[DataRequired()])
    stockname = StringField("Stock Name", validators=[DataRequired()])
    date = DateField("Date", format="%d/%m/%Y", validators=[Optional()])
    buyingprice = IntegerField("Buying Price", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Register")

class deleteholdingForm(FlaskForm):
    orderid = IntegerField("Order Id.", validators=[DataRequired()])
    submit = SubmitField("Register")

class watchlistForm(FlaskForm):
    stockname = StringField("Stock Name", validators=[DataRequired()])
    submit = SubmitField("Register")

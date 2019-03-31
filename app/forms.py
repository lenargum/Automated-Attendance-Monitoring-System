from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class TokenConfirmForm(FlaskForm):
    group_name = StringField("BS Group name", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    submit = SubmitField("Check")


class SessionCreateForm(FlaskForm):
    course = SelectField("Course", coerce=int, validators=[DataRequired()])
    # date = DateTimeField("Session date")
    submit = SubmitField("Create")

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class SessionCreateForm(FlaskForm):
    course = SelectField("Course", coerce=int, validators=[DataRequired()])
    s_type = RadioField("Course", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Create")

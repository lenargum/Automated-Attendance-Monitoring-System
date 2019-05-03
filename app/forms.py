from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import User
from app.models import Course
from app.models import Role


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()], render_kw={"placeholder": "Enter an e-mail address"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Enter a password"})
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class SessionCreateForm(FlaskForm):
    course = SelectField("Course", coerce=int, validators=[DataRequired()])
    s_type = RadioField("Course", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Create")



class UserCreateForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "New user name"})
    surname = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "New user surname"})
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "e-mail address"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Enter password"})
    password_2 = PasswordField("Repeat password", validators=[DataRequired(), EqualTo("password")],
                               render_kw={"placeholder": "Enter password again"})
    role = QuerySelectField("Role", query_factory=lambda: Role.query.all())
    is_admin = BooleanField("Is admin?")
    submit = SubmitField("Create user")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AdminUserModifyForm(FlaskForm):
    password = PasswordField("New password", validators=[DataRequired()], render_kw={"placeholder": "Enter password"})
    password_2 = PasswordField("Repeat password", validators=[DataRequired(), EqualTo("password")],
                               render_kw={"placeholder": "Enter password again"})
    submit = SubmitField("Update profile")


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators


class LoginForm(FlaskForm):
    """Represents the login form
    """

    user = StringField('User', [validators.DataRequired('User has to be present')])
    password = PasswordField('Password', [validators.DataRequired('Password is requried')])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')
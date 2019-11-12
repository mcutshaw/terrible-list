from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')
    remember_me = BooleanField('Remember Me')

class CaptureForm(FlaskForm):
    name = StringField('vApp Name')
    submit = SubmitField('Submit')
    error_override = BooleanField('Error Override')

class UsersForm(FlaskForm):
    
    name = StringField('Add new user')
    
class RegisterForm(FlaskForm):
    
    name = StringField('Add new account')
    password = StringField('password here')
    submit = SubmitField('Submit')

class ListForm(FlaskForm):

    name = StringField('Add new account')
    password = StringField('password here')
    submit = SubmitField('Submit')

class RemoveForm(FlaskForm):

    name = StringField('Person to remove from list')
    submit = SubmitField('Submit')

class AddForm(FlaskForm):

    name = StringField('Full name')
    username = StringField('Username')
    status = BooleanField('NAUGHTY')
    status_description = StringField('Why')
    submit = SubmitField('Submit')
from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import HiddenField
from wtforms import validators
import models

class PersonForm(FlaskForm): 
    Person_firstname = TextField()
    Person_lastname = TextField()
    Person_title = TextField()
    Person_telephone = TextField()
    Person_email = TextField()
    Person_position = TextField()
    Person_category = TextField()



class UserForm(FlaskForm):
    User_username = TextField()
    User_password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')




class UserPersonForm(UserForm, PersonForm):
    submit = SubmitField('Save')





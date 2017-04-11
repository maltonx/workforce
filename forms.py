from flask_wtf import Form
from wtforms import TextField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import validators

import models

class UserForm(Form):
    username = TextField()
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    email = TextField()
    submit = SubmitField()




class PersonForm(Form): 
    firstname = TextField()
    lastname = TextField()
    title = TextField()
    telephone = TextField()
    email = TextField()
    position = TextField()
    category = TextField()
    company_id = TextField()
    instance_id = TextField()
    submit = SubmitField()

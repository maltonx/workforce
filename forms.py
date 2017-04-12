from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import HiddenField
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import validators
from wtfpeewee.orm import model_form
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


class RegisterForm(
        model_form(models.Userperson), 
        model_form(models.Person),
        model_form(models.Address)):
    person = None
    instance = None
    company = None
    Address = None
    submit = SubmitField('Save')

class ManualRegisterForm(FlaskForm):
    Userperson_username = TextField()  #CharField(unique  #True)
    Userperson_password = PasswordField() #CharField(null  #False)
    Userperson_person = HiddenField(default='ForeignKey_Person') #ForeignKeyField(Person, related_name  #'person_userpersons', null  #True)
    #Userperson_instance = HiddenField(default='SelectForeignKey_Instance')  #ForeignKeyField(Instance, related_name  #'instance_userspersons', null  #True)
    Userperson_instance = SelectField(choices=[(x.id, x) for x in models.Instance().select()])
    Person_firstname = TextField()  #CharField()
    Person_lastname = TextField()  #CharField()
    Person_title = TextField()  #CharField()
    Person_address = HiddenField(default='ForeignKey_Address')  #ForeignKeyField(Address, related_name  #'address_persons', null  #True)
    Person_telephone = TextField()  #CharField()
    Person_email = TextField()  #CharField()
    Person_position = TextField()  #CharField()
    Person_category = TextField()  #CharField()
    Person_company = HiddenField(default='ForeignKey_Company')  #ForeignKeyField()
    Company_companyname = TextField()  #CharField()
    Company_address = HiddenField(default='ForeignKey_Address')  #ForeignKeyField(Address, related_name  #'address_companies')
    #Instance_name = TextField()  #CharField()
    #Instance_address = HiddenField(default='ForeignKey_Address')  #ForeignKeyField(Address, related_name  #'address_Instances', null  #True)
    #Instance_active = BooleanField()  #BooleanField()
    #Instance_category = TextField()  #CharField()
    Address_postaddress = TextField()  #CharField()
    Address_postalcode = IntegerField()  #IntegerField()
    Address_country = TextField()  #CharField()
    Address_telephone = TextField()  #CharField()
    submit = SubmitField('Save')



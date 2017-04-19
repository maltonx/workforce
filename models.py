#!/usr/bin/env
# -*- coding: UTF-8 -*-
from peewee import *
import os
from flask_login import UserMixin
import ConfigParser
from wtfpeewee.orm import model_form
import wtforms

CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath( __file__ )),
    'settings.ini'
    )
CONFIG = ConfigParser.ConfigParser()
CONFIG.read(CONFIG_FILE)


#---- database connection ------#
if CONFIG.get('database', 'uselocaldb'):
    sqlitefilepath = os.path.join(
        os.path.dirname(__file__), 
        CONFIG.get('database', 'localdatabase')
        )
    db = SqliteDatabase(sqlitefilepath)
else:
    db = MySQLDatabase(
        CONFIG.get('database', 'name'), 
        host = CONFIG.get('database', 'host'), 
        user = CONFIG.get('database', 'user'), 
        passwd = CONFIG.get('database', 'passwd')
        )


ALL_MODELS = []
ALL_MODELS_DICT = {}

# --- Base model --- #
class baseModel(Model):
    class Meta:
        database = db    

class Address(baseModel):
    postaddress = CharField()
    postalcode = IntegerField()
    country = CharField()
    telephone = CharField()

    def __unicode__(self):
        return self.postaddress


ALL_MODELS.append(Address)
ALL_MODELS_DICT['Address'] = Address
AddressForm = model_form(Address)


class Instance(baseModel):
    name = CharField()
    address = ForeignKeyField(Address, related_name = 'address_Instances', null = True)
    active = BooleanField()
    category = CharField()

    def __unicode__(self):
        return self.name


ALL_MODELS.append(Instance)
ALL_MODELS_DICT['Instance'] = Instance
InstanceForm = model_form(Instance)


class Company(baseModel):
    companyname = CharField()
    address = ForeignKeyField(Address, related_name = 'address_companies', null = True)
    def __unicode__(self):
        return self.companyname

ALL_MODELS.append(Company)
ALL_MODELS_DICT['Company'] = Company
CompanyForm = model_form(Company)

class Person(baseModel):
    firstname = CharField()
    lastname = CharField()
    title = CharField()
    address = ForeignKeyField(Address, related_name = 'address_persons', null = True)
    telephone = CharField()
    email = CharField()
    position = CharField()
    category = CharField()
    company = ForeignKeyField(Company, related_name = 'company_Persons', null = True)

    def __unicode__(self):
        return self.firstname


ALL_MODELS.append(Person)
ALL_MODELS_DICT['Person'] = Person
PersonForm = model_form(Person)

class Userperson(baseModel, UserMixin):
    username = CharField(unique = True)
    password = CharField(null = False)
    person = ForeignKeyField(Person, related_name = 'person_userpersons', null = True)
    instance = ForeignKeyField(Instance, related_name = 'instance_userspersons', null = True)

    def __unicode__(self):
        return self.username


ALL_MODELS.append(Userperson)
ALL_MODELS_DICT['Userperson'] = Userperson
UserpersonForm = model_form(Userperson)

class GroupOfAssets(baseModel):
    name = CharField()
    instance = ForeignKeyField(Instance, related_name = 'instance_GroupOfAssets', null = True)
    company = ForeignKeyField(Company, related_name = 'company_GroupOfAssets', null = True)
    def __unicode__(self):
        return self.name
ALL_MODELS.append(GroupOfAssets)
ALL_MODELS_DICT['GroupOfAssets'] = GroupOfAssets

class AssetType(baseModel):
    name = CharField() # dorr, tak
    label = CharField() # Dörr
    def __unicode__(self):
        return self.label
ALL_MODELS.append(AssetType)
ALL_MODELS_DICT['AssetType'] = AssetType

class Asset(baseModel): # door på clas ohlson
    GroupOfAssets = ForeignKeyField(GroupOfAssets, related_name = 'GroupOfAssets_Assets', null = True)
    category = IntegerField() # 1. spatialData(folder) / 2. physicalAsset / 3. TaskNonPhysical (todo)
    name = CharField() #huvudentre
    Description = CharField() # stor dörr
    AssetType = ForeignKeyField(AssetType, related_name = 'assettype_assets', null = True) # foreign key typ  typ_asset physical asset type
    rel = IntegerField() # risk effect level 1,2,3,4 not null
    performGPS = BooleanField() # yes/no
    performRFID = BooleanField() # yes/no
    performSWIPE = BooleanField() # yes/no
    performDATA = BooleanField() # yes/no
    template = BooleanField() # #yes or no
    parent = ForeignKeyField("self", related_name = 'children', null = True)
    sorting = IntegerField()
    active = BooleanField() # yes/no
    availability = IntegerField() #  0. not available 1. attendance rule  dvs. om attendece rule varje måndag t.ex  , 2. Always available and visible , 3. always available, but invisible
    def __unicode__(self):
        return self.name
ALL_MODELS.append(Asset)
ALL_MODELS_DICT['Asset'] = Asset

class Permission(baseModel):
    userperson = ForeignKeyField(Userperson, related_name = 'userperson_permissions', null = True)
    asset = ForeignKeyField(Asset, related_name = 'asset_permissions', null = True)    #asset_permitted_userpersons
    def __unicode__(self):
        return 'Permission'
ALL_MODELS.append(Permission)
ALL_MODELS_DICT['Permission'] = Permission

class Task(baseModel):
    asset = ForeignKeyField(Asset, related_name = 'asset_tasks', null = True)
    deadLine = TimestampField() #men hjälp av rel vet vi stard time end time
    def __unicode__(self):
        return self.asset.name
ALL_MODELS.append(Task)
ALL_MODELS_DICT['Task'] = Task

class TaskUserpersons(baseModel):
    task = ForeignKeyField(Task, related_name = 'task_userpersons', null = True)
    userperson = ForeignKeyField(Userperson, related_name = 'userperson_tasks', null = True)
    def __unicode__(self):
        return self.task.asset.name
ALL_MODELS.append(TaskUserpersons)
ALL_MODELS_DICT['TaskUserpersons'] = TaskUserpersons

class TaskGenerator(baseModel):  # genererar nästa deadline
    asset = ForeignKeyField(Asset, related_name = 'asset_taskgenerators', null = True)
    ruleCode = CharField()  #every hour workdays. #advanced feature
    interval = IntegerField()
    def __unicode__(self):
        return self.ruleCode
ALL_MODELS.append(TaskGenerator)
ALL_MODELS_DICT['TaskGenerator'] = TaskGenerator

class Category(baseModel):
    name = CharField()  # dorr, tak
    label = CharField()  # Dörr
    def __unicode__(self):
        return self.label
ALL_MODELS.append(Category)
ALL_MODELS_DICT['Category'] = Category

class CategoryDeviation(baseModel):
    category = ForeignKeyField(Category, related_name = 'category_deviations', null = True)
    value = CharField()
    def __unicode__(self):
        return self.value
ALL_MODELS.append(CategoryDeviation)
ALL_MODELS_DICT['CategoryDeviation'] = CategoryDeviation

class CategoryIntention(baseModel):
    category = ForeignKeyField(Category, related_name = 'category_intentions', null = True)
    value = CharField()
    def __unicode__(self):
        return self.value
ALL_MODELS.append(CategoryIntention)
ALL_MODELS_DICT['CategoryIntention'] = CategoryIntention

class AssetDeviation(baseModel):
    asset = ForeignKeyField(Asset, related_name = 'asset_deviations')
    CategoryDeviation = ForeignKeyField(CategoryDeviation, 
        related_name = 'categoryDeviation_AssetDeviations', 
        null = True)
    def __unicode__(self):
        return self.CategoryDeviation.value
ALL_MODELS.append(AssetDeviation)
ALL_MODELS_DICT['AssetDeviation'] = AssetDeviation

class AssetsIntention(baseModel):
    asset = ForeignKeyField(Asset, 
        related_name = 'asset_intention', 
        null = True)
    CategoryIntention = ForeignKeyField(CategoryIntention, 
        related_name = 'categoryIntention_AssetIntentions', 
        null = True)
    def __unicode__(self):
        return self.CategoryIntention.value

ALL_MODELS.append(AssetsIntention)
ALL_MODELS_DICT['AssetsIntention'] = AssetsIntention

### parametertypes are hard coded outside database   te.x cordinat, dropdownlist, contact)
class Parameter(baseModel):
    name = CharField() #post_address etc.
    datatype = CharField() #number, text, datum,(this is predefined in html, creates multiple parameters .. .  te.x cordinat, dropdownlist, contact)
    htmltype = CharField()
    def __unicode__(self):
        return self.name
ALL_MODELS.append(Parameter)
ALL_MODELS_DICT['Parameter'] = Parameter

class Value(baseModel):
    asset = ForeignKeyField(Asset, related_name = "asset_values", null = True)
    parameter = ForeignKeyField(Parameter, related_name = "parameter_values", null = True)
    value = CharField()
    def __unicode__(self):
        return '{}: {}'.format(self.parameter.name, self.value)
ALL_MODELS.append(Value)
ALL_MODELS_DICT['Value'] = Value

class Tag(baseModel):#tags
    asset = ForeignKeyField(Asset, related_name = "asset_Tags", null = True)
    label = CharField()
    def __unicode__(self):
        return self.label
ALL_MODELS.append(Tag)
ALL_MODELS_DICT['Tag'] = Tag


# ---   Functions  --- #
def resetDB():
    db.drop_tables(ALL_MODELS, safe=True)
    db.create_tables(ALL_MODELS)

    newUserperson = Userperson()
    newUserperson.username = 'Username'
    newUserperson.password = 'Password'
    newUserperson.email = 'username@email.com'
    newUserperson.save()



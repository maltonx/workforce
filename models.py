#!/usr/bin/env
# -*- coding: UTF-8 -*-
from peewee import *
import os
from flask_login import UserMixin
import ConfigParser


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
    post_address = CharField()
    postal_code = IntegerField()
    country = CharField()
    telephone = CharField()
ALL_MODELS.append(Address)
ALL_MODELS_DICT['Address'] = Address

class Instance(baseModel):
    name = CharField()
    address = ForeignKeyField(Address, related_name = 'address_Instances', null = True)
    active = CharField()
    category = CharField()
ALL_MODELS.append(Instance)
ALL_MODELS_DICT['Instance'] = Instance

class Company(baseModel):
    companyname = CharField()
    address = ForeignKeyField(Address, related_name = 'address_companies')
ALL_MODELS.append(Company)
ALL_MODELS_DICT['Company'] = Company

class Person(baseModel):
    firstname = CharField()
    lastname = CharField()
    title = CharField()
    Address = ForeignKeyField(Address, related_name = 'address_persons', null = True)
    telephone = CharField()
    email = CharField()
    position = CharField()
    category = CharField()
    company = ForeignKeyField(Company, related_name = 'company_Persons', null = True)
ALL_MODELS.append(Person)
ALL_MODELS_DICT['Person'] = Person

class User(baseModel, UserMixin):
    username = CharField(unique = True)
    password = CharField(null = False)
    person = ForeignKeyField(Person, related_name = 'person_users', null = True)
    instance = ForeignKeyField(Instance, related_name = 'instance_users', null = True)
ALL_MODELS.append(User)
ALL_MODELS_DICT['User'] = User


class GroupOfAssets(baseModel):
    name = CharField()
    instance = ForeignKeyField(Instance, related_name = 'instance_GroupOfAssets')
    company = ForeignKeyField(Company, related_name = 'company_GroupOfAssets')
ALL_MODELS.append(GroupOfAssets)
ALL_MODELS_DICT['GroupOfAssets'] = GroupOfAssets

class AssetType(baseModel):
    name = CharField() # dorr, tak
    label = CharField() # Dörr
ALL_MODELS.append(AssetType)
ALL_MODELS_DICT['AssetType'] = AssetType

class Asset(baseModel): # door på clas ohlson
    GroupOfAssets = ForeignKeyField(GroupOfAssets, related_name = 'GroupOfAssets_Assets')
    category = IntegerField() # 1. spatialData(folder) / 2. physicalAsset / 3. TaskNonPhysical (todo)
    name = CharField() #huvudentre
    Description = CharField() # stor dörr
    AssetType = ForeignKeyField(AssetType, related_name = 'assettype_assets') # foreign key typ  typ_asset physical asset type
    rel = IntegerField() # risk effect level 1,2,3,4 not null
    performGPS = BooleanField() # yes/no
    performRFID = BooleanField() # yes/no
    performSWIPE = BooleanField() # yes/no
    performDATA = BooleanField() # yes/no
    template = BooleanField() # #yes or no
    parent = ForeignKeyField("self", related_name = 'children')
    sorting = IntegerField()
    active = BooleanField() # yes/no
    availability = IntegerField() #  0. not available 1. attendance rule  dvs. om attendece rule varje måndag t.ex  , 2. Always available and visible , 3. always available, but invisible
ALL_MODELS.append(Asset)
ALL_MODELS_DICT['Asset'] = Asset

class Permission(baseModel):
    user = ForeignKeyField(User, related_name = 'user_permissions')
    asset = ForeignKeyField(Asset, related_name = 'asset_permissions')    #asset_permitted_users
ALL_MODELS.append(Permission)
ALL_MODELS_DICT['Permission'] = Permission

class Task(baseModel):
    asset = ForeignKeyField(Asset, related_name = 'asset_tasks')
    deadLine = TimestampField() #men hjälp av rel vet vi stard time end time
ALL_MODELS.append(Task)
ALL_MODELS_DICT['Task'] = Task

class TaskUsers(baseModel):
    task = ForeignKeyField(Task, related_name = 'task_users')
    user = ForeignKeyField(User, related_name = 'user_tasks')
ALL_MODELS.append(TaskUsers)
ALL_MODELS_DICT['TaskUsers'] = TaskUsers

class TaskGenerator(baseModel):  # genererar nästa deadline
    asset = ForeignKeyField(Asset, related_name = "asset_taskgenerators")
    ruleCode = CharField()  #every hour workdays. #advanced feature
    interval = IntegerField()
ALL_MODELS.append(TaskGenerator)
ALL_MODELS_DICT['TaskGenerator'] = TaskGenerator

class Category(baseModel):
    name = CharField()  # dorr, tak
    label = CharField()  # Dörr
ALL_MODELS.append(Category)
ALL_MODELS_DICT['Category'] = Category

class CategoryDeviation(baseModel):
    category = ForeignKeyField(Category, related_name = 'category_deviations')
    value = CharField()
ALL_MODELS.append(CategoryDeviation)
ALL_MODELS_DICT['CategoryDeviation'] = CategoryDeviation

class CategoryIntention(baseModel):
    Category = ForeignKeyField(Category, related_name = 'category_intentions')
    value = CharField()
ALL_MODELS.append(CategoryIntention)
ALL_MODELS_DICT['CategoryIntention'] = CategoryIntention

class AssetDeviation(baseModel):
    asset = ForeignKeyField(Asset, related_name = 'asset_deviations')
    CategoryDeviation = ForeignKeyField(CategoryDeviation, related_name = 'categoryDeviation_AssetDeviations')
ALL_MODELS.append(AssetDeviation)
ALL_MODELS_DICT['AssetDeviation'] = AssetDeviation

class AssetsIntention(baseModel):
    asset = ForeignKeyField(Asset, related_name = 'asset_intention')
    CategoryIntention = ForeignKeyField(CategoryIntention, related_name = 'categoryIntention_AssetIntentions')
ALL_MODELS.append(AssetsIntention)
ALL_MODELS_DICT['AssetsIntention'] = AssetsIntention

### parametertypes are hard coded outside database   te.x cordinat, dropdownlist, contact)
class Parameter(baseModel):
    name = CharField() #post_address etc.
    datatype = CharField() #number, text, datum,(this is predefined in html, creates multiple parameters .. .  te.x cordinat, dropdownlist, contact)
    htmltype = CharField()
ALL_MODELS.append(Parameter)
ALL_MODELS_DICT['Parameter'] = Parameter

class Value(baseModel):
    asset = ForeignKeyField(Asset, related_name = "asset_values")
    parameter = ForeignKeyField(Parameter, related_name = "parameter_values")
    value = CharField()
ALL_MODELS.append(Value)
ALL_MODELS_DICT['Value'] = Value

class Tag(baseModel):#tags
    asset = ForeignKeyField(Asset, related_name = "asset_Tags")
    label = CharField()
ALL_MODELS.append(Tag)
ALL_MODELS_DICT['Tag'] = Tag


# ---   Functions  --- #
def resetDB():
    db.drop_tables(ALL_MODELS, safe=True)
    db.create_tables(ALL_MODELS)

    newUser = User()
    newUser.username = 'Username'
    newUser.password = 'Password'
    newUser.email = 'username@email.com'
    newUser.save()


#resetDB()








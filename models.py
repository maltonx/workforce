#!/usr/bin/env
# -*- coding: <UTF-8> -*-
from peewee import *
import readSettingsFile as Conf
import os
from flask_login import UserMixin
import ConfigParser


SETTINGS_FILE = os.path.join(
    os.path.dirname(os.path.abspath( __file__ )),
    'settings.ini'
    )
CONFIG = ConfigParser.ConfigParser()
CONFIG.read(SETTINGS_FILE)


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

# --- Base model --- #
class baseModel(Model):
    class Meta:
        database = db    

class User(baseModel, UserMixin):
    username = CharField(unique = True)
    password = CharField(null = False)
    email = CharField()
ALL_MODELS.append(User)


# ---   Functions  --- #
def resetDB():
    db.drop_tables(ALL_MODELS, safe=True)
    db.create_tables(ALL_MODELS)

    newUser = User()
    newUser.username = 'Username'
    newUser.password = 'Password'
    newUser.email = 'username@email.com'
    newUser.save()
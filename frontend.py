#!/usr/bin/env
# -*- coding: <UTF-8> -*-
import os
import platform

# -- ACTIVATE VIRTUAL ENVIRONMENT -- #
if platform.system() == 'Windows':
    activate = os.path.join(
        os.path.dirname(__file__), 'venv_win', 'Scripts', 'activate_this.py')
else:
    activate = os.path.join(
        os.path.dirname(__file__), 'venv', 'bin', 'activate_this.py')
execfile(activate , dict(__file__= activate ))

from flask import Flask
from flask import render_template
import ConfigParser
CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath( __file__ )),
    'settings.ini'
    )
CONFIG = ConfigParser.ConfigParser()
CONFIG.read(CONFIG_FILE)



app = Flask(__name__)

app.config.update(dict(
    DEBUG = CONFIG.get('app', 'DEBUG'),
    SECRET_KEY = CONFIG.get('app', 'SECRET_KEY'),
    USERNAME = CONFIG.get('app', 'USERNAME'),
    PASSWORD = CONFIG.get('app', 'PASSWORD'),
))


from views import *



if __name__ == "__main__":
    app.run(host="0.0.0.0")
















    

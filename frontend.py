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

app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    SECRET_KEY='98huu4w9r8wo4r',
    USERNAME='admin',
    PASSWORD='default'
))

from wf_views import *


if __name__ == "__main__":
    app.run(host="0.0.0.0")
















    
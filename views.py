from frontend import app
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import redirect
from flask import url_for
import os
import models
import forms


@app.route('/', methods=['GET', 'POST'])
def frontpage():
    Form = forms.UserPersonForm(request.values)
    if request.method == 'POST':
        if Form.submit.data:
            saveFormsToModels(Form)
        return redirect(url_for('frontpage'))
    return render_template('frontpage.html', 
        users = models.User.select(),
        persons = models.Person.select(),
        userform = Form, 
        )


def saveFormsToModels(form):
    editedModels = {}
    for formfield in form.data:
        if formfield in ['csrf_token']:
            continue
        try:
            modelname, field = formfield.split('_')
        except:
            continue
        value = form[formfield].data
        try:
            setattr(editedModels[modelname], field, value)
        except:
            editedModels[modelname] = models.ALL_MODELS_DICT[modelname]()
            setattr(editedModels[modelname], field, value)
    for model in editedModels:
        for m in editedModels:
            try:
                setattr(editedModels[m], model.lower(), editedModels[model])
                print 'setted %s' % model.lower()
            except:
                pass
        editedModels[model].save()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/vnd.microsoft.icon')


from frontend import app
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import abort
import os
import models
import forms
from wtfpeewee.orm import model_form


@app.route('/register/', methods=['GET', 'POST'])
def register():
    Form = forms.ManualRegisterForm(request.values)
    if request.method == 'POST':
        if Form.submit.data:
            saveFormsToModels(Form)
        return redirect(url_for('register'))
    return render_template('frontpage.html', 
        form = Form, 
        )

@app.route('/edit/<modelname>/', methods=['GET', 'POST'])
def add(modelname):
    kwargs = listAndEdit(modelname)
    return render_template('addpage.html', **kwargs)

@app.route('/edit/<modelname>/<entryid>', methods=['GET', 'POST'])
def edit(modelname, entryid):
    kwargs = listAndEdit(modelname, entryid)
    return render_template('editpage.html', **kwargs)

def saveFormsToModels(form):
    # needs the form fields to be named modelname_fieldname
    editedModels = {}
    foreignKeys = []
    for formfield in form.data:
        if formfield in ['csrf_token']:
            continue
        try:
            modelname, field = formfield.split('_')
        except:
            continue
        value = form[formfield].data
        try:
            functionName, foreignKeyName = value.split('_')
            if functionName == 'ForeignKey':
                foreignKeys.append(
                    dict(
                        modelname = modelname,
                        field = field, 
                        foreignKeyName = foreignKeyName,
                        )
                    )
                continue
        except:
            pass
        try:
            setattr(editedModels[modelname], field, value)
        except:
            editedModels[modelname] = models.ALL_MODELS_DICT[modelname]()
            setattr(editedModels[modelname], field, value)
    for model in editedModels:
        editedModels[model].save()
    for key in foreignKeys:
        setattr(
            editedModels[key['modelname']], 
            key['field'], 
            editedModels[key['foreignKeyName']])
        print 'start'
        print 'Set attr: {}, {}, {}'.format(
            editedModels[key['modelname']], 
            key['field'], 
            editedModels[key['foreignKeyName']])
    for model in editedModels:
        editedModels[model].save()

def getFields(model, exclude=['id']):
    fields = [(x, type(model._meta.fields[x]).__name__) for x in model._meta.sorted_field_names if not x in exclude]
    return fields
  
def listAndEdit(modelname,entryid = 0, entries = False):
    try:
        model = models.ALL_MODELS_DICT[modelname]
    except KeyError:
        abort(404)
    if not entries:
        entries = model.select()
    modelForm = model_form(model)
    fields = getFields(model)
    try:
        entry = model.get(id=int(entryid))
    except:
        entry = model()
    if request.method == 'POST':
        if request.form['submit'] == 'Save':
            form = modelForm(request.values, obj = entry)
            if form.validate():
                form.populate_obj(entry)
                entry.save()
                flash('Your entry has been saved')
                print 'saved'
        elif request.form['submit'] == 'Delete':
            try:
                model.get(id=int(entryid)).delete_instance(recursive = True)
                return redirect(url_for('add', modelname = modelname))
            except:
                entry = model()
                form = modelForm(obj = entry)
    else:
        form = modelForm(obj = entry)




    kwargs = dict(
        links = [x.__name__ for x in models.ALL_MODELS],
        header = model.__name__,
        form=form, 
        entry=entry, 
        entries=entries, 
        fields = fields,
        )

    return kwargs


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/vnd.microsoft.icon')


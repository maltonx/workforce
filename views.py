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

@app.route('/add/<modelname>/', methods=['GET', 'POST'])
def add(modelname):
    kwargs = listAndEdit(modelname)
    return render_template('addpage.html', **kwargs)

@app.route('/add/<modelname>/to/<foreign_table>/<foreign_key>', methods=['GET', 'POST'])
def addto(modelname, foreign_table, foreign_key):
    kwargs = listAndEdit(modelname, 
        action = 'AddTo', 
        foreign_table = foreign_table, 
        foreign_key = foreign_key)
    return render_template('addpage.html', **kwargs)

@app.route('/edit/<modelname>/<entryid>', methods=['GET', 'POST'])
def edit(modelname, entryid):
    kwargs = listAndEdit(modelname, entryid)
    #print kwargs
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
    foreignKeys = {x.column : x.dest_table for x in models.db.get_foreign_keys(model.__name__)}
    #fields = [(x, type(model._meta.fields[x]).__name__, foreignKeys) for x in model._meta.sorted_field_names if not x in exclude]
    #print foreignKeys
    fields = []
    for field in model._meta.sorted_field_names:
        if not field in exclude:
            fieldtype = type(model._meta.fields[field]).__name__
            foreignFieldName = '{}_id'.format(field)
            if foreignFieldName in foreignKeys:
                foreignKeyModelName = foreignKeys[foreignFieldName].title()
            else:
                foreignKeyModelName = False
            fields.append(
                (field, fieldtype, foreignKeyModelName))
            #print "Field: {}\nType: {}\nModelname: {}\n".format(field, fieldtype, foreignKeyModelName)
    return fields
  
def getRelatedModels(entry):
    entries = []
    try:
        for query, fk in reversed(list(entry.dependencies())):
            #for x in dir(fk):
                #print x
            for x in fk.model_class.select().where(query):
                #print 'here:'
                #print x
                entries.append(x)
    except:
        pass
    return entries



def listAndEdit(modelname, entryid = 0, entries = False, action = False, **kwargs):
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
        dependencies = getRelatedModels(entry)
    except:
        entry = model()
        dependencies = False



    form = modelForm(obj = entry)

    if request.method == 'POST':
        if request.form['submit'] == 'Save':
            form = modelForm(request.values, obj = entry)
            if form.validate():
                form.populate_obj(entry)
                entry.save()
                if action == 'AddTo':
                    addForeignKey(model, entry, kwargs['foreign_table'], kwargs['foreign_key'])
                    redirect(url_for('edit', modelname = model, entryid = kwargs['foreign_key']))
                flash('Your entry has been saved')
                print 'saved'
        elif request.form['submit'] == 'Delete':
            try:
                model.get(model.id == int(entryid)).delete_instance(recursive = True)
                #redirect(url_for('add', modelname = modelname))
            except:
                pass
            finally:
                entry = model()
                form = modelForm(obj = entry)



    kwargs = dict(
        links = [x.__name__ for x in models.ALL_MODELS],
        header = model.__name__,
        form=form, 
        entry=entry, 
        entries=entries, 
        fields = fields,
        dependencies = dependencies,
        )




    return kwargs


def addForeignKey(model, entry, foreign_table, foreign_key):
    foreignModel = models.ALL_MODELS_DICT[foreign_table]
    foreignItem = foreignModel.get(foreignModel.id == int(foreign_key))
    foreignFieldName = model.__name__.lower()
    print "entry = {}".format(foreignModel)
    print "item = {}".format(foreignItem)
    print "fieldName = {}".format(foreignFieldName)
    print "id = {}".format(entry.id)

    setattr(foreignItem, foreignFieldName, entry.id)
    foreignItem.save()




@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/vnd.microsoft.icon')


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
def user():
    users = models.User.select()
    form = forms.UserForm()
    try:
        if request.form['Delete']:
            models.User.get(models.User.id == request.form['Delete']).delete_instance()
            return redirect(url_for('user'))
    except:
        pass
    if request.method == 'POST':
        u = models.User()
        u.username = request.form['username']
        u.password = request.form['username']
        u.email = request.form['username']
        u.save()
        return redirect(url_for('user'))

    return render_template('frontpage.html', form = form, users = users)


@app.route('/delete/<userid>')
def delete(userid):
    models.User.get(id = userid).delete_instance()








@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/vnd.microsoft.icon')


from frontend import app
from flask import render_template
import os

@app.route('/')
def frontpage():
    print "hej"
    username = 'Malte'
    return render_template('frontpage.html', username = username)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/vnd.microsoft.icon')

def bajs():
    print 'hej'
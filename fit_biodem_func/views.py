""" Run with
export FLASK_ENV=development
export FLASK_APP=fit_biodem_func/views.py
poetry run flask run """


import os
from flask import (
    Flask, flash, request, render_template, 
    redirect, url_for, send_from_directory)
from werkzeug.utils import secure_filename
from .user_data import create_app

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app = create_app()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


""" @app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
 """


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])
def get_userdata():
    if request.method == 'POST' and 'first_name' in request.form:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
    return render_template('index.html',
                           first_name=first_name,
                           last_name=last_name,
                           email=email)


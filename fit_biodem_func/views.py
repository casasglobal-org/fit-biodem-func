""" Run with
export FLASK_ENV=development
export FLASK_APP=fit_biodem_func/views.py
poetry run flask run """


import os
import csv
from flask import (
    flash, request, render_template, redirect,
    url_for, send_from_directory)
from werkzeug.utils import secure_filename
from .user_data import create_app

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'fit_biodem_func/uploads')
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
            fit_uploaded_data(app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('index.html')


# Serving the uploaded file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


# This route was defined as / and therefor overrode the earlier '/' endpoint
@app.route('/userdata', methods=['GET', 'POST'])
def get_userdata():
    if request.method == 'POST' and 'first_name' in request.form:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
    return render_template('index.html',
                           first_name=first_name,
                           last_name=last_name,
                           email=email)


# https://viveksb007.github.io/2018/04/uploading-processing-downloading-files-in-flask 
def fit_uploaded_data(path, filename):
    # Deduce the format of the CSV file
    csv_upload_file = os.path.join(path, filename)
    with open(csv_upload_file, newline='') as csvfile:
        # dialect = csv.Sniffer().sniff(csvfile.readline(), ['\t', ','])
        # csvfile.seek(0)  # sets the pointer to the biginning
        reader = csv.DictReader(csvfile, delimiter='\t')
        # reader.fieldnames = 'temperature', 'development_rate'
        # next(reader)
        temperature_list = []
        development_rate_list = []
        for row in reader:
            temperature_list.append(float(row['temperature']))
            development_rate_list.append(float(row['dev_rate']))
        print(temperature_list)
        print(development_rate_list)
    # Call funciton fitting routine from module [...]
